from __future__ import annotations

import os
import re
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_dotenv(path: str | Path | None = None) -> Path | None:
    """Load a small, dependency-free .env file without overriding the shell."""
    env_path = Path(path).expanduser() if path else project_root() / ".env"
    if not env_path.exists():
        return None
    for line in env_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\s*(?:export\s+)?([A-Z_][A-Z0-9_]*)\s*=\s*(.*)", line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ.setdefault(key, value)
    return env_path
