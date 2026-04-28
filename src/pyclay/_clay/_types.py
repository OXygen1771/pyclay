"""Clay structure wrappers using ctypes."""

from ctypes import (
    CFUNCTYPE,
    POINTER,
    Structure,
    Union,
    c_bool,
    c_char_p,
    c_float,
    c_int16,
    c_int32,
    c_size_t,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
    c_void_p,
)

# ruff: disable[N801]

# --- Utility structs ---


class Clay_Context(Structure):
    # Since there is no public definition of Clay_Context in clay.h, don't
    # define anything here either.
    pass


class Clay_String(Structure):
    _fields_ = (
        ("isStaticallyAllocated", c_bool),
        ("length", c_int32),
        ("chars", c_char_p),
    )


class Clay_StringSlice(Structure):
    _fields_ = (
        ("length", c_int32),
        ("chars", c_char_p),
        ("baseChars", c_char_p),
    )


class Clay_Arena(Structure):
    _fields_ = (
        # uintptr_t ~= uint64_t on most platforms, so...
        ("nextAllocation", c_uint64),
        ("capacity", c_size_t),
        ("memory", c_char_p),
    )


class Clay_Dimensions(Structure):
    _fields_ = (
        ("width", c_float),
        ("height", c_float),
    )


class Clay_Vector2(Structure):
    _fields_ = (
        ("x", c_float),
        ("y", c_float),
    )


class Clay_Color(Structure):
    _fields_ = (
        ("r", c_float),
        ("g", c_float),
        ("b", c_float),
        ("a", c_float),
    )


class Clay_BoundingBox(Structure):
    _fields_ = (
        ("x", c_float),
        ("y", c_float),
        ("width", c_float),
        ("height", c_float),
    )


class Clay_ElementId(Structure):
    _fields_ = (
        ("id", c_uint32),
        ("offset", c_uint32),
        ("baseId", c_uint32),
        ("stringId", Clay_String),
    )


class Clay_ElementIdArray(Structure):
    _fields_ = (
        ("capacity", c_int32),
        ("length", c_int32),
        ("internalArray", POINTER(Clay_ElementId)),
    )


class Clay_CornerRadius(Structure):
    _fields_ = (
        ("topLeft", c_float),
        ("topRight", c_float),
        ("bottomLeft", c_float),
        ("bottomRight", c_float),
    )


# --- Element Configs ---
# see _clay_enums.py for enums


class Clay_ChildAlignment(Structure):
    _fields_ = (
        ("x", c_uint8),  # Clay_LayoutAlignmentX
        ("y", c_uint8),  # Clay_LayoutAlignmentY
    )


class Clay_SizingMinMax(Structure):
    _fields_ = (
        ("min", c_float),
        ("max", c_float),
    )


class Clay_SizingAxis(Structure):
    class _U(Union):
        _fields_ = (
            ("minMax", Clay_SizingMinMax),
            ("percent", c_float),
        )

    _fields_ = (
        ("size", _U),
        ("type", c_uint8),  # Clay_SizingType
    )


class Clay_Sizing(Structure):
    _fields_ = (
        ("width", Clay_SizingAxis),
        ("height", Clay_SizingAxis),
    )


class Clay_Padding(Structure):
    _fields_ = (
        ("left", c_uint16),
        ("right", c_uint16),
        ("top", c_uint16),
        ("bottom", c_uint16),
    )


class Clay_LayoutConfig(Structure):
    _fields_ = (
        ("sizing", Clay_Sizing),
        ("padding", Clay_Padding),
        ("childGap", c_uint16),
        ("childAlignment", Clay_ChildAlignment),
        ("layoutDirection", c_uint8),  # Clay_LayoutDirection
    )


class Clay_TextElementConfig(Structure):
    _fields_ = (
        ("userData", c_void_p),
        ("textColor", Clay_Color),
        ("fontId", c_uint16),
        ("fontSize", c_uint16),
        ("letterSpacing", c_uint16),
        ("lineHeight", c_uint16),
        ("wrapMode", c_uint8),  # Clay_TextElementConfigWrapMode
        ("textAlignment", c_uint8),  # Clay_TextAlignment
    )


# --- Aspect Ratio ---


class Clay_AspectRatioElementConfig(Structure):
    _fields_ = (("aspectRatio", c_float),)


# --- Image ---


class Clay_ImageElementConfig(Structure):
    _fields_ = (("imageData", c_void_p),)


# --- Floating ---


class Clay_FloatingAttachPoints(Structure):
    _fields_ = (
        ("element", c_uint8),  # Clay_FloatingAttachPointType
        ("parent", c_uint8),  # Clay_FloatingAttachPointType
    )


class Clay_FloatingElementConfig(Structure):
    _fields_ = (
        ("offset", Clay_Vector2),
        ("expand", Clay_Dimensions),
        ("parentId", c_uint32),
        ("zIndex", c_int16),
        ("attachPoints", Clay_FloatingAttachPoints),
        ("pointerCaptureMode", c_uint8),  # Clay_PointerCaptureMode
        ("attachTo", c_uint8),  # Clay_FloatingAttachToElement
        ("clipTo", c_uint8),  # Clay_FloatingClipToElement
    )


# --- Custom ---


class Clay_CustomElementConfig(Structure):
    _fields_ = (("customData", c_void_p),)


# --- Scroll ---


class Clay_ClipElementConfig(Structure):
    _fields_ = (
        ("horizontal", c_bool),
        ("vertical", c_bool),
        ("childOffset", Clay_Vector2),
    )


# --- Border ---


class Clay_BorderWidth(Structure):
    _fields_ = (
        ("left", c_uint16),
        ("right", c_uint16),
        ("top", c_uint16),
        ("bottom", c_uint16),
        ("betweenChildren", c_uint16),
    )


class Clay_BorderElementConfig(Structure):
    _fields_ = (
        ("color", Clay_Color),
        ("width", Clay_BorderWidth),
    )


# --- Transitions ---


class Clay_TransitionData(Structure):
    _fields_ = (
        ("boundingBox", Clay_BoundingBox),
        ("backgroundColor", Clay_Color),
        ("overlayColor", Clay_Color),
        ("borderColor", Clay_Color),
        ("borderWidth", Clay_BorderWidth),
    )


class Clay_TransitionCallbackArguments(Structure):
    _fields_ = (
        ("transitionState", c_uint8),  # Clay_TransitionState
        ("initial", Clay_TransitionData),
        ("current", POINTER(Clay_TransitionData)),
        ("target", Clay_TransitionData),
        ("elapsedTime", c_float),
        ("duration", c_float),
        ("properties", c_uint32),  # Clay_TransitionProperty (mask)
    )


class Clay_TransitionElementConfig(Structure):
    # bool (*handler)(Clay_TransitionCallbackArguments arguments)
    _handler = CFUNCTYPE(c_bool, Clay_TransitionCallbackArguments)

    class _enter(Structure):
        # Clay_TransitionData (*setInitialState)(
        #   Clay_TransitionData targetState,
        #   Clay_TransitionProperty properties
        # )
        _setInitialState = CFUNCTYPE(  # noqa: N815
            Clay_TransitionData,
            Clay_TransitionData,
            c_uint32,
        )

        _fields_ = (
            ("setInitialState", _setInitialState),
            ("trigger", c_uint8),  # Clay_TransitionEnterTriggerType
        )

    class _exit(Structure):
        # Clay_TransitionData (*setFinalState)(
        #   Clay_TransitionData initialState,
        #   Clay_TransitionProperty properties
        # )
        _setFinalState = CFUNCTYPE(  # noqa: N815
            Clay_TransitionData,
            Clay_TransitionData,
            c_uint32,
        )

        _fields_ = (
            ("setFinalState", _setFinalState),
            ("trigger", c_uint8),  # Clay_TransitionExitTriggerType
            ("siblingOrdering", c_uint8),  # Clay_TransitionSiblingOrdering
        )

    _fields_ = (
        ("handler", _handler),
        ("duration", c_float),
        ("properties", c_uint32),  # Clay_TransitionProperty
        ("interactionHandling", c_uint8),  # Clay_TransitionInteractionHandlingType
        ("enter", _enter),
        ("exit", _exit),
    )


# --- Render Command data ---


class Clay_TextRenderData(Structure):
    _fields_ = (
        ("stringContents", Clay_StringSlice),
        ("textColor", Clay_Color),
        ("fontId", c_uint16),
        ("fontSize", c_uint16),
        ("letterSpacing", c_uint16),
        ("lineHeight", c_uint16),
    )


class Clay_RectangleRenderData(Structure):
    _fields_ = (
        ("backgroundColor", Clay_Color),
        ("cornerRadius", Clay_CornerRadius),
    )


class Clay_ImageRenderData(Structure):
    _fields_ = (
        ("backgroundColor", Clay_Color),
        ("cornerRadius", Clay_CornerRadius),
        ("imageData", c_void_p),
    )


class Clay_CustomRenderData(Structure):
    _fields_ = (
        ("backgroundColor", Clay_Color),
        ("cornerRadius", Clay_CornerRadius),
        ("customData", c_void_p),
    )


class Clay_ClipRenderData(Structure):
    _fields_ = (
        ("horizontal", c_bool),
        ("vertical", c_bool),
    )


class Clay_OverlayColorRenderData(Structure):
    _fields_ = (("color", Clay_Color),)


class Clay_BorderRenderData(Structure):
    _field_ = (
        ("color", Clay_Color),
        ("cornerRadius", Clay_CornerRadius),
        ("width", Clay_BorderWidth),
    )


class Clay_RenderData(Union):
    _fields_ = (
        ("rectangle", Clay_RectangleRenderData),
        ("text", Clay_TextRenderData),
        ("image", Clay_ImageRenderData),
        ("custom", Clay_CustomRenderData),
        ("border", Clay_BorderRenderData),
        ("clip", Clay_ClipRenderData),
        ("overlayColor", Clay_OverlayColorRenderData),
    )


class Clay_RenderCommand(Structure):
    _fields_ = (
        ("boundingBox", Clay_BoundingBox),
        ("renderData", Clay_RenderData),
        ("userData", c_void_p),
        ("id", c_uint32),
        ("zIndex", c_int16),
        ("commandType", c_uint8),  # Clay_RenderCommandType
    )


class Clay_RenderCommandArray(Structure):
    _fields_ = (
        ("capacity", c_int32),
        ("length", c_int32),
        ("internalArray", POINTER(Clay_RenderCommand)),
    )


# --- Miscellaneous Structs ---


class Clay_ScrollContainerData(Structure):
    _fields_ = (
        ("scrollPosition", POINTER(Clay_Vector2)),
        ("scrollContainerDimensions", Clay_Dimensions),
        ("contentDimensions", Clay_Dimensions),
        ("config", Clay_ClipElementConfig),
        ("found", c_bool),
    )


class Clay_ElementData(Structure):
    _fields_ = (
        ("boundingBox", Clay_BoundingBox),
        ("found", c_bool),
    )


class Clay_PointerData(Structure):
    _fields_ = (
        ("position", Clay_Vector2),
        ("state", c_uint8),  # Clay_PointerDataInteractionState
    )


class Clay_ElementDeclaration(Structure):
    _fields_ = (
        ("layout", Clay_LayoutConfig),
        ("backgroundColor", Clay_Color),
        ("overlayColor", Clay_Color),
        ("cornerRadius", Clay_CornerRadius),
        ("aspectRatio", Clay_AspectRatioElementConfig),
        ("image", Clay_ImageElementConfig),
        ("floating", Clay_FloatingElementConfig),
        ("custom", Clay_CustomElementConfig),
        ("clip", Clay_ClipElementConfig),
        ("border", Clay_BorderElementConfig),
        ("transition", Clay_TransitionElementConfig),
        ("userData", c_void_p),
    )


# --- Errors ---


class Clay_ErrorData(Structure):
    _fields_ = (
        ("errorType", c_uint8),  # Clay_ErrorType
        ("errorText", Clay_String),
        ("userData", c_void_p),
    )


class Clay_ErrorHandler(Structure):
    _errorHandlerFunction = CFUNCTYPE(None, Clay_ErrorData)  # noqa: N815

    _fields_ = (
        ("errorHandlerFunction", _errorHandlerFunction),
        ("userData", c_void_p),
    )


# ruff: enable[N801]
# ruff: disable[N816]

# --- Function pointers ---

# void (*onHoverFunction)(
#   Clay_ElementId elementId,
#   Clay_PointerData pointerData,
#   void *userData
# )
onHoverFunction = CFUNCTYPE(
    None,
    Clay_ElementId,
    Clay_PointerData,
    c_void_p,
)

# Clay_Dimensions (*measureTextFunction)(
#   Clay_StringSlice text,
#   Clay_TextElementConfig *config,
#   void *userData
# )
measureTextFunction = CFUNCTYPE(
    Clay_Dimensions,
    Clay_StringSlice,
    Clay_TextElementConfig,
    c_void_p,
)

# Clay_Vector2 (*queryScrollOffsetFunction)(
#   uint32_t elementId,
#   void *userData
# )
queryScrollOffsetFunction = CFUNCTYPE(
    c_uint32,
    Clay_TextElementConfig,
)

# Via: Clay_ErrorHandler
# void (*errorHandlerFunction)(Clay_ErrorData errorText)
errorHandlerFunction = CFUNCTYPE(None, Clay_ErrorData)

# Via: Clay_TransitionElementConfig
# bool (*handler)(Clay_TransitionCallbackArguments arguments)
transitionHandlerFunction = CFUNCTYPE(c_bool, Clay_TransitionCallbackArguments)

# ruff: enable[N816]
