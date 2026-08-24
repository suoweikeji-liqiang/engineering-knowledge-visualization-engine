from .audio import _sfx, build_audio
from .core import Point, Timeline
from .icon_patch import IconStudioMixin
from .studio import Studio as BaseStudio


class Studio(IconStudioMixin, BaseStudio):
    pass


__all__ = ["Point", "Studio", "Timeline", "_sfx", "build_audio"]
