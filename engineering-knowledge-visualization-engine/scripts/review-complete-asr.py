#!/usr/bin/env python3
"""Blindly transcribe every MiMo segment and compare it with the authored narration."""
from __future__ import annotations

import base64
import difflib
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/ai-agent-harness-complete"
STORY = json.loads((EXAMPLE / "storyboard/story.json").read_text(encoding="utf-8"))
AI_DAILY = Path(os.environ.get("AI_DAILY_REPO", "/Users/asteroida/work/ai_daily_brief_factory_v3"))
SANDIAO = ROOT.parent / "sandiao-science-studio"
CACHE = SANDIAO / "build/audio/ai-agent-harness-complete"

sys.path.insert(0, str(AI_DAILY))
from dailybrief.utils import load_dotenv_if_available  # noqa: E402

load_dotenv_if_available(AI_DAILY / ".env")

PROMPT = """你是语音识别引擎。请逐字转写这段音频，不要总结、润色或解释。
中文按听到的内容写；英文术语保留英文；数字按听到的写；不要省略。只输出转写文本。"""


def clean(text: str) -> str:
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", text.lower())


def ratio(expected: str, heard: str) -> float:
    return difflib.SequenceMatcher(None, clean(expected), clean(heard)).ratio()


def audio_url(path: Path) -> str:
    return "data:audio/wav;base64," + base64.b64encode(path.read_bytes()).decode()


def transcribe(path: Path) -> str:
    endpoint = os.environ.get("MIMO_API_BASE", "https://token-plan-sgp.xiaomimimo.com/v1").rstrip("/")
    payload = {
        "model": os.environ.get("MIMO_MULTIMODAL_MODEL") or "mimo-v2.5",
        "messages": [{"role": "user", "content": [
            {"type": "input_audio", "input_audio": {"data": audio_url(path)}},
            {"type": "text", "text": PROMPT},
        ]}],
        "max_completion_tokens": 2200,
    }
    headers = {"api-key": os.environ["MIMO_API_KEY"], "Content-Type": "application/json"}
    for attempt in range(3):
        try:
            response = requests.post(f"{endpoint}/chat/completions", headers=headers, json=payload, timeout=300)
            response.raise_for_status()
            heard = response.json()["choices"][0]["message"]["content"].strip()
            refusal_markers = (
                "没有收到任何音频", "上传音频文件", "无法访问音频", "未提供音频",
                "我是文本生成AI", "无法处理音频", "无法接收或处理音频", "基于文本的AI助手",
            )
            if not clean(heard) or any(marker in heard for marker in refusal_markers):
                raise ValueError("MiMo returned an empty or no-audio transcription")
            return heard
        except Exception as exc:  # noqa: BLE001
            if attempt == 2:
                return f"ERROR:{type(exc).__name__}:{str(exc)[:100]}"
            time.sleep(5 * (attempt + 1))
    return "ERROR"


def segment_for(shot_id: str) -> Path:
    exact = re.compile(rf"^{re.escape(shot_id)}-[0-9a-f]{{20}}\.wav$")
    matches = sorted((path for path in CACHE.glob(f"{shot_id}-*.wav") if exact.match(path.name)), key=lambda path: path.stat().st_mtime, reverse=True)
    if not matches:
        raise FileNotFoundError(f"No cached MiMo segment for {shot_id} in {CACHE}")
    return matches[0]


def main() -> int:
    requested = {item.strip() for item in os.environ.get("ASR_ONLY", "").split(",") if item.strip()}
    jobs = [(shot["id"], shot["dialogue"], segment_for(shot["id"])) for shot in STORY["shots"] if not requested or shot["id"] in requested]
    output = EXAMPLE / "evaluation/asr-report.json"
    previous = json.loads(output.read_text(encoding="utf-8")) if output.exists() and requested else {}
    results: dict[str, dict[str, object]] = dict(previous.get("results", {}))
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(transcribe, wav): (shot_id, expected) for shot_id, expected, wav in jobs}
        for future in as_completed(futures):
            shot_id, expected = futures[future]
            heard = future.result()
            heard = re.sub(r"^\s*\d{1,2}:\d{2}\s*", "", heard)
            heard = heard.split("你是语音识别引擎", 1)[0].strip()
            score = ratio(expected, heard)
            results[shot_id] = {"similarity": round(score, 3), "expected": expected, "heard": heard}
            print(f"{shot_id}: {score:.3f}", flush=True)

    ordered = {shot["id"]: results[shot["id"]] for shot in STORY["shots"]}
    scores = [float(item["similarity"]) for item in ordered.values()]
    summary = {
        "segments": len(scores),
        "meanSimilarity": round(sum(scores) / len(scores), 3),
        "minimumSimilarity": min(scores),
        "below0_8": sum(score < 0.8 for score in scores),
        "errors": sum(str(item["heard"]).startswith("ERROR:") for item in ordered.values()),
    }
    report = {
        "schemaVersion": "1.0",
        "method": "MiMo multimodal blind ASR + normalized character similarity",
        "thresholds": {"pass": 0.8, "review": 0.7},
        "summary": summary,
        "results": ordered,
    }
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return 1 if summary["errors"] or summary["below0_8"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
