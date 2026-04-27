"""Clay element configs.

These are a wrapper around actual Clay structures.
Simpler types are represented as NamedTuple, the library might also accept plain
Python tuples instead of NamedTuple in the future.
More complex types are represented as dataclasses and support caching to avoid
constantly recreating Clay C structures.
"""

import ctypes
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, NamedTuple

from pyclay._clay import _types as ct
from pyclay._clay._enums import (
    Clay__SizingType,
    Clay_ExitTransitionSiblingOrdering,
    Clay_FloatingAttachPointType,
    Clay_FloatingAttachToElement,
    Clay_FloatingClipToElement,
    Clay_LayoutAlignmentX,
    Clay_LayoutAlignmentY,
    Clay_LayoutDirection,
    Clay_PointerCaptureMode,
    Clay_TextAlignment,
    Clay_TextElementConfigWrapMode,
    Clay_TransitionEnterTriggerType,
    Clay_TransitionExitTriggerType,
    Clay_TransitionInteractionHandlingType,
    Clay_TransitionProperty,
    Clay_TransitionState,
)


class Dimensions(NamedTuple):
    """Represents dimensions of an object.

    Dimensions cannot be negative.
    """

    width: float = 0
    height: float = 0

    def to_ctypes(self) -> ct.Clay_Dimensions:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_Dimensions(width=self.width, height=self.height)

    @classmethod
    def from_ctypes(cls, c: ct.Clay_Dimensions) -> Dimensions:
        """Convert the underlying ctypes structure to the config."""
        return cls(width=c.width, height=c.height)


class Vector2(NamedTuple):
    """Represents a two-dimensional vector."""

    x: float = 0
    y: float = 0

    def to_ctypes(self) -> ct.Clay_Vector2:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_Vector2(x=self.x, y=self.y)

    @classmethod
    def from_ctypes(cls, c: ct.Clay_Vector2) -> Vector2:
        """Convert the underlying ctypes structure to the config."""
        return cls(x=c.x, y=c.y)


class Color(NamedTuple):
    """Represents a color in RGBA format.

    These values are passed directly to the renderer, so the actual meaning of the
    fields is up to implementation.
    Note that when using debug tools, internal colors are represented as colors in the
    range 0..255.
    """

    r: float = 0
    g: float = 0
    b: float = 0
    a: float = 0

    def to_ctypes(self) -> ct.Clay_Color:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_Color(r=self.r, g=self.g, b=self.b, a=self.a)

    @classmethod
    def from_ctypes(cls, c: ct.Clay_Color) -> Color:
        """Convert the underlying ctypes structure to the config."""
        return cls(r=c.r, g=c.g, b=c.b, a=c.a)


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


class CornerRadius(NamedTuple):
    """Radius in pixels for the arc of rectangle corners."""

    top_left: float = 0
    top_right: float = 0
    bottom_left: float = 0
    bottom_right: float = 0

    def to_ctypes(self) -> ct.Clay_CornerRadius:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_CornerRadius(
            topLeft=self.top_left,
            topRight=self.top_right,
            bottomLeft=self.bottom_left,
            bottomRight=self.bottom_right,
        )

    @classmethod
    def from_ctypes(cls, c: ct.Clay_CornerRadius) -> CornerRadius:
        """Convert the underlying ctypes structure to the config."""
        return cls(
            top_left=c.topLeft,
            top_right=c.topRight,
            bottom_left=c.bottomLeft,
            bottom_right=c.bottomRight,
        )


class ChildAlignment(NamedTuple):
    """Controls the alignment of children relative to the parent container."""

    x: Clay_LayoutAlignmentX = Clay_LayoutAlignmentX.CLAY_ALIGN_X_LEFT
    y: Clay_LayoutAlignmentY = Clay_LayoutAlignmentY.CLAY_ALIGN_Y_LEFT

    def to_ctypes(self) -> ct.Clay_ChildAlignment:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_ChildAlignment(x=self.x, y=self.y)

    @classmethod
    def from_ctypes(cls, c: ct.Clay_ChildAlignment) -> ChildAlignment:
        """Convert the underlying ctypes structure to the config."""
        return cls(x=c.x, y=c.y)


class SizingMinMax(NamedTuple):
    """Controls the minimum and maximum size of an element in pixels."""

    min: float = 0
    max: float = float("inf")

    def to_ctypes(self) -> ct.Clay_SizingMinMax:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_SizingMinMax(min=self.min, max=self.max)

    @classmethod
    def from_ctypes(cls, c: ct.Clay_SizingMinMax) -> SizingMinMax:
        """Convert the underlying ctypes structure to the config."""
        return cls(min=c.min, max=c.max)


@dataclass
class SizingAxis:
    """Controls the minimum and maximum size of an element in pixels."""

    type: Clay__SizingType = Clay__SizingType.CLAY__SIZING_TYPE_FIT
    # union: either size or percent
    size: SizingMinMax | None = None
    percent: float | None = None

    _cached_ctypes: ct.Clay_SizingAxis | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )
    _hash: int | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def _compute_hash(self) -> int:
        return hash((self.type, self.size, self.percent))

    def to_ctypes(self) -> ct.Clay_SizingAxis:
        """Convert the config to the underlying ctypes structure."""
        cur_hash: int = self._compute_hash()
        if self._hash != cur_hash or self._cached_ctypes is None:
            c_axis: ct.Clay_SizingAxis = ct.Clay_SizingAxis(
                type=self.type,
            )
            if self.type != Clay__SizingType.CLAY__SIZING_TYPE_PERCENT:
                if self.size:
                    c_axis.size.minMax = self.size.to_ctypes()
            else:
                c_axis.size.percent = self.percent or 0.0

            self._cached_ctypes = c_axis
            self._hash = cur_hash
        return self._cached_ctypes

    @classmethod
    def fit(cls, min: float = 0, max: float = float("inf")) -> SizingAxis:  # noqa: A002
        """Create a SizingAxis with FIT sizing type and specified limit sizes."""
        return cls(
            type=Clay__SizingType.CLAY__SIZING_TYPE_FIT,
            size=SizingMinMax(min, max),
        )

    @classmethod
    def grow(cls, min: float = 0, max: float = float("inf")) -> SizingAxis:  # noqa: A002
        """Create a SizingAxis with GROW sizing type and specified limit sizes."""
        return cls(
            type=Clay__SizingType.CLAY__SIZING_TYPE_GROW,
            size=SizingMinMax(min, max),
        )

    @classmethod
    def with_percent(cls, val: float) -> SizingAxis:
        """Create a SizingAxis with specified percent."""
        return cls(
            type=Clay__SizingType.CLAY__SIZING_TYPE_PERCENT,
            percent=val,
        )

    @classmethod
    def fixed(cls, val: float) -> SizingAxis:
        """Create a SizingAxis with FIXED sizing type and specified size."""
        return cls(
            type=Clay__SizingType.CLAY__SIZING_TYPE_FIXED,
            size=SizingMinMax(val, val),
        )


@dataclass
class Sizing:
    """Controls the minimum and maximum size of an element in pixels."""

    width: SizingAxis = field(default_factory=SizingAxis)
    height: SizingAxis = field(default_factory=SizingAxis)

    _cached_ctypes: ct.Clay_Sizing | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )
    _hash: int | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def _compute_hash(self) -> int:
        return hash((self.width, self.height))

    def to_ctypes(self) -> ct.Clay_Sizing:
        """Convert the config to the underlying ctypes structure."""
        cur_hash: int = self._compute_hash()
        if self._hash != cur_hash or self._cached_ctypes is None:
            c_sizing: ct.Clay_Sizing = ct.Clay_Sizing()
            c_sizing.width = self.width.to_ctypes()
            c_sizing.height = self.height.to_ctypes()

            self._cached_ctypes = c_sizing
            self._hash = cur_hash
        return self._cached_ctypes


class Padding(NamedTuple):
    """Controls white-space padding around the outside of child elements."""

    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0

    def to_ctypes(self) -> ct.Clay_Padding:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_Padding(
            left=self.left,
            right=self.right,
            top=self.top,
            bottom=self.bottom,
        )

    @classmethod
    def from_ctypes(cls, c: ct.Clay_Padding) -> Padding:
        """Convert the underlying ctypes structure to the config."""
        return cls(left=c.left, right=c.right, top=c.top, bottom=c.bottom)

    @classmethod
    def all(cls, val: int) -> Padding:
        """Create equal padding on all sides."""
        return cls(left=val, right=val, top=val, bottom=val)

    @classmethod
    def horizontal_vertical(cls, left_right: int, top_bottom: int) -> Padding:
        """Create padding with equal left/right and top/bottom spaces."""
        return cls(left=left_right, right=left_right, top=top_bottom, bottom=top_bottom)


@dataclass
class LayoutConfig:
    """Controls various layout options of the element and its children."""

    sizing: Sizing = field(default_factory=Sizing)
    padding: Padding = field(default_factory=Padding)
    child_gap: int = 0
    child_alignment: ChildAlignment = field(default_factory=ChildAlignment)
    layout_direction: Clay_LayoutDirection = Clay_LayoutDirection.CLAY_LEFT_TO_RIGHT

    _cached_ctypes: ct.Clay_LayoutConfig | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )
    _hash: int | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def _compute_hash(self) -> int:
        return hash(
            (
                self.sizing,
                self.padding,
                self.child_gap,
                self.child_alignment,
                self.layout_direction,
            ),
        )

    def to_ctypes(self) -> ct.Clay_LayoutConfig:
        """Convert the config to the underlying ctypes structure."""
        cur_hash: int = self._compute_hash()
        if self._hash != cur_hash or self._cached_ctypes is None:
            self._cached_ctypes = ct.Clay_LayoutConfig(
                sizing=self.sizing.to_ctypes(),
                padding=self.padding.to_ctypes(),
                childGap=self.child_gap,
                childAlignment=self.child_alignment.to_ctypes(),
                layoutDirection=self.layout_direction,
            )
            self._hash = cur_hash
        return self._cached_ctypes


@dataclass
class TextConfig:
    """Controls various options of text elements."""

    text_color: Color = field(default_factory=Color)
    font_id: int = 0
    font_size: int = 0
    letter_spacing: int = 0
    line_height: int = 0
    wrap_mode: Clay_TextElementConfigWrapMode = (
        Clay_TextElementConfigWrapMode.CLAY_TEXT_WRAP_WORDS
    )
    text_alignment: Clay_TextAlignment = Clay_TextAlignment.CLAY_TEXT_ALIGN_LEFT
    user_data: Any = None

    _cached_ctypes: ct.Clay_TextElementConfig | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )
    _hash: int | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def _compute_hash(self) -> int:
        return hash(
            (
                self.text_color,
                self.font_id,
                self.font_size,
                self.letter_spacing,
                self.line_height,
                self.wrap_mode,
                self.text_alignment,
                # the library will use the id of user data pointers once implemented
                id(self.user_data),
            ),
        )

    def to_ctypes(self) -> ct.Clay_TextElementConfig:
        """Convert the config to the underlying ctypes structure."""
        cur_hash: int = self._compute_hash()
        if self._hash != cur_hash or self._cached_ctypes is None:
            c_config: ct.Clay_TextElementConfig = ct.Clay_TextElementConfig(
                textColor=self.text_color.to_ctypes(),
                fontId=self.font_id,
                fontSize=self.font_size,
                letterSpacing=self.letter_spacing,
                lineHeight=self.line_height,
                wrapMode=self.wrap_mode,
                textAlignment=self.text_alignment,
            )
            if self.user_data is not None:
                # TODO(oxygen): add user data storage
                c_config.userData = ctypes.c_void_p(0)
            else:
                c_config.userData = ctypes.c_void_p(0)

            self._cached_ctypes = c_config
            self._hash = cur_hash
        return self._cached_ctypes


class AspectRatioConfig(NamedTuple):
    """Controls elements which are scaled by their aspect ratio."""

    aspect_ratio: float = 0

    def to_ctypes(self) -> ct.Clay_AspectRatioElementConfig:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_AspectRatioElementConfig(aspectRatio=self.aspect_ratio)

    @classmethod
    def from_ctypes(cls, c: ct.Clay_AspectRatioElementConfig) -> AspectRatioConfig:
        """Convert the underlying ctypes structure to the config."""
        return cls(aspect_ratio=c.aspectRatio)


class ImageConfig(NamedTuple):
    """Controls image elements."""

    image_data: Any = None

    def to_ctypes(self) -> ct.Clay_ImageElementConfig:
        """Convert the config to the underlying ctypes structure."""
        c_config: ct.Clay_ImageElementConfig = ct.Clay_ImageElementConfig()

        if self.image_data is not None:
            # TODO(oxygen): add user data storage
            c_config.imageData = ctypes.c_void_p(0)
        else:
            c_config.imageData = ctypes.c_void_p(0)

        return c_config

    @classmethod
    def from_ctypes(cls, c: ct.Clay_ImageElementConfig) -> ImageConfig:
        """Convert the underlying ctypes structure to the config."""
        # TODO(oxygen): add user data retrieval
        return cls(image_data=c.imageData)


class FloatingAttachPoints(NamedTuple):
    """Controls where a floating element is offset relative to its parent."""

    element: Clay_FloatingAttachPointType = (
        Clay_FloatingAttachPointType.CLAY_ATTACH_POINT_LEFT_TOP
    )
    parent: Clay_FloatingAttachPointType = (
        Clay_FloatingAttachPointType.CLAY_ATTACH_POINT_LEFT_TOP
    )

    def to_ctypes(self) -> ct.Clay_FloatingAttachPoints:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_FloatingAttachPoints(element=self.element, parent=self.parent)

    @classmethod
    def from_ctypes(cls, c: ct.Clay_FloatingAttachPoints) -> FloatingAttachPoints:
        """Convert the underlying ctypes structure to the config."""
        return cls(element=c.element, parent=c.parent)


@dataclass
class FloatingConfig:
    """Controls various options of floating elements."""

    offset: Vector2 = field(default_factory=Vector2)
    expand: Dimensions = field(default_factory=Dimensions)
    parent_id: int = 0
    z_index: int = 0
    attach_points: FloatingAttachPoints = field(default_factory=FloatingAttachPoints)
    pointer_capture_mode: Clay_PointerCaptureMode = (
        Clay_PointerCaptureMode.CLAY_POINTER_CAPTURE_MODE_CAPTURE
    )
    attach_to: Clay_FloatingAttachToElement = (
        Clay_FloatingAttachToElement.CLAY_ATTACH_TO_NONE
    )
    clip_to: Clay_FloatingClipToElement = Clay_FloatingClipToElement.CLAY_CLIP_TO_NONE

    _cached_ctypes: ct.Clay_FloatingElementConfig | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )
    _hash: int | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def _compute_hash(self) -> int:
        return hash(
            (
                self.offset,
                self.expand,
                self.parent_id,
                self.z_index,
                self.attach_points,
                self.pointer_capture_mode,
                self.attach_to,
                self.clip_to,
            ),
        )

    def to_ctypes(self) -> ct.Clay_FloatingElementConfig:
        """Convert the config to the underlying ctypes structure."""
        cur_hash: int = self._compute_hash()
        if self._hash != cur_hash or self._cached_ctypes is None:
            self._cached_ctypes = ct.Clay_FloatingElementConfig(
                offset=self.offset.to_ctypes(),
                expand=self.expand.to_ctypes(),
                parentId=self.parent_id,
                zIndex=self.z_index,
                attachPoints=self.attach_points.to_ctypes(),
                pointerCaptureMode=self.pointer_capture_mode,
                attachTo=self.attach_to,
                clipTo=self.clip_to,
            )
            self._hash = cur_hash
        return self._cached_ctypes


class CustomConfig(NamedTuple):
    """Controls image elements."""

    custom_data: Any = None

    def to_ctypes(self) -> ct.Clay_CustomElementConfig:
        """Convert the config to the underlying ctypes structure."""
        c_config: ct.Clay_CustomElementConfig = ct.Clay_CustomElementConfig()

        if self.custom_data is not None:
            # TODO(oxygen): add user data storage
            c_config.customData = ctypes.c_void_p(0)
        else:
            c_config.customData = ctypes.c_void_p(0)

        return c_config

    @classmethod
    def from_ctypes(cls, c: ct.Clay_CustomElementConfig) -> CustomConfig:
        """Convert the underlying ctypes structure to the config."""
        # TODO(oxygen): add user data retrieval
        return cls(custom_data=c.customData)


class ClipConfig(NamedTuple):
    """Controls the scrolling axis of an element.

    Overflowing elements in the specified direction get clipped, which allows for
    scrolling in that direction.
    """

    horizontal: bool = False
    vertical: bool = False
    child_offset: Vector2 = Vector2()

    def to_ctypes(self) -> ct.Clay_ClipElementConfig:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_ClipElementConfig(
            horizontal=self.horizontal,
            vertical=self.vertical,
            childOffset=self.child_offset.to_ctypes(),
        )

    @classmethod
    def from_ctypes(cls, c: ct.Clay_ClipElementConfig) -> ClipConfig:
        """Convert the underlying ctypes structure to the config."""
        return cls(
            horizontal=c.horizontal,
            vertical=c.vertical,
            child_offset=Vector2.from_ctypes(c.childOffset),
        )


class BorderWidth(NamedTuple):
    """Controls the widths of individual element borders.

    Also creates borders with specified width between children elements, if specified.
    Borders between children are created depending on the layoutDirection:
      - if "left to right", borders will be vertical lines
      - if "top to bottom", borders will be horizontal lines
    betweenChildren borders will result in individual RECTANGLE render commands.
    """

    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0
    between_children: int = 0

    def to_ctypes(self) -> ct.Clay_BorderWidth:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_BorderWidth(
            left=self.left,
            right=self.right,
            top=self.top,
            bottom=self.bottom,
            betweenChildren=self.between_children,
        )

    @classmethod
    def from_ctypes(cls, c: ct.Clay_BorderWidth) -> BorderWidth:
        """Convert the underlying ctypes structure to the config."""
        return cls(
            left=c.left,
            right=c.right,
            top=c.top,
            bottom=c.bottom,
            between_children=c.betweenChildren,
        )


class BorderConfig(NamedTuple):
    """Controls element borders."""

    color: Color = Color()
    width: BorderWidth = BorderWidth()

    def to_ctypes(self) -> ct.Clay_BorderElementConfig:
        """Convert the config to the underlying ctypes structure."""
        return ct.Clay_BorderElementConfig(
            color=self.color.to_ctypes(),
            width=self.width.to_ctypes(),
        )

    @classmethod
    def from_ctypes(cls, c: ct.Clay_BorderElementConfig) -> BorderConfig:
        """Convert the underlying ctypes structure to the config."""
        return cls(
            color=Color.from_ctypes(c.color),
            width=BorderWidth.from_ctypes(c.width),
        )


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


@dataclass
class TransitionEnterConfig:
    """Controls transition behaviour when entering a transition."""

    set_initial_state: (
        Callable[
            [TransitionData, Clay_TransitionProperty],
            TransitionData,
        ]
        | None
    ) = None
    trigger: Clay_TransitionEnterTriggerType = (
        Clay_TransitionEnterTriggerType.CLAY_TRANSITION_ENTER_SKIP_ON_FIRST_PARENT_FRAME
    )

    _cached_ctypes: ct.Clay_TransitionElementConfig._enter | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )
    _hash: int | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def _compute_hash(self) -> int:
        return hash((self.set_initial_state, self.trigger))

    def to_ctypes(self) -> ct.Clay_TransitionElementConfig._enter:
        """Convert the config to the underlying ctypes structure."""
        cur_hash: int = self._compute_hash()
        if self._hash != cur_hash or self._cached_ctypes is None:
            c_enter: ct.Clay_TransitionElementConfig._enter = (
                ct.Clay_TransitionElementConfig._enter()
            )
            if self.set_initial_state is not None:

                @ct.Clay_TransitionElementConfig._enter.setInitialState
                def wrapper(
                    c_target_state: ct.Clay_TransitionData,
                    c_properties: int,
                ) -> ct.Clay_TransitionData:
                    py_target_state: TransitionData = TransitionData.from_ctypes(
                        c_target_state,
                    )
                    py_properties: Clay_TransitionProperty = Clay_TransitionProperty(
                        c_properties,
                    )
                    # we explicitly check that set_initial_state != None, ty freaks out
                    py_result = self.set_initial_state(py_target_state, py_properties)  # ty:ignore[call-non-callable]
                    return py_result.to_ctypes()

                c_enter.setInitialState = wrapper
            c_enter.trigger = self.trigger

            self._cached_ctypes = c_enter
            self._hash = cur_hash
        return self._cached_ctypes


@dataclass
class TransitionExitConfig:
    """Controls transition behaviour when exiting from a transition."""

    set_final_state: (
        Callable[
            [TransitionData, Clay_TransitionProperty],
            TransitionData,
        ]
        | None
    ) = None
    trigger: Clay_TransitionExitTriggerType = (
        Clay_TransitionExitTriggerType.CLAY_TRANSITION_EXIT_SKIP_WHEN_PARENT_EXITS
    )
    sibling_ordering: Clay_ExitTransitionSiblingOrdering = (
        Clay_ExitTransitionSiblingOrdering.CLAY_EXIT_TRANSITION_ORDERING_NATURAL_ORDER
    )

    _cached_ctypes: ct.Clay_TransitionElementConfig._exit | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )
    _hash: int | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def _compute_hash(self) -> int:
        return hash((self.set_final_state, self.trigger, self.sibling_ordering))

    def to_ctypes(self) -> ct.Clay_TransitionElementConfig._exit:
        """Convert the config to the underlying ctypes structure."""
        cur_hash: int = self._compute_hash()
        if self._hash != cur_hash or self._cached_ctypes is None:
            c_exit: ct.Clay_TransitionElementConfig._exit = (
                ct.Clay_TransitionElementConfig._exit()
            )
            if self.set_final_state is not None:

                @ct.Clay_TransitionElementConfig._exit.setFinalState
                def wrapper(
                    c_initial_state: ct.Clay_TransitionData,
                    c_properties: int,
                ) -> ct.Clay_TransitionData:
                    py_target_state: TransitionData = TransitionData.from_ctypes(
                        c_initial_state,
                    )
                    py_properties: Clay_TransitionProperty = Clay_TransitionProperty(
                        c_properties,
                    )
                    # we explicitly check that set_final_state != None, ty freaks out
                    py_result = self.set_final_state(py_target_state, py_properties)  # ty:ignore[call-non-callable]
                    return py_result.to_ctypes()

                c_exit.setFinalState = wrapper
            c_exit.trigger = self.trigger
            c_exit.siblingOrdering = self.sibling_ordering

            self._cached_ctypes = c_exit
            self._hash = cur_hash
        return self._cached_ctypes


@dataclass
class TransitionConfig:
    """Controls various transition settings."""

    handler: Callable[[TransitionCallbackArgs], bool] | None = None
    duration: float = 0
    properties: Clay_TransitionProperty = (
        Clay_TransitionProperty.CLAY_TRANSITION_PROPERTY_NONE
    )
    interaction_handling: Clay_TransitionInteractionHandlingType = Clay_TransitionInteractionHandlingType.CLAY_TRANSITION_DISABLE_INTERACTIONS_WHILE_TRANSITIONING_POSITION  # noqa: E501
    enter: TransitionEnterConfig = field(default_factory=TransitionEnterConfig)
    exit: TransitionExitConfig = field(default_factory=TransitionExitConfig)

    _cached_ctypes: ct.Clay_TransitionElementConfig | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )
    _hash: int | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def _compute_hash(self) -> int:
        return hash(
            (
                self.handler,
                self.duration,
                self.properties,
                self.interaction_handling,
                self.enter._hash,
                self.exit._hash,
            ),
        )

    def to_ctypes(self) -> ct.Clay_TransitionElementConfig:
        """Convert the config to the underlying ctypes structure."""
        cur_hash: int = self._compute_hash()
        if self._hash != cur_hash or self._cached_ctypes is None:
            c_config: ct.Clay_TransitionElementConfig = (
                ct.Clay_TransitionElementConfig()
            )

            if self.handler is not None:

                @ct.transitionHandlerFunction
                def wrapper(c_args: ct.Clay_TransitionCallbackArguments) -> bool:
                    args = TransitionCallbackArgs.from_ctypes(c_args)

                    # we explicitly check that handler != None, ty freaks out
                    return self.handler(args)  # ty:ignore[call-non-callable]

                c_config.handler = wrapper

            c_config.duration = self.duration
            c_config.properties = self.properties
            c_config.interactionHandling = self.interaction_handling
            c_config.enter = self.enter.to_ctypes()
            c_config.exit = self.exit.to_ctypes()

            self._cached_ctypes = c_config
            self._hash = cur_hash
        return self._cached_ctypes


@dataclass
class ElementDeclaration:
    """Declaration of an element."""

    layout: LayoutConfig = field(default_factory=LayoutConfig)
    background_color: Color = field(default_factory=Color)
    overlay_color: Color = field(default_factory=Color)
    corner_radius: CornerRadius = field(default_factory=CornerRadius)
    aspect_ratio: AspectRatioConfig = field(default_factory=AspectRatioConfig)
    floating: FloatingConfig = field(default_factory=FloatingConfig)
    custom: CustomConfig = field(default_factory=CustomConfig)
    clip: ClipConfig = field(default_factory=ClipConfig)
    border: BorderConfig = field(default_factory=BorderConfig)
    transition: TransitionConfig = field(default_factory=TransitionConfig)
    user_data: Any = None

    _cached_ctypes: ct.Clay_ElementDeclaration | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )
    _hash: int | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def _compute_hash(self) -> int:
        return hash(
            (
                self.layout._hash,
                self.background_color,
                self.overlay_color,
                self.corner_radius,
                self.aspect_ratio,
                self.floating._hash,
                self.custom,
                self.border,
                self.transition._hash,
                # the library will use the id of user data pointers once implemented
                id(self.user_data),
            ),
        )

    def to_ctypes(self) -> ct.Clay_ElementDeclaration:
        """Convert the config to the underlying ctypes structure."""
        cur_hash: int = self._compute_hash()
        if self._hash != cur_hash or self._cached_ctypes is None:
            c_elem: ct.Clay_ElementDeclaration = ct.Clay_ElementDeclaration(
                layout=self.layout.to_ctypes(),
                backgroundColor=self.background_color.to_ctypes(),
                overlayColor=self.overlay_color.to_ctypes(),
                cornerRadius=self.corner_radius.to_ctypes(),
                aspectRatio=self.aspect_ratio.to_ctypes(),
                floating=self.floating.to_ctypes(),
                custom=self.custom.to_ctypes(),
                clip=self.clip.to_ctypes(),
                border=self.border.to_ctypes(),
                transition=self.transition.to_ctypes(),
            )

            if self.user_data is not None:
                # TODO(oxygen): add user data storage
                c_elem.userData = ctypes.c_void_p(0)
            else:
                c_elem.userData = ctypes.c_void_p(0)

            self._cached_ctypes = c_elem
            self._hash = cur_hash
        return self._cached_ctypes
