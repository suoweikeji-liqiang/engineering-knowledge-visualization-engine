from __future__ import annotations

import hashlib
import math
import wave
from pathlib import Path

import numpy as np

from .story import Story
from .resolved_timeline import ResolvedShot, save_resolved_timeline
from .settings import project_root
from .speech import resolve_speech_provider

RATE = 44_100
SPEECH_TAIL_SECONDS = 0.2
SILENCE_TRIM_THRESHOLD_DB = -48.0
SILENCE_TRIM_LEADING_SECONDS = 0.06
SILENCE_TRIM_TRAILING_SECONDS = 0.12

def _read_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as wav:
        rate, channels, width = wav.getframerate(), wav.getnchannels(), wav.getsampwidth()
        raw = wav.readframes(wav.getnframes())
    if width != 2: raise RuntimeError("only 16-bit WAV is supported")
    data = np.frombuffer(raw, dtype=np.int16).astype(np.float32)/32768
    if channels > 1: data = data.reshape(-1, channels).mean(axis=1)
    return data, rate


def _resample(data: np.ndarray, length: int) -> np.ndarray:
    if len(data) == length: return data
    return np.interp(np.linspace(0, 1, length, endpoint=False),
                     np.linspace(0, 1, len(data), endpoint=False), data).astype(np.float32)


def _trim_silence(data: np.ndarray) -> np.ndarray:
    """Remove TTS container silence while preserving natural breath margins."""
    if len(data) == 0:
        return data
    threshold = 10 ** (SILENCE_TRIM_THRESHOLD_DB / 20)
    active = np.flatnonzero(np.abs(data) >= threshold)
    if len(active) == 0:
        return data
    start = max(0, int(active[0]) - round(SILENCE_TRIM_LEADING_SECONDS * RATE))
    end = min(len(data), int(active[-1]) + 1 + round(SILENCE_TRIM_TRAILING_SECONDS * RATE))
    return data[start:end]


def _write_wav(path: Path, data: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    peak = float(np.max(np.abs(data))) if len(data) else 0
    if peak > .96: data *= .96/peak
    pcm = (np.clip(data, -1, 1)*32767).astype(np.int16)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(RATE); wav.writeframes(pcm.tobytes())


def _mix(target: np.ndarray, clip: np.ndarray, start: int, gain: float = 1) -> None:
    end = min(len(target), start+len(clip))
    if start < len(target): target[start:end] += clip[:end-start]*gain


def _sfx(name: str) -> np.ndarray:
    n = int(RATE*(.5 if name in {"ding", "sparkle"} else .35))
    t = np.arange(n)/RATE
    if name == "impact": return (.3*np.sin(2*math.pi*85*t)*np.exp(-10*t)).astype(np.float32)
    if name == "boing": return (.18*np.sin(2*math.pi*(520*t-230*t*t))*np.exp(-4*t)).astype(np.float32)
    if name == "whoosh": return (.08*np.random.default_rng(7).standard_normal(n)*np.sin(math.pi*t/t[-1])**2).astype(np.float32)
    return (.11*(np.sin(2*math.pi*880*t)+.5*np.sin(2*math.pi*1320*t))*np.exp(-5*t)).astype(np.float32)


def build_audio(story: Story, output: Path | None = None, provider: str = "auto") -> Path:
    out = (output or story.audio).resolve()
    speech = resolve_speech_provider(provider)
    cache_dir = project_root() / "build" / "audio" / story.slug
    clips: dict[str, np.ndarray] = {}
    resolved_shots: list[ResolvedShot] = []
    for shot in story.shots:
        speech_duration = 0.0
        if speech and shot.dialogue and shot.speaker:
            char = story.characters[shot.speaker]
            digest = hashlib.sha256(speech.cache_key(shot.dialogue, char).encode("utf-8")).hexdigest()[:20]
            clip = cache_dir / f"{shot.id}-{digest}.wav"
            if not clip.exists() or clip.stat().st_size == 0:
                speech.synthesize(shot.dialogue, char, clip)
            data, rate = _read_wav(clip)
            data = _resample(data, round(len(data)*RATE/rate))
            data = _trim_silence(data)
            clips[shot.id] = data
            speech_duration = len(data) / RATE
        duration = max(shot.duration, speech_duration + SPEECH_TAIL_SECONDS)
        resolved_shots.append(ResolvedShot(shot.id, shot.duration, speech_duration, duration))

    total_duration = sum(item.duration for item in resolved_shots)
    master = np.zeros(round(total_duration*RATE), dtype=np.float32)
    cursor = 0.0
    for shot, resolved in zip(story.shots, resolved_shots):
        start = int(cursor*RATE)
        if shot.id in clips:
            _mix(master, clips[shot.id], start+int(.25*RATE), .84)
        for i, name in enumerate(shot.sfx):
            _mix(master, _sfx(name), start+int((.04+.14*i)*RATE), .9)
        cursor += resolved.duration
    _write_wav(out, master)
    save_resolved_timeline(story, speech.name if speech else "silent", resolved_shots, out)
    return out
