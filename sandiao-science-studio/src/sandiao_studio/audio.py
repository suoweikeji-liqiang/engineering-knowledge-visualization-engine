from __future__ import annotations

import hashlib
import math
import shutil
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

from .story import Story

RATE = 44_100

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


def build_audio(story: Story, output: Path | None = None) -> Path:
    out = (output or story.audio).resolve()
    master = np.zeros(int(story.duration*RATE), dtype=np.float32)
    espeak = shutil.which("espeak-ng") or shutil.which("espeak")
    cursor = 0.0
    for shot in story.shots:
        start, room = int(cursor*RATE), int((shot.duration-.43)*RATE)
        if espeak and shot.dialogue and shot.speaker:
            char = story.characters[shot.speaker]
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            try:
                subprocess.run([espeak, "-v", str(char.voice.get("voice", "zh")),
                                "-s", str(char.voice.get("speed", 180)),
                                "-p", str(char.voice.get("pitch", 50)),
                                "-a", "165", "-w", str(tmp_path), shot.dialogue],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                data, rate = _read_wav(tmp_path)
                data = _resample(data, round(len(data)*RATE/rate))
                if len(data) > room: data = _resample(data, room)
                _mix(master, data, start+int(.25*RATE), .84)
            finally:
                tmp_path.unlink(missing_ok=True)
        for i, name in enumerate(shot.sfx):
            _mix(master, _sfx(name), start+int((.04+.14*i)*RATE), .9)
        cursor += shot.duration
    _write_wav(out, master)
    return out
