"""Clay enums: various element settings.

These enums mirror the C definitions from clay, but in a more Pythonic (duh) way.
They are NOT prefixed with Clay_ or Clay__, and members don't have long prefixes.
"""

from enum import IntEnum, IntFlag


class LayoutDirection(IntEnum):
    """Controls the layout direction of child elements."""

    LEFT_TO_RIGHT = 0
    TOP_TO_BOTTOM = 1

    @classmethod
    def default(cls) -> LayoutDirection:
        """Get the default value, as defined in clay.h."""
        return cls.LEFT_TO_RIGHT


class LayoutAlignmentX(IntEnum):
    """Controls the alignment of child elements along the X axis."""

    LEFT = 0
    RIGHT = 1
    CENTER = 2

    @classmethod
    def default(cls) -> LayoutAlignmentX:
        """Get the default value, as defined in clay.h."""
        return cls.LEFT


class LayoutAlignmentY(IntEnum):
    """Controls the alignment of child elements along the Y axis."""

    TOP = 0
    BOTTOM = 1
    CENTER = 2

    @classmethod
    def default(cls) -> LayoutAlignmentY:
        """Get the default value, as defined in clay.h."""
        return cls.TOP


class SizingType(IntEnum):
    """Controls how the element takes up space inside its parent container.

    Note: the double underscore might be a typo, but it is present in the original
    library, so I am including it here.
    """

    FIT = 0
    GROW = 1
    PERCENT = 2
    FIXED = 3

    @classmethod
    def default(cls) -> SizingType:
        """Get the default value, as defined in clay.h."""
        return cls.FIT


class TextElementConfigWrapMode(IntEnum):
    """Controls text wrapping."""

    WORDS = 0
    NEWLINES = 1
    NONE = 2

    @classmethod
    def default(cls) -> TextElementConfigWrapMode:
        """Get the default value, as defined in clay.h."""
        return cls.WORDS


class TextAlignment(IntEnum):
    """Controls how text is aligned within an outer text bounding box."""

    LEFT = 0
    CENTER = 1
    RIGHT = 2

    @classmethod
    def default(cls) -> TextAlignment:
        """Get the default value, as defined in clay.h."""
        return cls.LEFT


# --- Floating ---


class FloatingAttachPointType(IntEnum):
    """Controls where a floating element is offset relative to its parent."""

    LEFT_TOP = 0
    LEFT_CENTER = 1
    LEFT_BOTTOM = 2

    CENTER_TOP = 3
    CENTER_CENTER = 4
    CENTER_BOTTOM = 5

    RIGHT_TOP = 6
    RIGHT_CENTER = 7
    RIGHT_BOTTOM = 8

    @classmethod
    def default(cls) -> FloatingAttachPointType:
        """Get the default value, as defined in clay.h.

        Note that  doesn't specify the default value here.
        """
        return cls.LEFT_TOP


class PointerCaptureMode(IntEnum):
    """Controls how mouse pointer events are handled when above a floating element."""

    CAPTURE = 0
    PASSTHROUGH = 1

    @classmethod
    def default(cls) -> PointerCaptureMode:
        """Get the default value, as defined in clay.h."""
        return cls.CAPTURE


class FloatingAttachToElement(IntEnum):
    """Controls which element a floating element is attached to."""

    ATTACH_TO_NONE = 0
    ATTACH_TO_PARENT = 1
    ATTACH_TO_ELEMENT_WITH_ID = 2
    ATTACH_TO_ROOT = 3

    @classmethod
    def default(cls) -> FloatingAttachToElement:
        """Get the default value, as defined in clay.h."""
        return cls.ATTACH_TO_NONE


class FloatingClipToElement(IntEnum):
    """Controls floating element clipping."""

    CLIP_TO_NONE = 0
    CLIP_TO_ATTACHED_PARENT = 1

    @classmethod
    def default(cls) -> FloatingClipToElement:
        """Get the default value, as defined in clay.h."""
        return cls.CLIP_TO_NONE


# --- Transitions ---


class TransitionState(IntEnum):
    """Represents the transition state (?)."""

    IDLE = 0
    ENTERINT = 1
    TRANSITIONING = 2
    EXITING = 3

    @classmethod
    def default(cls) -> TransitionState:
        """Get the default value, as defined in clay.h.

        Note that  doesn't specify the default value here.
        """
        return cls.IDLE


class TransitionProperty(IntFlag):
    """Represents the property which the transition affects (?)."""

    NONE = 0
    X = 1
    Y = 2
    POSITION = X | Y

    WIDTH = 4
    HEIGHT = 8
    DIMENSIONS = WIDTH | HEIGHT

    BOUNDING_BOX = POSITION | DIMENSIONS

    BACKGROUND_COLOR = 16
    OVERLAY_COLOR = 32

    CORNER_RADIUS = 64

    BORDER_COLOR = 128
    BORDER_WIDTH = 256
    BORDER = BORDER_COLOR | BORDER_WIDTH

    @classmethod
    def default(cls):
        """Get the default value, as defined in clay.h.

        Note that  doesn't specify the default value here.
        """
        return cls.NONE


class TransitionEnterTriggerType(IntEnum):
    """Trigger to enter a transition (?)."""

    SKIP_ON_FIRST_PARENT_FRAME = 0
    TRIGGER_ON_FIRST_PARENT_FRAME = 1

    @classmethod
    def default(cls):
        """Get the default value, as defined in clay.h.

        Note that  doesn't specify the default value here.
        """
        return cls.SKIP_ON_FIRST_PARENT_FRAME


class TransitionExitTriggerType(IntEnum):
    """Trigger to exit a transition (?)."""

    SKIP_WHEN_PARENT_EXITS = 0
    TRIGGER_WHEN_PARENT_EXITS = 1

    @classmethod
    def default(cls):
        """Get the default value, as defined in clay.h.

        Note that  doesn't specify the default value here.
        """
        return cls.SKIP_WHEN_PARENT_EXITS


class TransitionInteractionHandlingType(IntEnum):
    """Whether to disable interactions during a transition (?)."""

    DISABLE_INTERACTIONS_WHILE_TRANSITIONING_POSITION = 0
    ALLOW_INTERACTIONS_WHILE_TRANSITIONING_POSITION = 1

    @classmethod
    def default(cls):
        """Get the default value, as defined in clay.h.

        Note that  doesn't specify the default value here.
        """
        return cls.DISABLE_INTERACTIONS_WHILE_TRANSITIONING_POSITION


class ExitTransitionSiblingOrdering(IntEnum):
    """Controls transition exit ordering (?)."""

    UNDERNEATH_SIBLINGS = 0
    NATURAL_ORDER = 1
    ABOVE_SIBLINGS = 2

    @classmethod
    def default(cls):
        """Get the default value, as defined in clay.h.

        Note that  doesn't specify the default value here.
        """
        return cls.NATURAL_ORDER


class RenderCommandType(IntEnum):
    """Used by renderers to determine specific handling for a render command."""

    NONE = 0
    RECTANGLE = 1
    BORDER = 2
    TEXT = 3
    IMAGE = 4
    SCISSOR_START = 5
    SCISSOR_END = 6
    OVERLAY_COLOR_START = 7
    OVERLAY_COLOR_END = 8
    CUSTOM = 9

    # Note that  doesn't specify the default value here.


# --- Miscellaneous Enums ---


class PointerDataInteractionState(IntEnum):
    """Represents the current state of interaction with clay in the current frame."""

    PRESSED_THIS_FRAME = 0
    PRESSED = 1
    RELEASED_THIS_FRAME = 2
    RELEASED = 3

    # Note that  doesn't specify the default value here.


# --- Errors ---


class ErrorType(IntEnum):
    """Represents the type of error clay encountered while computing layout."""

    TEXT_MEASUREMENT_FUNCTION_NOT_PROVIDED = 0
    ARENA_CAPACITY_EXCEEDED = 1
    ELEMENTS_CAPACITY_EXCEEDED = 2
    TEXT_MEASUREMENT_CAPACITY_EXCEEDED = 3
    DUPLICATE_ID = 4
    FLOATING_CONTAINER_PARENT_NOT_FOUND = 5
    PERCENTAGE_OVER_1 = 6
    INTERNAL_ERROR = 7
    UNBALANCED_OPEN_CLOSE = 8

    # Note that  doesn't specify the default value here.
