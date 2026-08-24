# Layout Engine

`sandiao_studio.layout` provides deterministic safe regions for headlines, diagrams, characters and subtitles before renderer-specific drawing starts.

The default engine supports landscape and portrait canvases, zero to two characters, optional diagrams, optional headlines and zero to three subtitle lines. Portrait output is reflowed into vertical diagram and character stages; it is not a crop of the landscape composition.

All regions are expressed as pixel `Rect` values and can be normalized for renderer-independent manifests. `LayoutEngine.validate()` rejects regions outside the safe area and collisions among exclusive regions.

These defaults are intentionally style-neutral. When the visual design system is delivered, its manifest may provide ratio overrides while retaining the same request, plan and validation model.
