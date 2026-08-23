from __future__ import annotations

import base64
import mimetypes
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

from .settings import load_dotenv


DEFAULT_ASR_PROMPT = """你是语音识别引擎。请逐字转写音频，不要总结、润色或纠错；保留数字、英文术语和听到的异常音节。只输出转写文本。"""
DEFAULT_VIDEO_PROMPT = """请理解这段视频的画面和声音，概括内容、叙事结构、关键事实，并指出明显的音画、字幕或表达问题。"""


class MimoError(RuntimeError):
    pass


@dataclass(frozen=True)
class MimoConfig:
    api_key: str
    base_url: str = "https://token-plan-sgp.xiaomimimo.com/v1"
    multimodal_model: str = "mimo-v2.5"
    tts_model: str = "mimo-v2.5-tts"
    tts_voice: str = "mimo_default"
    timeout: int = 300
    retries: int = 3
    max_data_url_chars: int = 27_000_000

    @classmethod
    def from_env(cls) -> "MimoConfig":
        load_dotenv()
        key = os.environ.get("MIMO_API_KEY", "").strip()
        if not key:
            raise MimoError("MIMO_API_KEY is not configured; add it to .env or the shell environment")
        return cls(
            api_key=key,
            base_url=os.environ.get("MIMO_API_BASE", cls.base_url).strip().rstrip("/"),
            multimodal_model=os.environ.get("MIMO_MULTIMODAL_MODEL", cls.multimodal_model).strip(),
            tts_model=os.environ.get("MIMO_TTS_MODEL", cls.tts_model).strip(),
            tts_voice=os.environ.get("MIMO_TTS_VOICE", cls.tts_voice).strip(),
            timeout=int(os.environ.get("MIMO_TIMEOUT_SECONDS", cls.timeout)),
        )

    @property
    def endpoint(self) -> str:
        base = self.base_url.rstrip("/")
        return base if base.endswith("/chat/completions") else base + "/chat/completions"


def _message(data: dict[str, Any]) -> dict[str, Any]:
    choices = data.get("choices") or []
    if not choices or not isinstance(choices[0], dict):
        raise MimoError("MiMo response did not include choices[0]")
    message = choices[0].get("message")
    if not isinstance(message, dict):
        raise MimoError("MiMo response did not include a message")
    return message


class MimoClient:
    def __init__(self, config: MimoConfig | None = None):
        self.config = config or MimoConfig.from_env()

    def _post(self, body: dict[str, Any]) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(self.config.retries):
            try:
                response = requests.post(
                    self.config.endpoint,
                    headers={"api-key": self.config.api_key, "Content-Type": "application/json"},
                    json=body,
                    timeout=self.config.timeout,
                )
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, dict):
                    raise MimoError("MiMo returned a non-object JSON response")
                return payload
            except (requests.RequestException, ValueError, MimoError) as exc:
                last_error = exc
                if attempt + 1 < self.config.retries:
                    time.sleep(2 + attempt * 3)
        raise MimoError(f"MiMo request failed after {self.config.retries} attempts: {last_error}") from last_error

    def _file_data_url(self, path: str | Path, fallback_mime: str) -> str:
        media = Path(path).expanduser().resolve()
        if not media.is_file():
            raise MimoError(f"media file not found: {media}")
        mime = mimetypes.guess_type(media.name)[0] or fallback_mime
        value = f"data:{mime};base64," + base64.b64encode(media.read_bytes()).decode("ascii")
        if len(value) > self.config.max_data_url_chars:
            raise MimoError(
                f"local media is too large for an inline request ({len(value)} characters); "
                "compress it or provide an HTTPS URL"
            )
        return value

    def synthesize(
        self,
        text: str,
        output: str | Path,
        *,
        model: str | None = None,
        voice: str | None = None,
        voice_sample: str | Path | None = None,
        style: str = "",
        audio_format: str | None = None,
        optimize_text_preview: bool | None = None,
    ) -> Path:
        destination = Path(output).expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        fmt = (audio_format or destination.suffix.lstrip(".") or "wav").lower()
        messages: list[dict[str, str]] = []
        if style:
            messages.append({"role": "user", "content": style})
        messages.append({"role": "assistant", "content": text})
        selected_model = model or self.config.tts_model
        model_lower = selected_model.lower()
        audio: dict[str, Any] = {"format": fmt}
        if "voiceclone" in model_lower:
            if not voice_sample:
                raise MimoError("MiMo voiceclone requires a voice_sample")
            sample = str(voice_sample)
            audio["voice"] = (
                sample if sample.startswith("data:") else self._file_data_url(sample, "audio/wav")
            )
        elif "voicedesign" in model_lower:
            if not style:
                raise MimoError("MiMo voicedesign requires a non-empty style prompt")
            if optimize_text_preview is not None:
                audio["optimize_text_preview"] = bool(optimize_text_preview)
        else:
            audio["voice"] = voice or self.config.tts_voice
        payload = self._post(
            {
                "model": selected_model,
                "messages": messages,
                "audio": audio,
            }
        )
        audio_data = (_message(payload).get("audio") or {}).get("data")
        if not audio_data:
            raise MimoError("MiMo TTS response did not include message.audio.data")
        try:
            destination.write_bytes(base64.b64decode(audio_data, validate=True))
        except (ValueError, base64.binascii.Error) as exc:
            raise MimoError("MiMo TTS returned invalid base64 audio") from exc
        return destination

    def transcribe(self, audio: str | Path, *, prompt: str = DEFAULT_ASR_PROMPT) -> str:
        data_url = self._file_data_url(audio, "audio/wav")
        payload = self._post(
            {
                "model": self.config.multimodal_model,
                "messages": [{"role": "user", "content": [
                    {"type": "input_audio", "input_audio": {"data": data_url}},
                    {"type": "text", "text": prompt},
                ]}],
                "max_completion_tokens": 2500,
            }
        )
        content = str(_message(payload).get("content") or "").strip()
        if not content:
            raise MimoError("MiMo ASR response was empty")
        return content

    def understand_video(
        self,
        video: str | Path,
        *,
        prompt: str = DEFAULT_VIDEO_PROMPT,
        fps: float = 1.0,
    ) -> str:
        source = str(video)
        url = source if source.startswith(("http://", "https://", "data:")) else self._file_data_url(source, "video/mp4")
        payload = self._post(
            {
                "model": self.config.multimodal_model,
                "messages": [{"role": "user", "content": [
                    {"type": "video_url", "video_url": {"url": url}, "fps": fps, "media_resolution": "default"},
                    {"type": "text", "text": prompt},
                ]}],
                "max_completion_tokens": 3000,
            }
        )
        content = str(_message(payload).get("content") or "").strip()
        if not content:
            raise MimoError("MiMo video-understanding response was empty")
        return content
