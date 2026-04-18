"""Clay enums.

Most of these are CLAY_PACKED_ENUM, and are not directly used in _clay_types.py
structures. A packed enum ensures that the size of the enum is a single byte.
"""

from enum import IntEnum, IntFlag

# ruff: disable[N801]


class Clay_LayoutDirection(IntEnum):
    """Controls the layout direction of child elements."""

    CLAY_LEFT_TO_RIGHT = 0
    CLAY_TOP_TO_BOTTOM = 1

    @classmethod
    def default(cls) -> Clay_LayoutDirection:
        """Get the default value, as defined in clay.h."""
        return cls.CLAY_LEFT_TO_RIGHT


class Clay_LayoutAlignmentX(IntEnum):
    """Controls the alignment of child elements along the X axis."""

    CLAY_ALIGN_X_LEFT = 0
    CLAY_ALIGN_X_RIGHT = 1
    CLAY_ALIGN_X_CENTER = 2

    @classmethod
    def default(cls) -> Clay_LayoutAlignmentX:
        """Get the default value, as defined in clay.h."""
        return cls.CLAY_ALIGN_X_LEFT


class Clay_LayoutAlignmentY(IntEnum):
    """Controls the alignment of child elements along the Y axis."""

    CLAY_ALIGN_Y_LEFT = 0
    CLAY_ALIGN_Y_RIGHT = 1
    CLAY_ALIGN_Y_CENTER = 2

    @classmethod
    def default(cls) -> Clay_LayoutAlignmentY:
        """Get the default value, as defined in clay.h."""
        return cls.CLAY_ALIGN_Y_LEFT


class Clay__SizingType(IntEnum):
    """Controls how the element takes up space inside its parent container.

    Note: the double underscore might be a typo, but it is present in the original
    library, so I am including it here.
    """

    CLAY__SIZING_TYPE_FIT = 0
    CLAY__SIZING_TYPE_GROW = 1
    CLAY__SIZING_TYPE_PERCENT = 2
    CLAY__SIZING_TYPE_FIXED = 3

    @classmethod
    def default(cls) -> Clay__SizingType:
        """Get the default value, as defined in clay.h."""
        return cls.CLAY__SIZING_TYPE_FIT


class Clay_TextElementConfigWrapMode(IntEnum):
    """Controls text wrapping."""

    CLAY_TEXT_WRAP_WORDS = 0
    CLAY_TEXT_WRAP_NEWLINES = 1
    CLAY_TEXT_WRAP_NONE = 2

    @classmethod
    def default(cls) -> Clay_TextElementConfigWrapMode:
        """Get the default value, as defined in clay.h."""
        return cls.CLAY_TEXT_WRAP_WORDS


class Clay_TextAlignment(IntEnum):
    """Controls how text is aligned within an outer text bounding box."""

    CLAY_TEXT_ALIGN_LEFT = 0
    CLAY_TEXT_ALIGN_CENTER = 0
    CLAY_TEXT_ALIGN_RIGHT = 0

    @classmethod
    def default(cls) -> Clay_TextAlignment:
        """Get the default value, as defined in clay.h."""
        return cls.CLAY_TEXT_ALIGN_LEFT


# --- Floating ---


class Clay_FloatingAttachPointType(IntEnum):
    """Controls where a floating element is offset relative to its parent."""

    CLAY_ATTACH_POINT_LEFT_TOP = 0
    CLAY_ATTACH_POINT_LEFT_CENTER = 1
    CLAY_ATTACH_POINT_LEFT_BOTTOM = 2

    CLAY_ATTACH_POINT_CENTER_TOP = 3
    CLAY_ATTACH_POINT_CENTER_CENTER = 4
    CLAY_ATTACH_POINT_CENTER_BOTTOM = 5

    CLAY_ATTACH_POINT_RIGHT_TOP = 6
    CLAY_ATTACH_POINT_RIGHT_CENTER = 7
    CLAY_ATTACH_POINT_RIGHT_BOTTOM = 8

    @classmethod
    def default(cls) -> Clay_FloatingAttachPointType:
        """Get the default value, as defined in clay.h.

        Note that Clay doesn't specify the default value here.
        """
        return cls.CLAY_ATTACH_POINT_LEFT_TOP


class Clay_PointerCaptureMode(IntEnum):
    """Controls how mouse pointer events are handled when above a floating element."""

    CLAY_POINTER_CAPTURE_MODE_CAPTURE = 0
    CLAY_POINTER_CAPTURE_MODE_PASSTHROUGH = 1

    @classmethod
    def default(cls) -> Clay_PointerCaptureMode:
        """Get the default value, as defined in clay.h."""
        return cls.CLAY_POINTER_CAPTURE_MODE_CAPTURE


class Clay_FloatingAttachToElement(IntEnum):
    """Controls which element a floating element is attached to."""

    CLAY_ATTACH_TO_NONE = 0
    CLAY_ATTACH_TO_PARENT = 1
    CLAY_ATTACH_TO_ELEMENT_WITH_ID = 2
    CLAY_ATTACH_TO_ROOT = 3

    @classmethod
    def default(cls) -> Clay_FloatingAttachToElement:
        """Get the default value, as defined in clay.h."""
        return cls.CLAY_ATTACH_TO_NONE


class Clay_FloatingClipToElement(IntEnum):
    """Controls floating element clipping."""

    CLAY_CLIP_TO_NONE = 0
    CLAY_CLIP_TO_ATTACHED_PARENT = 1

    @classmethod
    def default(cls) -> Clay_FloatingClipToElement:
        """Get the default value, as defined in clay.h."""
        return cls.CLAY_CLIP_TO_NONE


# --- Transitions ---


class Clay_TransitionState(IntEnum):
    """Represents the transition state (?)."""

    CLAY_TRANSITION_STATE_IDLE = 0
    CLAY_TRANSITION_STATE_ENTERINT = 1
    CLAY_TRANSITION_STATE_TRANSITIONING = 2
    CLAY_TRANSITION_STATE_EXITING = 3

    @classmethod
    def default(cls) -> Clay_TransitionState:
        """Get the default value, as defined in clay.h.

        Note that Clay doesn't specify the default value here.
        """
        return cls.CLAY_TRANSITION_STATE_IDLE


class Clay_TransitionProperty(IntFlag):
    """Represents the property which the transition affects (?)."""

    CLAY_TRANSITION_PROPERTY_NONE = 0
    CLAY_TRANSITION_PROPERTY_X = 1
    CLAY_TRANSITION_PROPERTY_Y = 2
    CLAY_TRANSITION_PROPERTY_POSITION = (
        CLAY_TRANSITION_PROPERTY_X | CLAY_TRANSITION_PROPERTY_Y
    )

    CLAY_TRANSITION_PROPERTY_WIDTH = 4
    CLAY_TRANSITION_PROPERTY_HEIGHT = 8
    CLAY_TRANSITION_PROPERTY_DIMENSIONS = (
        CLAY_TRANSITION_PROPERTY_WIDTH | CLAY_TRANSITION_PROPERTY_HEIGHT
    )

    CLAY_TRANSITION_PROPERTY_BOUNDING_BOX = (
        CLAY_TRANSITION_PROPERTY_POSITION | CLAY_TRANSITION_PROPERTY_DIMENSIONS
    )

    CLAY_TRANSITION_PROPERTY_BACKGROUND_COLOR = 16
    CLAY_TRANSITION_PROPERTY_OVERLAY_COLOR = 32

    CLAY_TRANSITION_PROPERTY_CORNER_RADIUS = 64

    CLAY_TRANSITION_PROPERTY_BORDER_COLOR = 128
    CLAY_TRANSITION_PROPERTY_BORDER_WIDTH = 256
    CLAY_TRANSITION_PROPERTY_BORDER = (
        CLAY_TRANSITION_PROPERTY_BORDER_COLOR | CLAY_TRANSITION_PROPERTY_BORDER_WIDTH
    )

    @classmethod
    def default(cls):
        """Get the default value, as defined in clay.h.

        Note that Clay doesn't specify the default value here.
        """
        return cls.CLAY_TRANSITION_PROPERTY_NONE


class Clay_TransitionEnterTriggerType(IntEnum):
    """Trigger to enter a transition (?)."""

    CLAY_TRANSITION_ENTER_SKIP_ON_FIRST_PARENT_FRAME = 0
    CLAY_TRANSITION_ENTER_TRIGGER_ON_FIRST_PARENT_FRAME = 1

    # Note that Clay doesn't specify the default value here.


class Clay_TransitionExitTriggerType(IntEnum):
    """Trigger to exit a transition (?)."""

    CLAY_TRANSITION_EXIT_SKIP_WHEN_PARENT_EXITS = 0
    CLAY_TRANSITION_EXIT_TRIGGER_WHEN_PARENT_EXITS = 1

    # Note that Clay doesn't specify the default value here.


class Clay_TransitionInteractionHandlingType(IntEnum):
    """Whether to disable interactions during a transition (?)."""

    CLAY_TRANSITION_DISABLE_INTERACTIONS_WHILE_TRANSITIONING_POSITION = 0
    CLAY_TRANSITION_ALLOW_INTERACTIONS_WHILE_TRANSITIONING_POSITION = 1

    # Note that Clay doesn't specify the default value here.


class Clay_ExitTransitionSiblingOrdering(IntEnum):
    """Controls transition exit ordering (?)."""

    CLAY_EXIT_TRANSITION_ORDERING_UNDERNEATH_SIBLINGS = 0
    CLAY_EXIT_TRANSITION_ORDERING_NATURAL_ORDER = 1
    CLAY_EXIT_TRANSITION_ORDERING_ABOVE_SIBLINGS = 2

    # Note that Clay doesn't specify the default value here.


class Clay_RenderCommandType(IntEnum):
    """Used by renderers to determine specific handling for a render command."""

    CLAY_RENDER_COMMAND_TYPE_NONE = 0
    CLAY_RENDER_COMMAND_TYPE_RECTANGLE = 1
    CLAY_RENDER_COMMAND_TYPE_BORDER = 2
    CLAY_RENDER_COMMAND_TYPE_TEXT = 3
    CLAY_RENDER_COMMAND_TYPE_IMAGE = 4
    CLAY_RENDER_COMMAND_TYPE_SCISSOR_START = 5
    CLAY_RENDER_COMMAND_TYPE_SCISSOR_END = 6
    CLAY_RENDER_COMMAND_TYPE_OVERLAY_COLOR_START = 7
    CLAY_RENDER_COMMAND_TYPE_OVERLAY_COLOR_END = 8
    CLAY_RENDER_COMMAND_TYPE_CUSTOM = 9

    # Note that Clay doesn't specify the default value here.


# --- Miscellaneous Enums ---


class Clay_PointerDataInteractionState(IntEnum):
    """Represents the current state of interaction with clay in the current frame."""

    CLAY_POINTER_DATA_PRESSED_THIS_FRAME = 0
    CLAY_POINTER_DATA_PRESSED = 1
    CLAY_POINTER_DATA_RELEASED_THIS_FRAME = 2
    CLAY_POINTER_DATA_RELEASED = 3

    # Note that Clay doesn't specify the default value here.


# --- Errors ---


class Clay_ErrorType(IntEnum):
    """Represents the type of error clay encountered while computing layout."""

    CLAY_ERROR_TYPE_TEXT_MEASUREMENT_FUNCTION_NOT_PROVIDED = 0
    CLAY_ERROR_TYPE_ARENA_CAPACITY_EXCEEDED = 1
    CLAY_ERROR_TYPE_ELEMENTS_CAPACITY_EXCEEDED = 2
    CLAY_ERROR_TYPE_TEXT_MEASUREMENT_CAPACITY_EXCEEDED = 3
    CLAY_ERROR_TYPE_DUPLICATE_ID = 4
    CLAY_ERROR_TYPE_FLOATING_CONTAINER_PARENT_NOT_FOUND = 5
    CLAY_ERROR_TYPE_PERCENTAGE_OVER_1 = 6
    CLAY_ERROR_TYPE_INTERNAL_ERROR = 7
    CLAY_ERROR_TYPE_UNBALANCED_OPEN_CLOSE = 8

    # Note that Clay doesn't specify the default value here.


# ruff: enable[N801]
