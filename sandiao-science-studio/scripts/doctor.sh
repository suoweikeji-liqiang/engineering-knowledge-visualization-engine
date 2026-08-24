#!/usr/bin/env bash
set -euo pipefail
missing=0
for command in python ffmpeg; do
  if command -v "$command" >/dev/null 2>&1; then
    printf 'OK   %s: %s\n' "$command" "$(command -v "$command")"
  else
    printf 'MISS %s\n' "$command"
    missing=1
  fi
done
if command -v espeak-ng >/dev/null 2>&1 || command -v espeak >/dev/null 2>&1; then
  printf 'OK   TTS: espeak available\n'
else
  printf 'WARN TTS: espeak/espeak-ng not found; video can render without narration\n'
fi
exit "$missing"
