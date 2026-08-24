"""Typed renderer lookup with explicit configuration errors."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar


RendererT = TypeVar("RendererT")


class RendererRegistryError(LookupError):
    """Base class for registry configuration and lookup failures."""


class DuplicateRendererError(RendererRegistryError):
    """Raised when an id is registered more than once."""


class UnknownRendererError(RendererRegistryError):
    """Raised when resolving an id that has not been registered."""


class RendererRegistry(Generic[RendererT]):
    """Small deterministic registry intended to be owned per component kind."""

    def __init__(self) -> None:
        self._renderers: dict[str, RendererT] = {}

    def register(self, renderer_id: str, renderer: RendererT) -> None:
        renderer_id = self._validate_id(renderer_id)
        if renderer_id in self._renderers:
            raise DuplicateRendererError(
                f"renderer id already registered: {renderer_id!r}"
            )
        self._renderers[renderer_id] = renderer

    def register_component(self, renderer: RendererT) -> None:
        """Register a component using its public ``renderer_id`` attribute."""

        renderer_id = getattr(renderer, "renderer_id", None)
        if not isinstance(renderer_id, str):
            raise ValueError("renderer must expose a string renderer_id")
        self.register(renderer_id, renderer)

    def resolve(self, renderer_id: str) -> RendererT:
        renderer_id = self._validate_id(renderer_id)
        try:
            return self._renderers[renderer_id]
        except KeyError as exc:
            known = ", ".join(self.ids()) or "<none>"
            raise UnknownRendererError(
                f"unknown renderer id {renderer_id!r}; registered ids: {known}"
            ) from exc

    def ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._renderers))

    def __contains__(self, renderer_id: object) -> bool:
        return renderer_id in self._renderers

    def __len__(self) -> int:
        return len(self._renderers)

    def __iter__(self) -> Iterator[str]:
        return iter(self.ids())

    @staticmethod
    def _validate_id(renderer_id: str) -> str:
        if not isinstance(renderer_id, str) or not renderer_id.strip():
            raise ValueError("renderer id must be a non-empty string")
        if renderer_id != renderer_id.strip():
            raise ValueError("renderer id may not have leading or trailing whitespace")
        return renderer_id
