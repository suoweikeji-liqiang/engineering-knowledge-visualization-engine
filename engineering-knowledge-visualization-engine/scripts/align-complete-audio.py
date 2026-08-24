#!/usr/bin/env python3
"""Align frozen Agent/Harness narration text to real per-shot speech timestamps."""

from __future__ import annotations

import argparse
import difflib
import glob
import hashlib
import json
import re
import statistics
import wave
from pathlib import Path

from faster_whisper import WhisperModel


ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "ai-agent-harness-complete"
PUNCTUATION = re.compile(r"[\s，。！？；、：,.!?;:'\"“”‘’（）()《》〈〉—…·`~\-_/\\]+")
CLAUSE_END = set("。！？；，、：")


def normalize(text: str) -> str:
    return PUNCTUATION.sub("", text).lower()


def split_caption(text: str, max_chars: int = 24) -> list[str]:
    clauses: list[str] = []
    current = ""
    for char in text.strip():
        current += char
        if char in CLAUSE_END:
            clauses.append(current.strip())
            current = ""
    if current.strip():
        clauses.append(current.strip())
    result: list[str] = []
    current = ""
    for clause in clauses:
        if current and len(current) + len(clause) > max_chars:
            result.append(current)
            current = clause
        else:
            current += clause
    if current:
        result.append(current)
    return result or [text]


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / audio.getframerate()


def select_audio(cache_root: Path, shot_id: str, expected_duration: float) -> Path:
    candidates = [Path(path) for path in glob.glob(str(cache_root / f"{shot_id}-*.wav"))]
    if not candidates:
        raise FileNotFoundError(f"No cached narration segment for {shot_id} in {cache_root}")
    return min(candidates, key=lambda path: abs(wav_duration(path) - expected_duration))


def recognized_characters(words) -> tuple[str, list[tuple[float, float]]]:
    text = ""
    times: list[tuple[float, float]] = []
    for word in words:
        token = normalize(word.word)
        if not token or word.start is None or word.end is None:
            continue
        duration = max(0.01, word.end - word.start)
        for index, char in enumerate(token):
            start = word.start + duration * (index / len(token))
            end = word.start + duration * ((index + 1) / len(token))
            text += char
            times.append((start, end))
    return text, times


def target_character_times(target: str, recognized: str, recognized_times: list[tuple[float, float]]) -> list[tuple[float, float]]:
    matcher = difflib.SequenceMatcher(a=target, b=recognized, autojunk=False)
    direct: dict[int, tuple[float, float]] = {}
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            direct[block.a + offset] = recognized_times[block.b + offset]
    if not direct:
        raise ValueError("ASR produced no characters matching the frozen narration")

    mapped: list[tuple[float, float] | None] = [direct.get(index) for index in range(len(target))]
    for index, value in enumerate(mapped):
        if value is not None:
            continue
        left = next((cursor for cursor in range(index - 1, -1, -1) if mapped[cursor] is not None), None)
        right = next((cursor for cursor in range(index + 1, len(mapped)) if mapped[cursor] is not None), None)
        left_time = mapped[left][1] if left is not None else recognized_times[0][0]
        right_time = mapped[right][0] if right is not None else recognized_times[-1][1]
        run_start = (left + 1) if left is not None else 0
        run_end = right if right is not None else len(mapped)
        slots = max(1, run_end - run_start)
        slot = index - run_start
        start = left_time + (right_time - left_time) * (slot / slots)
        end = left_time + (right_time - left_time) * ((slot + 1) / slots)
        mapped[index] = (start, max(start + 0.01, end))
    return [value for value in mapped if value is not None]


def align_chunks(dialogue: str, chunks: list[str], recognized: str, recognized_times: list[tuple[float, float]]) -> list[dict]:
    target = normalize(dialogue)
    mapped = target_character_times(target, recognized, recognized_times)
    cues: list[dict] = []
    cursor = 0
    for index, chunk in enumerate(chunks):
        chunk_length = len(normalize(chunk))
        if chunk_length <= 0:
            continue
        start_index = cursor
        end_index = min(len(mapped), cursor + chunk_length)
        if start_index >= len(mapped) or end_index <= start_index:
            raise ValueError(f"Caption chunk {index} falls outside aligned text")
        start = mapped[start_index][0]
        end = mapped[end_index - 1][1]
        if cues:
            start = max(start, cues[-1]["end"])
        cues.append({"index": index, "text": chunk, "start": round(start, 3), "end": round(max(start + 0.08, end), 3)})
        cursor += chunk_length
    return cues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="base")
    parser.add_argument("--prompt-retry-threshold", type=float, default=0.9)
    parser.add_argument("--model-cache", default="/tmp/agent-harness-whisper-models")
    parser.add_argument("--audio-cache", default=str(ROOT.parent / "sandiao-science-studio" / "build" / "audio" / "ai-agent-harness-complete"))
    args = parser.parse_args()

    story = json.loads((EXAMPLE / "storyboard" / "story.json").read_text())
    source_timeline = json.loads((EXAMPLE / "audio" / "ai-agent-harness-complete.timeline.json").read_text())
    story_by_id = {shot["id"]: shot for shot in story["shots"]}
    cache_root = Path(args.audio_cache).resolve()
    model = WhisperModel(args.model, device="cpu", compute_type="int8", download_root=args.model_cache)

    output_shots: list[dict] = []
    similarities: list[float] = []
    matched_ratios: list[float] = []
    for timing in source_timeline["shots"]:
        shot = story_by_id[timing["id"]]
        audio_path = select_audio(cache_root, timing["id"], timing["duration"])
        target = normalize(shot["dialogue"])

        def transcribe(initial_prompt: str | None) -> dict:
            segments, _ = model.transcribe(
                str(audio_path),
                language="zh",
                beam_size=5,
                word_timestamps=True,
                vad_filter=False,
                condition_on_previous_text=False,
                initial_prompt=initial_prompt,
            )
            segments = list(segments)
            words = [word for segment in segments for word in (segment.words or [])]
            recognized, recognized_times = recognized_characters(words)
            matcher = difflib.SequenceMatcher(a=target, b=recognized, autojunk=False)
            similarity = matcher.ratio()
            matching = sum(block.size for block in matcher.get_matching_blocks())
            return {
                "segments": segments,
                "words": words,
                "recognized": recognized,
                "recognizedTimes": recognized_times,
                "similarity": similarity,
                "matchedRatio": matching / max(1, len(target)),
                "promptMode": "frozen-dialogue" if initial_prompt else "none",
            }

        candidates = [transcribe(None)]
        if candidates[0]["similarity"] < args.prompt_retry_threshold:
            candidates.append(transcribe(shot["dialogue"]))
        best = max(candidates, key=lambda candidate: (candidate["similarity"], candidate["matchedRatio"]))
        segments = best["segments"]
        words = best["words"]
        recognized = best["recognized"]
        recognized_times = best["recognizedTimes"]
        similarity = best["similarity"]
        matched_ratio = best["matchedRatio"]
        chunks = split_caption(shot["dialogue"])
        cues = align_chunks(shot["dialogue"], chunks, recognized, recognized_times)
        similarities.append(similarity)
        matched_ratios.append(matched_ratio)
        output_shots.append({
            "id": timing["id"],
            "audioFile": audio_path.name,
            "audioDuration": round(wav_duration(audio_path), 3),
            "transcript": "".join(segment.text for segment in segments).strip(),
            "similarity": round(similarity, 4),
            "matchedTargetCharacterRatio": round(matched_ratio, 4),
            "promptMode": best["promptMode"],
            "wordCount": len(words),
            "cues": cues,
        })
        print(f"{timing['id']}: similarity={similarity:.3f}, matched={matched_ratio:.3f}, cues={len(cues)}")

    output = {
        "schemaVersion": "1.0",
        "storySlug": story["meta"]["slug"],
        "storyFingerprint": source_timeline["storyFingerprint"],
        "narrationMasterSha256": hashlib.sha256((EXAMPLE / "audio" / "ai-agent-harness-complete.wav").read_bytes()).hexdigest(),
        "method": "faster-whisper-word-timestamps-plus-frozen-text-alignment",
        "model": args.model,
        "timingDomain": "raw-narration-before-playback-rate",
        "proportionalFallbackAllowed": False,
        "metrics": {
            "shots": len(output_shots),
            "meanTranscriptSimilarity": round(statistics.mean(similarities), 4),
            "minimumTranscriptSimilarity": round(min(similarities), 4),
            "meanMatchedTargetCharacterRatio": round(statistics.mean(matched_ratios), 4),
            "minimumMatchedTargetCharacterRatio": round(min(matched_ratios), 4),
        },
        "shots": output_shots,
    }
    target_path = EXAMPLE / "audio" / "forced-alignment.timeline.json"
    target_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(target_path), **output["metrics"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
