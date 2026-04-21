"""Factories and helpers for creating Clay structures."""

import ctypes
from collections.abc import Callable
from enum import IntEnum, IntFlag

from pyclay._clay._lib import clay_ease_out
from pyclay._clay._types import (
    Clay_Arena,
    Clay_AspectRatioElementConfig,
    Clay_BorderElementConfig,
    Clay_BorderWidth,
    Clay_BoundingBox,
    Clay_ChildAlignment,
    Clay_ClipElementConfig,
    Clay_Color,
    Clay_CornerRadius,
    Clay_CustomElementConfig,
    Clay_Dimensions,
    Clay_ElementDeclaration,
    Clay_ElementId,
    Clay_ElementIdArray,
    Clay_FloatingAttachPoints,
    Clay_FloatingElementConfig,
    Clay_ImageElementConfig,
    Clay_LayoutConfig,
    Clay_Padding,
    Clay_Sizing,
    Clay_SizingAxis,
    Clay_SizingMinMax,
    Clay_String,
    Clay_StringSlice,
    Clay_TextElementConfig,
    Clay_TransitionCallbackArguments,
    Clay_TransitionData,
    Clay_TransitionElementConfig,
    Clay_Vector2,
)
from pyclay.enums import (
    ExitTransitionSiblingOrdering,
    FloatingAttachPointType,
    FloatingAttachToElement,
    FloatingClipToElement,
    LayoutAlignmentX,
    LayoutAlignmentY,
    LayoutDirection,
    PointerCaptureMode,
    SizingType,
    TextAlignment,
    TextElementConfigWrapMode,
    TransitionEnterTriggerType,
    TransitionExitTriggerType,
    TransitionInteractionHandlingType,
    TransitionProperty,
)

# --- Validation helpers ---

_validation_enabled: bool = __debug__
_error_callback: Callable[[str], bool] | None = None


def set_validation_enabled(enabled: bool) -> None:
    """Enable or disable validating the conversions from Python to C data types.

    By default, set to True when the Python interpreter is in debugging mode.

    :param enabled: New setting.
    :type enabled: bool
    """
    global _validation_enabled
    _validation_enabled = enabled


def set_error_callback(callback: Callable[[str], bool]) -> None:
    """Set error callback to be called when encountering a validation error.

    The callback must receive a message string and return a boolean: True if the error
    was handled, False otherwise.
    By default, a ValueError gets raised when pyclay encounters a validation error.

    :param callback: Function to call when encountering an error. None by default.
    :type callback: Callable[[str], bool]
    """
    global _error_callback
    _error_callback = callback


def _handle_validation_errors(msg: str) -> None:
    """Handle validation errors.

    If _error_callback is set, tries to delegate the error handling to the user-defined
    callback. If _error_callback returns False, raises a ValueError.

    :raises ValueError: If validation is enabled and no user callback handled the error.
    :param msg: Message of the error.
    :type msg: str
    """
    if _error_callback and not _error_callback(msg):
        raise ValueError(msg)
    raise ValueError(msg)


def _check_enum_value(val: int, enum_cls: type[IntEnum], name: str) -> None:
    if not _validation_enabled:
        return

    int_val: int = val
    try:
        enum_cls(int_val)
    except ValueError:
        _handle_validation_errors(
            f"{name} must be a valid {enum_cls.__name__}, got {int_val} instead",
        )


def _check_enum_flag_value(
    val: int,
    flag_cls: type[IntFlag],
    name: str,
) -> None:
    if not _validation_enabled:
        return

    allowed: int = 0  # bitwise OR of all fields
    for member in flag_cls:
        allowed |= member
    int_val: int = val
    if int_val & ~allowed:
        _handle_validation_errors(
            f"{name} must be a valid {flag_cls.__name__}, got {int_val} instead",
        )


# only these for now


def _check_uint8(val: int, name: str) -> None:
    if _validation_enabled and not (0 <= val <= 255):
        _handle_validation_errors(f"{name} must be 0..255, got {val} instead")


def _check_uint16(val: int, name: str) -> None:
    if _validation_enabled and not (0 <= val <= 65535):
        _handle_validation_errors(f"{name} must be 0..65535, got {val} instead")


def _check_uint32(val: int, name: str) -> None:
    if _validation_enabled and not (0 <= val <= 4294967295):
        _handle_validation_errors(
            f"{name} must be 0..4294967295 (2^32 - 1), got {val} instead",
        )


def _check_uint64(val: int, name: str) -> None:
    if _validation_enabled and not (0 <= val <= 18446744073709551615):
        _handle_validation_errors(
            f"{name} must be 0..18446744073709551615 (2^64 - 1), got {val} instead",
        )


def _check_int16(val: int, name: str) -> None:
    if _validation_enabled and not (-32768 <= val <= 32767):
        _handle_validation_errors(f"{name} must be -32768..32767, got {val} instead")


def _check_int32(val: int, name: str) -> None:
    if _validation_enabled and not (-2147483648 <= val <= 2147483647):
        _handle_validation_errors(
            f"{name} must be -2147483648..2147483647, got {val} instead",
        )


_SIZE_T_MAX: int = (2 ** (ctypes.sizeof(ctypes.c_size_t) * 8)) - 1


def _check_size_t(val: int, name: str) -> None:
    if _validation_enabled and not (0 <= val <= _SIZE_T_MAX):
        _handle_validation_errors(f"{name} must be 0..{_SIZE_T_MAX}, got {val} instead")


def _check_float_nonnegative(val: float, name: str) -> None:
    if _validation_enabled and val < 0:
        _handle_validation_errors(f"{name} must be >=0, got {val} instead")


def _check_float_0_to_1(val: float, name: str) -> None:
    if _validation_enabled and not (0 <= val <= 1):
        _handle_validation_errors(f"{name} must be 0..1, got {val} instead")


# --- Factories ---


def make_clay_string(text: str, static: bool = False) -> Clay_String:
    """Generate a Clay_String.

    :param text: Contents of the string.
    :type text: str
    :param static: Whether the string was statically allocated and will live for the
        entire duration of the program (optional, False by default).
    :type static: bool
    :return: Resulting Clay_String.
    :rtype: Clay_String
    """
    b: bytes = text.encode("utf-8")
    return Clay_String(
        isStaticallyAllocated=static,
        length=len(b),
        chars=b,
    )


def make_clay_string_slice(text: str, base: str | None = None) -> Clay_StringSlice:
    """Generate a Clay_StringSlice.

    :param text: Contents of the string.
    :type text: str
    :param base: String the slice is derived from (optional).
    :type base: base
    :return: Resulting Clay_StringSlice.
    :rtype: Clay_StringSlice
    """
    b: bytes = text.encode("utf-8")
    b_base: bytes = base.encode("utf-8") if base is not None else b
    return Clay_StringSlice(
        length=len(b),
        chars=b,
        baseChars=b_base,
    )


def make_clay_arena(capacity: int, memory: bytes | None = None) -> Clay_Arena:
    """Generate a Clay_Arena.

    :param capacity: Desired capacity of the arena, in bytes. Usually determined via
        Clay_MinMemorySize() (clay_min_memory_size()).
    :type capacity: int
    :param memory: Pointer to allocated memory, if already allocated. None by default.
    :type memory: bytes | None
    :return: Resulting Clay_Arena.
    :rtype: Clay_Arena
    """
    _check_size_t(capacity, "Arena capacity (size_t)")
    return Clay_Arena(
        nextAllocation=0,
        capacity=capacity,
        memory=memory,
    )


def make_clay_dimensions(width: float, height: float) -> Clay_Dimensions:
    """Generate a Clay_Dimensions structure.

    :param width: Width (non-negative).
    :type width: float
    :param height: Height (non-negative).
    :type height: float
    :return: Resulting Clay_Dimensions.
    :rtype: Clay_Dimensions
    """
    _check_float_nonnegative(width, "Width of Dimensions")
    _check_float_nonnegative(height, "Height of Dimensions")
    return Clay_Dimensions(width=width, height=height)


def make_clay_vector2(x: float, y: float) -> Clay_Vector2:
    """Generate a Clay_Vector2.

    :return: Resulting Clay_Vector2.
    :rtype: Clay_Vector2
    """
    return Clay_Vector2(x=x, y=y)


def make_clay_color(r: float, g: float, b: float, a: float) -> Clay_Color:
    """Generate a Clay_Color.

    The RGBA values may not correspond to RGBA exactly, as they may be negative and in
    any range. The meaning is for you to decide.
    Note: Internally clay represents colors as values in the range 0..255, but
    interpretation is up to the renderer.

    :return: Resulting Clay_Color.
    :rtype: Clay_Color
    """
    return Clay_Color(r=r, g=g, b=b, a=a)


def make_clay_bounding_box(
    x: float,
    y: float,
    width: float,
    height: float,
) -> Clay_BoundingBox:
    """Generate a Clay_BoundingBox.

    :param x: X coordinate of the top-left corner of the bounding box.
    :type x: float
    :param y: Y coordinate of the top-left corner of the bounding box.
    :type y: float
    :param width: Width (non-negative).
    :type width: float
    :param height: Height (non-negative).
    :type height: float
    :return: Resulting Clay_BoundingBox.
    :rtype: Clay_BoundingBox
    """
    _check_float_nonnegative(width, "Width of BoundingBox")
    _check_float_nonnegative(height, "Height of BoundingBox")
    return Clay_BoundingBox(x=x, y=y, width=width, height=height)


def make_clay_element_id(
    id: int,  # noqa: A002
    offset: int = 0,
    base_id: int = 0,
    string_id: str | None = None,
) -> Clay_ElementId:
    """Generate a Clay_ElementId.

    :param id: Resulting hash generated from element's fields.
    :type id: int
    :param offset: Numerical offset applied after computing the hash from string_id.
    :type offset: int
    :param base_id: Base hash value to start from.
    :type base_id: int
    :param string_id: The string id to hash.
    :type string_id: str
    :return: Resulting Clay_ElementId.
    :rtype: Clay_ElementId
    """
    _check_uint32(id, "ElementId id (uint32)")
    _check_uint32(offset, "ElementId offset (uint32)")
    _check_uint32(base_id, "ElementId base_id (uint32)")
    clay_string: Clay_String = (
        make_clay_string(string_id) if string_id is not None else Clay_String()
    )
    return Clay_ElementId(id=id, offset=offset, baseId=base_id, stringId=clay_string)


def make_clay_element_id_array(
    element_ids: list[Clay_ElementId],
) -> Clay_ElementIdArray:
    """Generate a Clay_ElementIdArray from a list of Clay_ElementId.

    Note that you MUST call free_element_id_array() after using the array to avoid
    memory leaks.

    :param element_ids: List of Clay_ElementId.
    :type element_ids: list[Clay_ElementId]
    :return: Resulting Clay_ElementIdArray.
    :rtype: Clay_ElementIdArray
    """
    length: int = len(element_ids)
    if length == 0:
        return Clay_ElementIdArray(capacity=0, length=0, internalArray=None)

    array_type: type[ctypes.Array[Clay_ElementId]] = Clay_ElementId * length
    c_array: ctypes.Array[Clay_ElementId] = array_type(*element_ids)

    return Clay_ElementIdArray(
        capacity=length,
        length=length,
        internalArray=ctypes.cast(c_array, ctypes.POINTER(Clay_ElementId)),
    )


def free_clay_element_id_array(arr: Clay_ElementIdArray) -> None:
    """Free the memory allocated by make_clay_element_id_array()."""
    arr.internalArray = None


def make_clay_corner_radius(
    top_left: float,
    top_right: float,
    bottom_left: float,
    bottom_right: float,
) -> Clay_CornerRadius:
    """Generate a Clay_CornerRadius.

    :param top_left: Rounding radius of the top left corner (non-negative).
    :type top_left: float
    :param top_right: Rounding radius of the top right corner (non-negative).
    :type top_right: float
    :param bottom_left: Rounding radius of the bottom left corner (non-negative).
    :type bottom_left: float
    :param bottom_right: Rounding radius of the bottom right corner (non-negative).
    :type bottom_right: float
    :return: Resulting Clay_CornerRadius.
    :rtype: Clay_CornerRadius
    """
    _check_float_nonnegative(top_left, "Top left rounding corner")
    _check_float_nonnegative(top_right, "Top right rounding corner")
    _check_float_nonnegative(bottom_left, "Bottom left rounding corner")
    _check_float_nonnegative(bottom_right, "Bottom right rounding corner")
    return Clay_CornerRadius(
        topLeft=top_left,
        topRight=top_right,
        bottomLeft=bottom_left,
        bottomRight=bottom_right,
    )


def make_clay_child_alignment(
    x: LayoutAlignmentX | int | None = None,
    y: LayoutAlignmentY | int | None = None,
) -> Clay_ChildAlignment:
    """Generate a Clay_ChildAlignment.

    :param x: Alignment along the X axis (optional, left to right by default).
    :type x: LayoutAlignmentX | int
    :param y: Alignment along the Y axis (optional, top to bottom by default).
    :type y: LayoutAlignmentY | int
    :return: Resulting Clay_ChildAlignment.
    :rtype: Clay_ChildAlignment
    """
    if x is None:
        x = LayoutAlignmentX.default()
    elif not isinstance(x, LayoutAlignmentX):
        _check_enum_value(x, LayoutAlignmentX, "x layout alignment")
        x = LayoutAlignmentX(x)
    if y is None:
        y = LayoutAlignmentY.default()
    elif not isinstance(y, LayoutAlignmentY):
        _check_enum_value(y, LayoutAlignmentY, "y layout alignment")
        y = LayoutAlignmentY(y)

    return Clay_ChildAlignment(
        x=x.value,
        y=y.value,
    )


def make_clay_sizing_min_max(
    min_sizing: float = 0,
    max_sizing: float = float("inf"),
) -> Clay_SizingMinMax:
    """Generate a Clay_SizingMinMax.

    :param min_sizing: The minimm size an element can be (non-negative).
    :type min_sizing: float
    :param max_sizing: The maximum size an element can be (non-negative).
    :type max_sizing: float
    :return: Resulting Clay_SizingMinMax.
    :rtype: Clay_SizingMinMax
    """
    _check_float_nonnegative(min_sizing, "min sizing")
    if max_sizing != float("inf"):
        _check_float_nonnegative(max_sizing, "max sizing")
    return Clay_SizingMinMax(min=min_sizing, max=max_sizing)


def make_clay_sizing_axis(
    sizing_type: SizingType | int | None = None,
    min_max: Clay_SizingMinMax | None = None,
    percent: float | None = None,
) -> Clay_SizingAxis:
    """Generate a Clay_SizingAxis.

    Depending on the type, either min_max or percent must be specified. If they are not
    specified, default values will be used (max size).

    :param sizing_type: The sizing type. See SizingType.
    :type sizing_type: SizingType | int
    :param min_max: The minimum and maximum size of an element if the type is FIT or
        GROW.
    :type min_max: Clay_SizingMinMax
    :param percent: The percent of parent's space the element can occupy. 0..1 range.
    :type percent: float
    :return: Resulting Clay_SizingAxis.
    :rtype: Clay_SizingAxis
    """
    if sizing_type is None:
        sizing_type = SizingType.default()
    elif not isinstance(sizing_type, SizingType):
        _check_enum_value(sizing_type, SizingType, "Sizing type")
        sizing_type = SizingType(sizing_type)

    axis: Clay_SizingAxis = Clay_SizingAxis(type=sizing_type.value)

    if sizing_type == SizingType.PERCENT:
        if percent is None:
            percent = 1.0
        else:
            _check_float_0_to_1(percent, "Sizing percent")
        axis.size.percent = percent
        return axis

    if min_max is None:
        min_max = Clay_SizingMinMax(min=0, max=float("inf"))
    axis.size.minMax = min_max
    return axis


def make_clay_sizing(
    width: Clay_SizingAxis,
    height: Clay_SizingAxis,
) -> Clay_Sizing:
    """Generate a Clay_Sizing.

    :param width: Sizing along the horizontal axis.
    :type width: Clay_SizingAxis
    :param height: Sizing along the vertical axis.
    :type height: Clay_SizingAxis
    :return: Resulting Clay_Sizing.
    :rtype: Clay_Sizing
    """
    return Clay_Sizing(width=width, height=height)


def make_clay_padding(left: int, right: int, top: int, bottom: int) -> Clay_Padding:
    """Generate a Clay_Padding structure.

    Note that all the fields must be non-negative.

    :return: Resulting Clay_Padding.
    :rtype: Clay_Padding
    """
    _check_uint16(left, "left padding")
    _check_uint16(right, "right padding")
    _check_uint16(top, "top padding")
    _check_uint16(bottom, "bottom padding")
    return Clay_Padding(left=left, right=right, top=top, bottom=bottom)


def make_clay_layout_config(
    sizing: Clay_Sizing,
    padding: Clay_Padding,
    child_alignment: Clay_ChildAlignment,
    child_gap: int = 0,
    layout_direction: LayoutDirection | int | None = None,
) -> Clay_LayoutConfig:
    """Generate a Clay_LayoutConfig.

    :param sizing: Sizing of the element layout.
    :type sizing: Clay_Sizing
    :param padding: Padding between this element's border and its children.
    :type padding: Clay_Padding
    :param child_alignment: Alignment of children relative to parent container.
    :type child_alignment: Clay_ChildAlignment
    :param child_gap: Gap between children in pixels along layout axis (non-negative).
    :type child_gap: int
    :param layout_direction: Layout of child elements.
    :type layout_direction: LayoutDirection | int
    :return: Resulting Clay_LayoutConfig.
    :rtype: Clay_LayoutConfig
    """
    _check_uint16(child_gap, "child gap")
    if layout_direction is None:
        layout_direction = LayoutDirection.default()
    elif not isinstance(layout_direction, LayoutDirection):
        _check_enum_value(layout_direction, LayoutDirection, "layout direction")
        layout_direction = LayoutDirection(layout_direction)

    return Clay_LayoutConfig(
        sizing=sizing,
        padding=padding,
        childGap=child_gap,
        childAlignment=child_alignment,
        layoutDirection=layout_direction.value,
    )


def make_clay_text_element_config(
    text_color: Clay_Color,
    font_id: int,
    font_size: int,
    letter_spacing: int,
    line_height: int,
    wrap_mode: TextElementConfigWrapMode | int | None = None,
    text_alignment: TextAlignment | int | None = None,
    user_data: ctypes.c_void_p | None = None,
) -> Clay_TextElementConfig:
    """Generate a Clay_TextElementConfig.

    :param text_color: Clay_Color of text.
    :type text_color: Clay_Color
    :param font_id: Integer transparently passed to Clay_MeasureText(). Font management
        and mapping is up to the user. Non-negative.
    :type font_id: int
    :param font_size: Size of the font. Interpretation is up to the user. Non-negative.
    :type font_size: int
    :param letter_spacing: Spacing between letters. Interpretation is up to the user.
        Non-negative.
    :type letter_spacing: int
    :param line_height: If not zero, forcibly sets the height of each wrapped line of
        text to line_height pixels tall. If zero, uses the measured height of the font.
        Non-negative.
    :type line_height: int
    :param wrap_mode: Specifies text wrapping conditions.
    :type wrap_mode: TextElementConfigWrapMode | int
    :param text_alignment: Alignment of wrapped text lines.
    :type text_alignment: TextAlignment | int
    :param user_data: Pointer transparently passed to the renderer.
    :type user_data: c_void_p
    :return: Resulting Clay_TextElementConfig.
    :rtype: Clay_TextElementConfig
    """
    _check_uint16(font_id, "font id")
    _check_uint16(font_size, "font size")
    _check_uint16(letter_spacing, "letter spacing")
    _check_uint16(line_height, "line height")
    if wrap_mode is None:
        wrap_mode = TextElementConfigWrapMode.default()
    elif not isinstance(wrap_mode, TextElementConfigWrapMode):
        _check_enum_value(wrap_mode, TextElementConfigWrapMode, "Text config wrap mode")
        wrap_mode = TextElementConfigWrapMode(wrap_mode)
    if text_alignment is None:
        text_alignment = TextAlignment.default()
    elif not isinstance(text_alignment, TextAlignment):
        _check_enum_value(text_alignment, TextAlignment, "Text alignment")
        text_alignment = TextAlignment(text_alignment)

    return Clay_TextElementConfig(
        userData=user_data,
        textColor=text_color,
        fontId=font_id,
        fontSize=font_size,
        letterSpacing=letter_spacing,
        lineHeight=line_height,
        wrapMode=wrap_mode.value,
        textAlignment=text_alignment.value,
    )


def make_clay_aspect_ratio_element_config(
    aspect_ratio: float,
) -> Clay_AspectRatioElementConfig:
    """Generate a Clay_AspectRatioElementConfig.

    :param aspect_ratio: Desired aspect_ratio of an element. Non-negative.
    :type aspect_ratio: float
    :return: Resulting Clay_AspectRatioElementConfig.
    :rtype: Clay_AspectRatioElementConfig
    """
    _check_float_nonnegative(aspect_ratio, "Aspect ratio")
    return Clay_AspectRatioElementConfig(aspectRatio=aspect_ratio)


def make_clay_image_element_config(
    image_data: ctypes.c_void_p,
) -> Clay_ImageElementConfig:
    """Generate a Clay_ImageElementConfig.

    :param image_data: Pointer transparently passed to the renderer.
    :type image_data: c_void_p
    :return: Resulting Clay_ImageElementConfig.
    :rtype: Clay_ImageElementConfig
    """
    return Clay_ImageElementConfig(imageData=image_data)


def make_clay_floating_attach_points(
    element: FloatingAttachPointType | int | None = None,
    parent: FloatingAttachPointType | int | None = None,
) -> Clay_FloatingAttachPoints:
    """Generate a Clay_FloatingAttachPoints.

    :param element: Attach type of the origin point that gets attached to the parent.
    :type element: FloatingAttachPointType | int
    :param parent: Attach type of the point on parent that the element gets attached to.
    :type parent: FloatingAttachPointType | int
    :return: Resulting Clay_FloatingAttachPoints.
    :rtype: Clay_FloatingAttachPoints
    """
    if element is None:
        element = FloatingAttachPointType.default()
    elif not isinstance(element, FloatingAttachPointType):
        _check_enum_value(
            element,
            FloatingAttachPointType,
            "Element origin attach type",
        )
        element = FloatingAttachPointType(element)
    if parent is None:
        parent = FloatingAttachPointType.default()
    elif not isinstance(parent, FloatingAttachPointType):
        _check_enum_value(parent, FloatingAttachPointType, "Parent point attach type")
        parent = FloatingAttachPointType(parent)

    return Clay_FloatingAttachPoints(element=element.value, parent=parent.value)


def make_clay_floating_element_config(
    offset: Clay_Vector2,
    expand: Clay_Dimensions,
    z_index: int,
    parent_id: int | None = None,
    attach_points: Clay_FloatingAttachPoints | None = None,
    pointer_captrue_mode: PointerCaptureMode | int | None = None,
    attach_to: FloatingAttachToElement | int | None = None,
    clip_to: FloatingClipToElement | int | None = None,
) -> Clay_FloatingElementConfig:
    """Generate a Clay_FloatingElementConfig.

    :raises ValueError: If attaching to an element via ID without a parent_id.
    :param offset: Applies an offset to floating element after all layout calculations.
    :type offset: Clay_Vector2
    :param expand: Expands the dimensions of floting element before laying out children.
    :type expand: Clay_Dimensions
    :param z_index: Z index by which the floating element will be sorted.
    :type z_index: int
    :param parent_id: ID of the element to attach the floating element to.
    :type parent_id: int
    :param attach_points: Points used to attach the floating element to its parent.
    :type attach_points: Clay_FloatingAttachPoints
    :param pointer_captrue_mode: Controls pointer event handling. Events are captured by
        the floating element by default.
    :type pointer_captrue_mode: PointerCaptureMode | int
    :param attach_to: Which element to attach this floating container to.
    :type attach_to: FloatingAttachToElement | int
    :param clip_to: Controls clipping of the floating element. The floating element is
        clipped to its parent by default.
    :type clip_to: FloatingClipToElement | int
    :return: Resulting Clay_FloatingElementConfig.
    :rtype: Clay_FloatingElementConfig
    """
    if pointer_captrue_mode is None:
        pointer_captrue_mode = PointerCaptureMode.default()
    elif not isinstance(pointer_captrue_mode, PointerCaptureMode):
        _check_enum_value(
            pointer_captrue_mode,
            PointerCaptureMode,
            "Pointer capture mode",
        )
        pointer_captrue_mode = PointerCaptureMode(pointer_captrue_mode)
    if attach_to is None:
        attach_to = FloatingAttachToElement.default()
    elif not isinstance(attach_to, FloatingAttachToElement):
        _check_enum_value(attach_to, FloatingAttachToElement, "Attach to element")
        attach_to = FloatingAttachToElement(attach_to)
    if clip_to is None:
        clip_to = FloatingClipToElement.default()
    elif not isinstance(clip_to, FloatingClipToElement):
        _check_enum_value(clip_to, FloatingClipToElement, "Clip to element")
        clip_to = FloatingClipToElement(clip_to)

    _check_int16(z_index, "Z index")

    if (
        attach_to
        in (
            FloatingAttachToElement.ATTACH_TO_PARENT,
            FloatingAttachToElement.ATTACH_TO_ELEMENT_WITH_ID,
        )
        and attach_points is None
    ):
        attach_points = make_clay_floating_attach_points()
        if parent_id is not None:
            _check_uint32(parent_id, "Parent ID")
        else:
            raise ValueError(
                "When attaching a floating element to something via ID, you must "
                "specify the ID of the parent element.",
            )

    return Clay_FloatingElementConfig(
        offset=offset,
        expand=expand,
        parentId=parent_id,
        zIndex=z_index,
        attachPoints=attach_points,
        pointerCaptureMode=pointer_captrue_mode.value,
        attachTo=attach_to.value,
        clipTo=clip_to.value,
    )


def make_clay_custom_element_config(
    custom_data: ctypes.c_void_p,
) -> Clay_CustomElementConfig:
    """Generate a Clay_CustomElementConfig.

    :param image_data: Pointer transparently passed to the renderer.
    :type image_data: c_void_p
    :return: Resulting Clay_CustomElementConfig.
    :rtype: Clay_CustomElementConfig
    """
    return Clay_CustomElementConfig(customData=custom_data)


def make_clay_clip_element_config(
    horizontal: bool,
    vertical: bool,
    child_offset: Clay_Vector2,
) -> Clay_ClipElementConfig:
    """Generate a Clay_ClipElementConfig.

    :param horizontal: Whether to clip the element horizontally.
    :type horizontal: bool
    :param vertical: Whether to clip the element vertically.
    :type vertical: bool
    :param child_offset: Offset positions of all children by this vector.
    :type child_offset: Clay_Vector2
    :return: Resulting Clay_CustomElementConfig.
    :rtype: Clay_CustomElementConfig
    """
    return Clay_ClipElementConfig(
        horizontal=horizontal,
        vertical=vertical,
        childOffset=child_offset,
    )


def make_clay_border_width(
    left: int,
    right: int,
    top: int,
    bottom: int,
    between_children: int,
) -> Clay_BorderWidth:
    """Generate a Clay_BorderWidth.

    Note that all parameters must be non-negative.

    :param left: Thickness of the left border.
    :type left: int
    :param right: Thickness of the right border.
    :type right: int
    :param top: Thickness of the top border.
    :type top: int
    :param bottom: Thickness of the bottom border.
    :type bottom: int
    :param between_children: Thickness of the border between child elements.
    :type between_children: int
    :return: Resulting Clay_BorderWidth.
    :rtype: Clay_BorderWidth
    """
    _check_uint16(left, "left border width")
    _check_uint16(right, "right border width")
    _check_uint16(top, "top border width")
    _check_uint16(bottom, "bottom border width")
    _check_uint16(between_children, "between children border width")
    return Clay_BorderWidth(
        left=left,
        right=right,
        top=top,
        bottom=bottom,
        betweenChildren=between_children,
    )


def make_clay_border_element_config(
    color: Clay_Color,
    width: Clay_BorderWidth,
) -> Clay_BorderElementConfig:
    """Generate a Clay_BorderElementConfig.

    :param color: Color of all visible borders.
    :type color: Clay_Color
    :param width: Border width settings.
    :type width: Clay_BorderWidth
    :return: Resulting Clay_BorderElementConfig.
    :rtype: Clay_BorderElementConfig
    """
    return Clay_BorderElementConfig(color=color, width=width)


def make_clay_transition_element_config(
    duration: float,
    handler: Callable[[Clay_TransitionCallbackArguments], bool] | None = None,
    properties: TransitionProperty | int | None = None,
    interaction_handling: TransitionInteractionHandlingType | int | None = None,
    enter_trigger: TransitionEnterTriggerType | int | None = None,
    enter_set_initial_state: Callable[
        [Clay_TransitionData, TransitionProperty],
        Clay_TransitionData,
    ]
    | None = None,
    exit_trigger: TransitionExitTriggerType | int | None = None,
    exit_set_final_state: Callable[
        [Clay_TransitionData, TransitionProperty],
        Clay_TransitionData,
    ]
    | None = None,
    sibling_ordering: ExitTransitionSiblingOrdering | int | None = None,
) -> Clay_TransitionElementConfig:
    """Generate a Clay_TransitionElementConfig.

    :param duration: Duration of the transition in seconds. Non-negative.
    :type duration: float
    :param handler: Called each frame to determine the current state of the element.
        Clay provides an EaseOut function.
    :type handler: Callable[[Clay_TransitionCallbackArguments], bool]
    :param properties: Properties on which to transition. A bitfield.
    :type properties: TransitionProperty | int
    :param interaction_handling: How interactions are handled during positions
        animations.
    :type interaction_handling: TransitionInteractionHandlingType | int
    :param enter_trigger: Whether the "enter" transition is triggered on the same frame
        the parent element appears.
    :type enter_trigger: TransitionEnterTriggerType | int
    :param enter_set_initial_state: Called the first time the element appears. If not
        set, the "enter" transition will not be played.
    :type enter_set_initial_state: Callable[
        [Clay_TransitionData, TransitionProperty], Clay_TransitionData]
    :param exit_trigger: Whether the "exit" transition is triggered on the same frame
        the parent element disappears.
    :type exit_trigger: TransitionExitTriggerType | int
    :param exit_set_final_state: Called the first time the element disappears. If not
        set, the "exit" transition will not be played.
    :type exit_set_final_state: Callable[
        [Clay_TransitionData, TransitionProperty], Clay_TransitionData]
    :param sibling_ordering: Controls relative z-ordering of exiting elements.
    :type sibling_ordering: ExitTransitionSiblingOrdering | int
    :return: Resulting Clay_TransitionElementConfig.
    :rtype: Clay_TransitionElementConfig
    """
    _check_float_nonnegative(duration, "Transition duration")
    if handler is None:
        handler = clay_ease_out
    if properties is None:
        properties = TransitionProperty.default()
    elif not isinstance(properties, TransitionProperty):
        _check_enum_flag_value(properties, TransitionProperty, "Transition property")
        properties = TransitionProperty(properties)
    if interaction_handling is None:
        interaction_handling = TransitionInteractionHandlingType.default()
    elif not isinstance(interaction_handling, TransitionInteractionHandlingType):
        _check_enum_value(
            interaction_handling,
            TransitionInteractionHandlingType,
            "Transition interaction",
        )
        interaction_handling = TransitionInteractionHandlingType(interaction_handling)

    enter_: Clay_TransitionElementConfig._enter | None = None
    exit_: Clay_TransitionElementConfig._exit | None = None

    if enter_set_initial_state is not None:
        if enter_trigger is None:
            enter_trigger = TransitionEnterTriggerType.default()
        elif not isinstance(enter_trigger, TransitionEnterTriggerType):
            _check_enum_value(
                enter_trigger,
                TransitionEnterTriggerType,
                "Enter trigger",
            )
            enter_trigger = TransitionEnterTriggerType(enter_trigger)

        # check user callback arguments
        def _enter_wrapper(
            target_state: Clay_TransitionData,
            raw_properties: ctypes.c_uint32,
        ) -> Clay_TransitionData:
            _check_enum_flag_value(
                int(raw_properties),
                TransitionProperty,
                "Transition property in user defined enter_set_initial_state()",
            )
            properties: TransitionProperty = TransitionProperty(raw_properties)
            return enter_set_initial_state(target_state, properties)

        enter_ = Clay_TransitionElementConfig._enter()
        enter_.trigger = enter_trigger
        enter_.setInitialState = Clay_TransitionElementConfig._enter.setInitialState(
            _enter_wrapper,
        )

    if exit_set_final_state is not None:
        if exit_trigger is None:
            exit_trigger = TransitionExitTriggerType.default()
        elif not isinstance(exit_trigger, TransitionExitTriggerType):
            _check_enum_value(
                exit_trigger,
                TransitionExitTriggerType,
                "Exit trigger",
            )
            exit_trigger = TransitionExitTriggerType(exit_trigger)
        if sibling_ordering is None:
            sibling_ordering = ExitTransitionSiblingOrdering.default()
        elif not isinstance(sibling_ordering, ExitTransitionSiblingOrdering):
            _check_enum_value(
                sibling_ordering,
                ExitTransitionSiblingOrdering,
                "Sibling exit ordering",
            )
            sibling_ordering = ExitTransitionSiblingOrdering(sibling_ordering)

        # check user callback arguments
        def _exit_wrapper(
            target_state: Clay_TransitionData,
            raw_properties: ctypes.c_uint32,
        ) -> Clay_TransitionData:
            _check_enum_flag_value(
                int(raw_properties),
                TransitionProperty,
                "Transition property in user defined exit_set_final_state()",
            )
            properties: TransitionProperty = TransitionProperty(raw_properties)
            return exit_set_final_state(target_state, properties)

        exit_ = Clay_TransitionElementConfig._exit()
        exit_.trigger = exit_trigger
        exit_.setFinalState = Clay_TransitionElementConfig._exit.setFinalState(
            _exit_wrapper,
        )
        exit_.siblingOrdering = sibling_ordering

    return Clay_TransitionElementConfig(
        handler=handler,
        duration=duration,
        properties=properties,
        interactionHandling=interaction_handling,
        enter=enter_,
        exit=exit_,
    )


def make_clay_element_declaration(
    layout: Clay_LayoutConfig,
    background_color: Clay_Color,
    overlay_color: Clay_Color | None = None,
    corner_radius: Clay_CornerRadius | None = None,
    aspect_ratio: Clay_AspectRatioElementConfig | None = None,
    floating: Clay_FloatingElementConfig | None = None,
    custom: Clay_CustomElementConfig | None = None,
    clip: Clay_ClipElementConfig | None = None,
    border: Clay_BorderElementConfig | None = None,
    transition: Clay_TransitionElementConfig | None = None,
    user_data: ctypes.c_void_p | None = None,
) -> Clay_ElementDeclaration:
    """Generate a Clay_ElementDeclaration.

    :param layout: Layout of the element and its children.
    :type layout: Clay_LayoutConfig
    :param background_color: If nothing else is set, color of the resulting rectangle.
    :type background_color: Clay_Color
    :param overlay_color: Color to overlay on the element and its children (optional).
    :type overlay_color: Clay_Color
    :param corner_radius: Rounding of the element's corners (optional).
    :type corner_radius: Clay_CornerRadius
    :param aspect_ratio: Desired aspect ratio of the element (optional).
    :type aspect_ratio: Clay_AspectRatioElementConfig
    :param floating: Controls element floating (optional).
    :type floating: Clay_FloatingElementConfig
    :param custom: Configuration for the CUSTOM render command (optional).
    :type custom: Clay_CustomElementConfig
    :param clip: Controls clipping of the element (optional).
    :type clip: Clay_ClipElementConfig
    :param border: Controls borders of the element (optional).
    :type border: Clay_BorderElementConfig
    :param transition: Controls transitions of the element (optional).
    :type transition: Clay_TransitionElementConfig
    :param user_data: User data, passed transparently to the renderer (optional).
    :type user_data: c_void_p
    :return: Resulting Clay_TransitionElementConfig.
    :rtype: Clay_TransitionElementConfig
    """
    return Clay_ElementDeclaration(
        layout=layout,
        backgroundColor=background_color,
        overlayColor=overlay_color,
        cornerRadius=corner_radius,
        aspectRatio=aspect_ratio,
        floating=floating,
        custom=custom,
        clip=clip,
        border=border,
        transition=transition,
        userData=user_data,
    )
