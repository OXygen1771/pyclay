"""Describes data passed by clay to various callbacks."""

from dataclasses import dataclass

from pyclay._clay import _types as ct
from pyclay._clay._enums import (
    Clay_PointerDataInteractionState,
)
from pyclay.configs import (
    BoundingBox,
    ClipConfig,
    Dimensions,
    Vector2,
)


@dataclass(frozen=True)
class ScrollContainerData:
    """Represents the current internal state of a scrolling element."""

    scroll_position: Vector2
    scroll_container_dimensions: Dimensions
    content_dimensions: Dimensions
    config: ClipConfig
    found: bool

    @classmethod
    def from_ctypes(cls, c: ct.Clay_ScrollContainerData) -> ScrollContainerData:
        """Convert the underlying ctypes structure to the Python dataclass."""
        return cls(
            scroll_position=Vector2.from_ctypes(c.scrollPosition.contents),
            scroll_container_dimensions=Dimensions.from_ctypes(
                c.scrollContainerDimensions,
            ),
            content_dimensions=Dimensions.from_ctypes(c.contentDimensions),
            config=ClipConfig.from_ctypes(c.config),
            found=c.found,
        )


@dataclass(frozen=True)
class ElementData:
    """Represents the current internal state of an element."""

    bounding_box: BoundingBox
    found: bool

    @classmethod
    def from_ctypes(cls, c: ct.Clay_ElementData) -> ElementData:
        """Convert the underlying ctypes structure to the Python dataclass."""
        return cls(bounding_box=BoundingBox.from_ctypes(c.boundingBox), found=c.found)


@dataclass(frozen=True)
class PointerData:
    """Represents the current internal state of an element."""

    position: Vector2
    state: Clay_PointerDataInteractionState

    @classmethod
    def from_ctypes(cls, c: ct.Clay_PointerData) -> PointerData:
        """Convert the underlying ctypes structure to the Python dataclass."""
        return cls(
            position=Vector2.from_ctypes(c.position),
            state=Clay_PointerDataInteractionState(c.state),
        )
