from __future__ import annotations

import json
from pathlib import Path

import pytest

from sandiao_studio.assets import AssetManifestError, load_asset_manifest, load_asset_source


FIXTURE = Path(__file__).parent / "fixtures/assets/manifests/design-assets.json"
PROJECT_DIR = Path(__file__).resolve().parents[1]


def _write_svg(
    path: Path,
    body: str = '<g id="root"/>',
    view_box: str | None = "0 0 100 200",
) -> None:
    view_box_attribute = "" if view_box is None else f' viewBox="{view_box}"'
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg"{view_box_attribute}>{body}</svg>',
        encoding="utf-8",
    )


def _write_manifest(root: Path, assets: list[dict[str, object]], version: str = "1.0") -> Path:
    manifests = root / "manifests"
    manifests.mkdir(exist_ok=True)
    path = manifests / "design-assets.json"
    path.write_text(
        json.dumps({"schemaVersion": version, "assets": assets}, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def _asset(source: str = "asset.svg", **changes: object) -> dict[str, object]:
    item: dict[str, object] = {
        "id": "character.xiaoming.pose.point",
        "type": "character-pose",
        "source": source,
        "viewBox": [0, 0, 100, 200],
        "anchors": {"feet": [50, 200], "mouth": [50, 40]},
        "variants": ["default"],
        "capabilities": ["lipSync"],
        "layers": ["root"],
    }
    item.update(changes)
    return item


def test_load_valid_manifest_and_lookup() -> None:
    manifest = load_asset_manifest(FIXTURE)

    assert manifest.schema_version == "1.0"
    assert manifest.asset_root == FIXTURE.parent.parent.resolve()
    assert len(manifest.assets) == 1
    asset = manifest.get("prop.thermometer.default")
    assert asset.view_box == (0.0, 0.0, 64.0, 96.0)
    assert asset.anchors["center"] == (32.0, 48.0)
    assert asset.layers == ("root", "body", "signal")
    assert asset.path.is_file()


def test_optional_collections_default_to_empty(tmp_path: Path) -> None:
    _write_svg(tmp_path / "asset.svg")
    asset = _asset()
    for field in ("anchors", "variants", "capabilities", "layers"):
        asset.pop(field)
    manifest = load_asset_manifest(_write_manifest(tmp_path, [asset]))

    loaded = manifest.assets[0]
    assert loaded.anchors == {}
    assert loaded.variants == ()
    assert loaded.capabilities == ()
    assert loaded.layers == ()


@pytest.mark.parametrize("version", ["1", "1.1", "2.0"])
def test_rejects_unsupported_schema_version(tmp_path: Path, version: str) -> None:
    with pytest.raises(AssetManifestError, match="unsupported.*schemaVersion"):
        load_asset_manifest(_write_manifest(tmp_path, [], version=version))


def test_rejects_duplicate_asset_id(tmp_path: Path) -> None:
    _write_svg(tmp_path / "asset.svg")
    with pytest.raises(AssetManifestError, match="duplicate asset id"):
        load_asset_manifest(_write_manifest(tmp_path, [_asset(), _asset()]))


@pytest.mark.parametrize(
    "source",
    ["../outside.svg", "/tmp/outside.svg", "folder\\asset.svg", "./asset.svg", "folder//asset.svg"],
)
def test_rejects_unsafe_source_path(tmp_path: Path, source: str) -> None:
    with pytest.raises(AssetManifestError, match="source"):
        load_asset_manifest(_write_manifest(tmp_path, [_asset(source)]))


def test_rejects_symlink_that_escapes_asset_root(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-outside.svg"
    _write_svg(outside)
    (tmp_path / "asset.svg").symlink_to(outside)
    try:
        with pytest.raises(AssetManifestError, match="escapes asset root"):
            load_asset_manifest(_write_manifest(tmp_path, [_asset()]))
    finally:
        outside.unlink()


def test_rejects_missing_source(tmp_path: Path) -> None:
    with pytest.raises(AssetManifestError, match="does not exist"):
        load_asset_manifest(_write_manifest(tmp_path, [_asset()]))


@pytest.mark.parametrize(
    ("view_box", "message"),
    [
        ([0, 0, 0, 200], "greater than zero"),
        ([0, 0, 100], "must be"),
        ([0, 0, True, 1], "finite number"),
    ],
)
def test_rejects_invalid_manifest_view_box(
    tmp_path: Path, view_box: list[object], message: str
) -> None:
    _write_svg(tmp_path / "asset.svg")
    with pytest.raises(AssetManifestError, match=message):
        load_asset_manifest(_write_manifest(tmp_path, [_asset(viewBox=view_box)]))


def test_rejects_anchor_outside_view_box(tmp_path: Path) -> None:
    _write_svg(tmp_path / "asset.svg")
    with pytest.raises(AssetManifestError, match="outside viewBox"):
        load_asset_manifest(
            _write_manifest(tmp_path, [_asset(anchors={"feet": [50, 201]})])
        )


def test_requires_svg_view_box(tmp_path: Path) -> None:
    _write_svg(tmp_path / "asset.svg", view_box=None)
    with pytest.raises(AssetManifestError, match="missing viewBox"):
        load_asset_manifest(_write_manifest(tmp_path, [_asset()]))


def test_requires_svg_and_manifest_view_boxes_to_match(tmp_path: Path) -> None:
    _write_svg(tmp_path / "asset.svg", view_box="0 0 120 200")
    with pytest.raises(AssetManifestError, match="does not match manifest"):
        load_asset_manifest(_write_manifest(tmp_path, [_asset()]))


@pytest.mark.parametrize(
    "body",
    [
        '<image href="https://example.com/image.png"/>',
        '<script src="https://example.com/runtime.js"/>',
        '<style>.shape { fill: url(https://example.com/pattern.svg); }</style>',
        '<use href="other.svg#shape"/>',
    ],
)
def test_rejects_svg_external_dependencies(tmp_path: Path, body: str) -> None:
    _write_svg(tmp_path / "asset.svg", body=body)
    with pytest.raises(AssetManifestError, match="external resource"):
        load_asset_manifest(_write_manifest(tmp_path, [_asset(layers=[])]))


def test_allows_internal_svg_references(tmp_path: Path) -> None:
    _write_svg(
        tmp_path / "asset.svg",
        body='<defs><path id="shape" d="M0 0h1v1z"/></defs><use id="root" href="#shape"/>',
    )
    manifest = load_asset_manifest(_write_manifest(tmp_path, [_asset()]))
    assert manifest.assets[0].layers == ("root",)


def test_rejects_missing_declared_svg_layer(tmp_path: Path) -> None:
    _write_svg(tmp_path / "asset.svg")
    with pytest.raises(AssetManifestError, match="missing declared layer"):
        load_asset_manifest(_write_manifest(tmp_path, [_asset(layers=["mouth"])]))


def test_rejects_layers_for_non_svg_asset(tmp_path: Path) -> None:
    (tmp_path / "asset.png").write_bytes(b"not inspected by the manifest loader")
    with pytest.raises(AssetManifestError, match="only be declared for SVG"):
        load_asset_manifest(_write_manifest(tmp_path, [_asset("asset.png")]))


def test_rejects_unknown_fields(tmp_path: Path) -> None:
    _write_svg(tmp_path / "asset.svg")
    with pytest.raises(AssetManifestError, match=r"unknown assets\[0\] field"):
        load_asset_manifest(_write_manifest(tmp_path, [_asset(description="not in v1")]))


def test_catalog_composes_namespaced_package_manifests(tmp_path: Path) -> None:
    package = tmp_path / "assets" / "brand"
    package.mkdir(parents=True)
    _write_svg(package / "character.svg")
    (package / "manifest.json").write_text(
        json.dumps(
            {
                "schemaVersion": "1.0",
                "assets": [
                    _asset(
                        "character.svg",
                        id="brand.character.host.pose.idle",
                    )
                ],
            }
        ),
        encoding="utf-8",
    )
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    catalog = manifests / "design-assets.json"
    catalog.write_text(
        json.dumps(
            {
                "schemaVersion": "1.0",
                "manifests": [
                    {"namespace": "brand", "source": "assets/brand/manifest.json"}
                ],
            }
        ),
        encoding="utf-8",
    )

    loaded = load_asset_source(catalog)

    assert loaded.source == catalog.resolve()
    assert loaded.get("brand.character.host.pose.idle").path == (package / "character.svg").resolve()


def test_catalog_rejects_asset_outside_declared_namespace(tmp_path: Path) -> None:
    package = tmp_path / "assets" / "brand"
    package.mkdir(parents=True)
    _write_svg(package / "character.svg")
    (package / "manifest.json").write_text(
        json.dumps({"schemaVersion": "1.0", "assets": [_asset("character.svg")]}),
        encoding="utf-8",
    )
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    catalog = manifests / "design-assets.json"
    catalog.write_text(
        json.dumps(
            {
                "schemaVersion": "1.0",
                "manifests": [
                    {"namespace": "brand", "source": "assets/brand/manifest.json"}
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(AssetManifestError, match="escapes namespace"):
        load_asset_source(catalog)


def test_ai_models_domain_pack_is_complete_and_composable() -> None:
    package = load_asset_manifest(
        PROJECT_DIR / "design/assets/domains/ai-models/manifest.json"
    )
    catalog = load_asset_source(PROJECT_DIR / "design/manifests/design-assets.json")

    assert len(package.assets) == 21
    assert {asset.type for asset in package.assets} == {
        "background",
        "component",
        "diagram",
    }
    transformer = package.get("domain.ai-models.component.transformer-block")
    assert "attention-slot" in transformer.layers
    assert transformer.capabilities == ("animatable", "tintable")
    rag = catalog.get("domain.ai-models.diagram.rag-pipeline")
    assert "retrieval-stage" in rag.layers
    assert rag.capabilities == ("stateful", "dataBindable")
