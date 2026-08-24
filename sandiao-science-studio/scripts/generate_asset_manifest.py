#!/usr/bin/env python3
"""Generate isolated brand/shared/domain manifests and their composition catalog."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
DESIGN_DIR = PROJECT_DIR / "design"
ASSETS_DIR = DESIGN_DIR / "assets"
CATALOG_FILE = DESIGN_DIR / "manifests" / "design-assets.json"
VIEW_BOX_SPLIT = re.compile(r"[\s,]+")

CHARACTER_LAYERS = (
    "root", "legs", "leg_left", "leg_right", "torso", "arms", "arm_left",
    "arm_right", "hand_left", "hand_right", "head", "face", "eye_left",
    "eye_right", "mouth", "prop_anchor",
)


def _slug(value: str) -> str:
    parts = [part for part in re.split(r"[_\s]+", value.lower()) if part]
    if not parts:
        raise ValueError(f"cannot derive asset id from {value!r}")
    result = parts[0]
    for part in parts[1:]:
        result += part if part[0].isdigit() else f"-{part}"
    return result


def _svg_metadata(path: Path) -> tuple[list[float | int], list[str]]:
    root = ET.parse(path).getroot()
    raw = root.get("viewBox")
    if raw is None:
        raise ValueError(f"SVG is missing viewBox: {path}")
    parts = [part for part in VIEW_BOX_SPLIT.split(raw.strip()) if part]
    if len(parts) != 4:
        raise ValueError(f"invalid SVG viewBox in {path}: {raw!r}")
    numbers = [float(part) for part in parts]
    view_box: list[float | int] = [int(n) if n.is_integer() else n for n in numbers]
    ids = [element.get("id") for element in root.iter() if element.get("id")]
    return view_box, ids  # type: ignore[return-value]


def _character_asset(path: Path, package_root: Path) -> dict[str, object]:
    relative = path.relative_to(package_root)
    _, character, collection, filename = relative.parts
    kind = {
        "turnaround": "turnaround", "expressions": "expression",
        "mouths": "mouth", "poses": "pose",
    }[collection]
    view_box, ids = _svg_metadata(path)
    return {
        "id": f"brand.character.{character}.{kind}.{_slug(Path(filename).stem)}",
        "type": f"character-{kind}",
        "source": relative.as_posix(),
        "viewBox": view_box,
        "anchors": {
            "feet": [256, 700], "center": [256, 384], "head": [256, 180],
            "mouth": [256, 245 if character == "xiaoming" else 240],
            "lookAt": [256, 190], "propAnchor": [256, 495],
        },
        "variants": ["default"],
        "capabilities": ["lipSync", "lookAt", "propAttach"],
        "layers": [layer for layer in CHARACTER_LAYERS if layer in ids],
    }


def _background_asset(
    path: Path, package_root: Path, namespace: str
) -> dict[str, object]:
    relative = path.relative_to(package_root)
    _, scene, filename = relative.parts
    stem = Path(filename).stem
    view_box, _ = _svg_metadata(path)
    min_x, min_y, width, height = view_box
    variants = ["vertical" if "9x16" in stem else "landscape"]
    if "night" in stem or "dark" in stem:
        variants.append("night")
    if stem.startswith(("background_", "midground_", "foreground_")):
        variants.append("layer")
    return {
        "id": f"{namespace}.background.{_slug(scene)}.{_slug(stem)}",
        "type": "background-layer" if "layer" in variants else "background",
        "source": relative.as_posix(),
        "viewBox": view_box,
        "anchors": {
            "center": [min_x + width / 2, min_y + height / 2],
            "horizon": [min_x + width / 2, min_y + height * 0.78],
        },
        "variants": variants,
        "capabilities": [],
        "layers": [],
    }


def _component_asset(
    path: Path,
    package_root: Path,
    namespace: str,
    family: str,
    filename_prefix: str,
) -> dict[str, object]:
    relative = path.relative_to(package_root)
    stem = path.stem
    view_box, ids = _svg_metadata(path)
    min_x, min_y, width, height = view_box
    root_id = stem if stem in ids else None
    layers = ids if family in {"diagram", "component"} else ([root_id] if root_id else [])
    capabilities = {
        "diagram": ["stateful", "dataBindable"],
        "component": ["animatable", "tintable"],
        "symbol": ["tintable"],
    }.get(family, [])
    return {
        "id": f"{namespace}.{family}.{_slug(stem.removeprefix(filename_prefix))}",
        "type": family,
        "source": relative.as_posix(),
        "viewBox": view_box,
        "anchors": {
            "center": [min_x + width / 2, min_y + height / 2],
            "label": [min_x + width / 2, min_y + height * 0.15],
        },
        "variants": ["default"],
        "capabilities": capabilities,
        "layers": layers,
    }


def _write_manifest(root: Path, assets: list[dict[str, object]]) -> Path:
    path = root / "manifest.json"
    path.write_text(
        json.dumps({"schemaVersion": "1.0", "assets": assets}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def build_manifests() -> dict[str, int]:
    legacy_roots = [
        DESIGN_DIR / "characters", DESIGN_DIR / "backgrounds",
        DESIGN_DIR / "props", DESIGN_DIR / "diagrams",
    ]
    found_legacy = [str(path) for path in legacy_roots if path.exists()]
    if found_legacy:
        raise RuntimeError(
            "legacy global asset roots are forbidden; move them into brand/shared/domains: "
            + ", ".join(found_legacy)
        )
    brand_root = ASSETS_DIR / "brand"
    shared_root = ASSETS_DIR / "shared"
    hvac_root = ASSETS_DIR / "domains" / "hvac"
    ai_models_root = ASSETS_DIR / "domains" / "ai-models"

    brand: list[dict[str, object]] = []
    for path in sorted((brand_root / "characters").rglob("*.svg")):
        brand.append(_character_asset(path, brand_root))
    for path in sorted((brand_root / "backgrounds").rglob("*.svg")):
        brand.append(_background_asset(path, brand_root, "brand"))

    shared: list[dict[str, object]] = []
    for path in sorted((shared_root / "backgrounds").rglob("*.svg")):
        shared.append(_background_asset(path, shared_root, "shared"))
    for path in sorted((shared_root / "symbols").glob("*.svg")):
        shared.append(_component_asset(path, shared_root, "shared", "symbol", "symbol-"))
    for path in sorted((shared_root / "diagrams").glob("*.svg")):
        shared.append(_component_asset(path, shared_root, "shared", "diagram", "diagram-"))

    hvac: list[dict[str, object]] = []
    for path in sorted((hvac_root / "backgrounds").rglob("*.svg")):
        hvac.append(_background_asset(path, hvac_root, "domain.hvac"))
    for path in sorted((hvac_root / "props").glob("*.svg")):
        hvac.append(_component_asset(path, hvac_root, "domain.hvac", "prop", "hvac-"))

    ai_models: list[dict[str, object]] = []
    for path in sorted((ai_models_root / "backgrounds").rglob("*.svg")):
        ai_models.append(_background_asset(path, ai_models_root, "domain.ai-models"))
    for path in sorted((ai_models_root / "components").glob("*.svg")):
        ai_models.append(
            _component_asset(
                path, ai_models_root, "domain.ai-models", "component", "ai-"
            )
        )
    for path in sorted((ai_models_root / "diagrams").glob("*.svg")):
        ai_models.append(
            _component_asset(
                path, ai_models_root, "domain.ai-models", "diagram", "ai-"
            )
        )

    _write_manifest(brand_root, brand)
    _write_manifest(shared_root, shared)
    _write_manifest(hvac_root, hvac)
    _write_manifest(ai_models_root, ai_models)
    catalog = {
        "schemaVersion": "1.0",
        "manifests": [
            {"namespace": "brand", "source": "assets/brand/manifest.json"},
            {"namespace": "shared", "source": "assets/shared/manifest.json"},
            {"namespace": "domain.hvac", "source": "assets/domains/hvac/manifest.json"},
            {
                "namespace": "domain.ai-models",
                "source": "assets/domains/ai-models/manifest.json",
            },
        ],
    }
    CATALOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_FILE.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "brand": len(brand),
        "shared": len(shared),
        "domain.hvac": len(hvac),
        "domain.ai-models": len(ai_models),
    }


if __name__ == "__main__":
    counts = build_manifests()
    print(f"Generated {CATALOG_FILE}: {counts} ({sum(counts.values())} assets)")
