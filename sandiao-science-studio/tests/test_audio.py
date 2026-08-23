from __future__ import annotations

import numpy as np

from sandiao_studio.audio import (
    RATE,
    SILENCE_TRIM_LEADING_SECONDS,
    SILENCE_TRIM_TRAILING_SECONDS,
    _trim_silence,
)


def test_trim_silence_removes_tts_container_padding() -> None:
    leading = np.zeros(round(0.8 * RATE), dtype=np.float32)
    speech = np.full(round(0.5 * RATE), 0.2, dtype=np.float32)
    trailing = np.zeros(round(1.1 * RATE), dtype=np.float32)

    trimmed = _trim_silence(np.concatenate([leading, speech, trailing]))

    expected = round(
        (SILENCE_TRIM_LEADING_SECONDS + 0.5 + SILENCE_TRIM_TRAILING_SECONDS) * RATE
    )
    assert abs(len(trimmed) - expected) <= 2


def test_trim_silence_does_not_destroy_a_silent_clip() -> None:
    silent = np.zeros(round(0.25 * RATE), dtype=np.float32)

    assert np.array_equal(_trim_silence(silent), silent)
