from __future__ import annotations

import json
from pathlib import Path

from sandiao_studio.cli import main


def test_migrate_story_command_writes_v2_without_overwriting_source(tmp_path: Path) -> None:
    source = Path("stories/ac-16c.json")
    legacy = json.loads(source.read_text(encoding="utf-8"))
    local_source = tmp_path / "story.json"
    local_source.write_text(json.dumps(legacy, ensure_ascii=False), encoding="utf-8")

    assert main(["migrate-story", str(local_source)]) == 0

    output = tmp_path / "story.v2.json"
    assert json.loads(output.read_text(encoding="utf-8"))["schemaVersion"] == "2.0"
    assert "schemaVersion" not in json.loads(local_source.read_text(encoding="utf-8"))
    assert main(["migrate-story", str(local_source)]) == 5


def test_validate_assets_command_accepts_fixture() -> None:
    manifest = Path("tests/fixtures/assets/manifests/design-assets.json")
    assert main(["validate-assets", str(manifest)]) == 0


def test_validate_assets_command_reports_missing_manifest(tmp_path: Path) -> None:
    assert main(["validate-assets", str(tmp_path / "missing.json")]) == 4
