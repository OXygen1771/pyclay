"""Describes data passed by clay to various callbacks."""

from dataclasses import dataclass
from typing import NamedTuple

from pyclay._clay import _types as ct
from pyclay._clay._enums import (
    Clay_PointerDataInteractionState,
    Clay_TransitionProperty,
    Clay_TransitionState,
)
from pyclay.configs import (
    BorderWidth,
    ClipConfig,
    Color,
    Dimensions,
    Vector2,
)


class BoundingBox(NamedTuple):
    """A rectangle representing the bounding box of an element.

    The x and y coordinates represent the top-left corner of the rectangle.

    It is calculated by Clay.
    """

    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0

    def to_ctypes(self) -> ct.Clay_BoundingBox:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_BoundingBox(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
        )

    @classmethod
    def from_ctypes(cls, c: ct.Clay_BoundingBox) -> BoundingBox:
        """Convert the underlying ctypes structure to the config."""
        return cls(x=c.x, y=c.y, width=c.width, height=c.height)


@dataclass(frozen=True)
class TransitionData:
    """Represents element properties that are modifiable in a transition."""

    bounding_box: BoundingBox
    background_color: Color
    overlay_color: Color
    border_color: Color
    border_width: BorderWidth

    def to_ctypes(self) -> ct.Clay_TransitionData:
        """Convert the dataclass to the underlying ctypes structure."""
        return ct.Clay_TransitionData(
            boundingBox=self.bounding_box.to_ctypes(),
            backgroundColor=self.background_color.to_ctypes(),
            overlayColor=self.overlay_color.to_ctypes(),
            borderColor=self.border_color.to_ctypes(),
            borderWidth=self.border_width.to_ctypes(),
        )

    @classmethod
    def from_ctypes(cls, c: ct.Clay_TransitionData) -> TransitionData:
        """Convert the underlying ctypes structure to the Python dataclass."""
        return cls(
            bounding_box=BoundingBox.from_ctypes(c.boundingBox),
            background_color=Color.from_ctypes(c.backgroundColor),
            overlay_color=Color.from_ctypes(c.overlayColor),
            border_color=Color.from_ctypes(c.borderColor),
            border_width=BorderWidth.from_ctypes(c.borderWidth),
        )


@dataclass(frozen=True)
class TransitionCallbackArgs:
    """Arguments passed to a transition callback."""

    state: Clay_TransitionState
    initial: TransitionData
    current: TransitionData
    target: TransitionData
    elapsed_time: float
    duration: float
    properties: Clay_TransitionProperty

    @classmethod
    def from_ctypes(
        cls,
        c: ct.Clay_TransitionCallbackArguments,
    ) -> TransitionCallbackArgs:
        """Convert the underlying ctypes structure to the Python dataclass."""
        return cls(
            state=Clay_TransitionState(c.transitionState),
            initial=TransitionData.from_ctypes(c.initial),
            # this is a pointer to Clay_TransitionData
            current=TransitionData.from_ctypes(c.current.contents),  # ty:ignore[unresolved-attribute]
            target=TransitionData.from_ctypes(c.target),
            elapsed_time=c.elapsedTime,
            duration=c.duration,
            properties=Clay_TransitionProperty(c.properties),
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
