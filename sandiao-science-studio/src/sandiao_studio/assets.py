from __future__ import annotations

import json
import math
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


class AssetManifestError(ValueError):
    """Raised when a design asset manifest or one of its assets is invalid."""


@dataclass(frozen=True)
class DesignAsset:
    id: str
    type: str
    source: str
    path: Path
    view_box: tuple[float, float, float, float]
    anchors: dict[str, tuple[float, float]]
    variants: tuple[str, ...]
    capabilities: tuple[str, ...]
    layers: tuple[str, ...]


@dataclass(frozen=True)
class AssetManifest:
    source: Path
    asset_root: Path
    schema_version: str
    assets: tuple[DesignAsset, ...]

    def get(self, asset_id: str) -> DesignAsset:
        for asset in self.assets:
            if asset.id == asset_id:
                return asset
        raise KeyError(asset_id)


_ROOT_FIELDS = {"schemaVersion", "assets"}
_CATALOG_ROOT_FIELDS = {"schemaVersion", "manifests"}
_CATALOG_ENTRY_FIELDS = {"namespace", "source"}
_ASSET_FIELDS = {
    "id",
    "type",
    "source",
    "viewBox",
    "anchors",
    "variants",
    "capabilities",
    "layers",
}
_ASSET_ID = re.compile(r"^[a-z][a-z0-9]*(?:[.-][a-z][a-z0-9]*)*$")
_ASSET_TYPE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
_VIEW_BOX_SPLIT = re.compile(r"[\s,]+")
_CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)


class _DuplicateKeyError(ValueError):
    pass


def _json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_manifest(source: Path) -> dict[str, Any]:
    try:
        text = source.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AssetManifestError(f"asset manifest not found: {source}") from exc
    except OSError as exc:
        raise AssetManifestError(f"cannot read asset manifest {source}: {exc}") from exc

    try:
        raw = json.loads(text, object_pairs_hook=_json_object)
    except _DuplicateKeyError as exc:
        raise AssetManifestError(str(exc)) from exc
    except json.JSONDecodeError as exc:
        raise AssetManifestError(
            f"invalid manifest JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(raw, dict):
        raise AssetManifestError("manifest root must be an object")
    return raw


def _reject_unknown_fields(data: dict[str, Any], allowed: set[str], where: str) -> None:
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise AssetManifestError(f"unknown {where} field(s): {', '.join(unknown)}")


def _required(data: dict[str, Any], key: str, where: str) -> Any:
    if key not in data:
        raise AssetManifestError(f"missing {where}.{key}")
    return data[key]


def _string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AssetManifestError(f"{where} must be a non-empty string")
    if value != value.strip():
        raise AssetManifestError(f"{where} must not have leading or trailing whitespace")
    return value


def _number(value: Any, where: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AssetManifestError(f"{where} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise AssetManifestError(f"{where} must be a finite number")
    return result


def _view_box(value: Any, where: str) -> tuple[float, float, float, float]:
    if not isinstance(value, list) or len(value) != 4:
        raise AssetManifestError(f"{where} must be [minX, minY, width, height]")
    result = tuple(_number(item, f"{where}[{index}]") for index, item in enumerate(value))
    if result[2] <= 0 or result[3] <= 0:
        raise AssetManifestError(f"{where} width and height must be greater than zero")
    return result  # type: ignore[return-value]


def _named_list(value: Any, where: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise AssetManifestError(f"{where} must be an array of names")
    names: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        name = _string(item, f"{where}[{index}]")
        if not _NAME.fullmatch(name):
            raise AssetManifestError(
                f"{where}[{index}] has invalid name {name!r}; use letters, digits, '_' or '-'"
            )
        if name in seen:
            raise AssetManifestError(f"duplicate name {name!r} in {where}")
        seen.add(name)
        names.append(name)
    return tuple(names)


def _anchors(
    value: Any, view_box: tuple[float, float, float, float], where: str
) -> dict[str, tuple[float, float]]:
    if not isinstance(value, dict):
        raise AssetManifestError(f"{where} must be an object of [x, y] coordinates")
    min_x, min_y, width, height = view_box
    max_x, max_y = min_x + width, min_y + height
    result: dict[str, tuple[float, float]] = {}
    for name, point in value.items():
        if not _NAME.fullmatch(name):
            raise AssetManifestError(
                f"invalid anchor name {name!r} in {where}; use letters, digits, '_' or '-'"
            )
        if not isinstance(point, list) or len(point) != 2:
            raise AssetManifestError(f"{where}.{name} must be [x, y]")
        x = _number(point[0], f"{where}.{name}[0]")
        y = _number(point[1], f"{where}.{name}[1]")
        if not (min_x <= x <= max_x and min_y <= y <= max_y):
            raise AssetManifestError(
                f"{where}.{name} [{x:g}, {y:g}] is outside viewBox "
                f"[{min_x:g}, {min_y:g}, {width:g}, {height:g}]"
            )
        result[name] = (x, y)
    return result


def _asset_path(source_value: Any, asset_root: Path, where: str) -> tuple[str, Path]:
    value = _string(source_value, where)
    if "\\" in value:
        raise AssetManifestError(f"{where} must use '/' separators")
    relative = PurePosixPath(value)
    if (
        relative.is_absolute()
        or value != relative.as_posix()
        or any(part == ".." for part in relative.parts)
    ):
        raise AssetManifestError(f"{where} must be a normalized relative path inside {asset_root}")

    resolved = (asset_root / Path(*relative.parts)).resolve()
    try:
        resolved.relative_to(asset_root)
    except ValueError as exc:
        raise AssetManifestError(f"{where} escapes asset root {asset_root}: {value}") from exc
    if not resolved.is_file():
        raise AssetManifestError(f"{where} does not exist or is not a file: {resolved}")
    return value, resolved


def _parse_svg_view_box(value: str, path: Path) -> tuple[float, float, float, float]:
    parts = [part for part in _VIEW_BOX_SPLIT.split(value.strip()) if part]
    if len(parts) != 4:
        raise AssetManifestError(f"SVG {path} has invalid viewBox {value!r}")
    try:
        result = tuple(float(part) for part in parts)
    except ValueError as exc:
        raise AssetManifestError(f"SVG {path} has non-numeric viewBox {value!r}") from exc
    if any(not math.isfinite(item) for item in result) or result[2] <= 0 or result[3] <= 0:
        raise AssetManifestError(f"SVG {path} has invalid viewBox {value!r}")
    return result  # type: ignore[return-value]


def _external_reference(value: str) -> str | None:
    stripped = value.strip().strip("'\"")
    if not stripped or stripped.startswith("#"):
        return None
    return stripped


def _validate_css_references(css: str, path: Path) -> None:
    if re.search(r"@import\b", css, re.IGNORECASE):
        raise AssetManifestError(f"SVG {path} contains forbidden CSS @import")
    for match in _CSS_URL.finditer(css):
        reference = _external_reference(match.group(2))
        if reference is not None:
            raise AssetManifestError(
                f"SVG {path} contains forbidden external resource reference: {reference}"
            )


def _validate_svg(
    path: Path,
    expected_view_box: tuple[float, float, float, float],
    declared_layers: tuple[str, ...],
) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise AssetManifestError(f"cannot read SVG {path}: {exc}") from exc
    if re.search(r"<!DOCTYPE|<!ENTITY", text, re.IGNORECASE):
        raise AssetManifestError(f"SVG {path} must not contain DOCTYPE or ENTITY declarations")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise AssetManifestError(f"invalid SVG XML in {path}: {exc}") from exc
    if root.tag.rsplit("}", 1)[-1] != "svg":
        raise AssetManifestError(f"SVG source {path} must have an <svg> root element")

    raw_view_box = root.get("viewBox")
    if raw_view_box is None:
        raise AssetManifestError(f"SVG {path} is missing viewBox")
    actual_view_box = _parse_svg_view_box(raw_view_box, path)
    if any(
        not math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-9)
        for actual, expected in zip(actual_view_box, expected_view_box)
    ):
        raise AssetManifestError(
            f"SVG {path} viewBox {list(actual_view_box)} does not match manifest "
            f"viewBox {list(expected_view_box)}"
        )

    ids: set[str] = set()
    for element in root.iter():
        element_id = element.get("id")
        if element_id:
            if element_id in ids:
                raise AssetManifestError(f"SVG {path} contains duplicate id {element_id!r}")
            ids.add(element_id)
        for attribute, value in element.attrib.items():
            local_name = attribute.rsplit("}", 1)[-1].lower()
            if local_name in {"href", "src"}:
                reference = _external_reference(value)
                if reference is not None:
                    raise AssetManifestError(
                        f"SVG {path} contains forbidden external resource reference: {reference}"
                    )
            if local_name == "style" or "url(" in value.lower():
                _validate_css_references(value, path)
        if element.tag.rsplit("}", 1)[-1].lower() == "style" and element.text:
            _validate_css_references(element.text, path)

    missing_layers = [layer for layer in declared_layers if layer not in ids]
    if missing_layers:
        raise AssetManifestError(
            f"SVG {path} is missing declared layer id(s): {', '.join(missing_layers)}"
        )


def _parse_asset(item: Any, index: int, asset_root: Path) -> DesignAsset:
    where = f"assets[{index}]"
    if not isinstance(item, dict):
        raise AssetManifestError(f"{where} must be an object")
    _reject_unknown_fields(item, _ASSET_FIELDS, where)

    asset_id = _string(_required(item, "id", where), f"{where}.id")
    if not _ASSET_ID.fullmatch(asset_id):
        raise AssetManifestError(
            f"{where}.id has invalid value {asset_id!r}; use lowercase dot/kebab notation"
        )
    asset_type = _string(_required(item, "type", where), f"{where}.type")
    if not _ASSET_TYPE.fullmatch(asset_type):
        raise AssetManifestError(f"{where}.type must use lowercase kebab-case")
    source, path = _asset_path(_required(item, "source", where), asset_root, f"{where}.source")
    view_box = _view_box(_required(item, "viewBox", where), f"{where}.viewBox")
    anchors = _anchors(item.get("anchors", {}), view_box, f"{where}.anchors")
    variants = _named_list(item.get("variants", []), f"{where}.variants")
    capabilities = _named_list(item.get("capabilities", []), f"{where}.capabilities")
    layers = _named_list(item.get("layers", []), f"{where}.layers")

    if path.suffix.lower() == ".svg":
        _validate_svg(path, view_box, layers)
    elif layers:
        raise AssetManifestError(f"{where}.layers may only be declared for SVG assets")

    return DesignAsset(
        id=asset_id,
        type=asset_type,
        source=source,
        path=path,
        view_box=view_box,
        anchors=anchors,
        variants=variants,
        capabilities=capabilities,
        layers=layers,
    )


def load_asset_manifest(
    path: str | Path, *, asset_root: str | Path | None = None
) -> AssetManifest:
    """Load and strictly validate a design asset manifest.

    A manifest in a ``manifests`` directory resolves asset sources against the
    parent of that directory (for example, ``design/``). Other manifests resolve
    sources against their own directory unless ``asset_root`` is supplied.
    """

    source = Path(path).resolve()
    raw = _read_manifest(source)
    _reject_unknown_fields(raw, _ROOT_FIELDS, "root")

    schema_version = _string(_required(raw, "schemaVersion", "root"), "root.schemaVersion")
    if schema_version != "1.0":
        raise AssetManifestError(
            f"unsupported root.schemaVersion {schema_version!r}; expected '1.0'"
        )

    raw_assets = _required(raw, "assets", "root")
    if not isinstance(raw_assets, list):
        raise AssetManifestError("root.assets must be an array")

    if asset_root is None:
        root = source.parent.parent if source.parent.name == "manifests" else source.parent
    else:
        root = Path(asset_root)
    root = root.resolve()
    if not root.is_dir():
        raise AssetManifestError(f"asset root does not exist or is not a directory: {root}")

    assets: list[DesignAsset] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(raw_assets):
        asset = _parse_asset(item, index, root)
        if asset.id in seen_ids:
            raise AssetManifestError(f"duplicate asset id {asset.id!r} at assets[{index}]")
        seen_ids.add(asset.id)
        assets.append(asset)

    return AssetManifest(
        source=source,
        asset_root=root,
        schema_version=schema_version,
        assets=tuple(assets),
    )


def load_asset_catalog(path: str | Path) -> AssetManifest:
    """Load a catalog that composes isolated brand/shared/domain manifests."""

    source = Path(path).resolve()
    raw = _read_manifest(source)
    _reject_unknown_fields(raw, _CATALOG_ROOT_FIELDS, "catalog root")
    schema_version = _string(
        _required(raw, "schemaVersion", "catalog"), "catalog.schemaVersion"
    )
    if schema_version != "1.0":
        raise AssetManifestError(
            f"unsupported catalog.schemaVersion {schema_version!r}; expected '1.0'"
        )
    entries = _required(raw, "manifests", "catalog")
    if not isinstance(entries, list) or not entries:
        raise AssetManifestError("catalog.manifests must be a non-empty array")

    catalog_root = source.parent.parent if source.parent.name == "manifests" else source.parent
    catalog_root = catalog_root.resolve()
    assets: list[DesignAsset] = []
    seen_ids: set[str] = set()
    seen_namespaces: set[str] = set()
    for index, value in enumerate(entries):
        where = f"catalog.manifests[{index}]"
        if not isinstance(value, dict):
            raise AssetManifestError(f"{where} must be an object")
        _reject_unknown_fields(value, _CATALOG_ENTRY_FIELDS, where)
        namespace = _string(_required(value, "namespace", where), f"{where}.namespace")
        if not _ASSET_ID.fullmatch(namespace):
            raise AssetManifestError(f"{where}.namespace must use lowercase dot/kebab notation")
        if namespace in seen_namespaces:
            raise AssetManifestError(f"duplicate catalog namespace {namespace!r}")
        seen_namespaces.add(namespace)
        relative, manifest_path = _asset_path(
            _required(value, "source", where), catalog_root, f"{where}.source"
        )
        if Path(relative).suffix.lower() != ".json":
            raise AssetManifestError(f"{where}.source must reference a JSON manifest")
        manifest = load_asset_manifest(manifest_path)
        for asset in manifest.assets:
            if not asset.id.startswith(namespace + "."):
                raise AssetManifestError(
                    f"asset {asset.id!r} from {relative} escapes namespace {namespace!r}"
                )
            if asset.id in seen_ids:
                raise AssetManifestError(f"duplicate asset id across catalog: {asset.id!r}")
            seen_ids.add(asset.id)
            assets.append(asset)

    return AssetManifest(
        source=source,
        asset_root=catalog_root,
        schema_version=schema_version,
        assets=tuple(assets),
    )


def load_asset_source(path: str | Path, *, asset_root: str | Path | None = None) -> AssetManifest:
    """Load either one package manifest or a composed asset catalog."""

    source = Path(path).resolve()
    raw = _read_manifest(source)
    if "assets" in raw:
        return load_asset_manifest(source, asset_root=asset_root)
    if "manifests" in raw:
        if asset_root is not None:
            raise AssetManifestError("asset_root is not supported for asset catalogs")
        return load_asset_catalog(source)
    raise AssetManifestError("asset source must contain either root.assets or root.manifests")
