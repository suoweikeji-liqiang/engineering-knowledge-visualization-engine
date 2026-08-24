from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Protocol

from .mimo import MimoClient
from .settings import load_dotenv
from .story import Character


class SpeechProvider(Protocol):
    name: str

    def cache_key(self, text: str, character: Character) -> str: ...

    def synthesize(self, text: str, character: Character, output: Path) -> Path: ...


class MimoSpeechProvider:
    name = "mimo"

    def __init__(self, client: MimoClient | None = None):
        self.client = client or MimoClient()

    def cache_key(self, text: str, character: Character) -> str:
        model = str(character.voice.get("mimo_model") or self.client.config.tts_model)
        voice = str(character.voice.get("mimo_voice") or self.client.config.tts_voice)
        voice_sample = str(character.voice.get("mimo_voice_sample") or "")
        style = str(character.voice.get("style") or "")
        optimize_text_preview = character.voice.get("mimo_optimize_text_preview")
        return json.dumps(
            {
                "provider": self.name,
                "model": model,
                "voice": voice,
                "voice_sample": voice_sample,
                "style": style,
                "optimize_text_preview": optimize_text_preview,
                "text": text,
            },
            ensure_ascii=False,
            sort_keys=True,
        )

    def synthesize(self, text: str, character: Character, output: Path) -> Path:
        model = str(character.voice.get("mimo_model") or self.client.config.tts_model)
        voice = str(character.voice.get("mimo_voice") or self.client.config.tts_voice)
        voice_sample = character.voice.get("mimo_voice_sample")
        style = str(character.voice.get("style") or "")
        return self.client.synthesize(
            text,
            output,
            model=model,
            voice=voice,
            voice_sample=str(voice_sample) if voice_sample else None,
            style=style,
            audio_format="wav",
            optimize_text_preview=character.voice.get("mimo_optimize_text_preview"),
        )


class EspeakSpeechProvider:
    name = "espeak"

    def __init__(self):
        self.command = shutil.which("espeak-ng") or shutil.which("espeak")
        if not self.command:
            raise RuntimeError("espeak/espeak-ng not found")

    def cache_key(self, text: str, character: Character) -> str:
        return json.dumps({"provider": self.name, "voice": character.voice, "text": text}, ensure_ascii=False, sort_keys=True)

    def synthesize(self, text: str, character: Character, output: Path) -> Path:
        output.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                self.command,
                "-v", str(character.voice.get("voice", "zh")),
                "-s", str(character.voice.get("speed", 180)),
                "-p", str(character.voice.get("pitch", 50)),
                "-a", "165",
                "-w", str(output),
                text,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return output


def resolve_speech_provider(name: str = "auto") -> SpeechProvider | None:
    load_dotenv()
    selected = (name if name != "auto" else os.environ.get("SANDIAO_TTS_PROVIDER", "auto")).strip().lower()
    if selected == "auto":
        selected = "mimo" if os.environ.get("MIMO_API_KEY") else "espeak"
    if selected == "mimo":
        return MimoSpeechProvider()
    if selected == "espeak":
        return EspeakSpeechProvider() if shutil.which("espeak-ng") or shutil.which("espeak") else None
    if selected in {"none", "silent"}:
        return None
    raise RuntimeError(f"unknown TTS provider: {selected}")
