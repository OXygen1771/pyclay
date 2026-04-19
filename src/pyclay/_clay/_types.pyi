"""Interface definitions for Clay structures."""

from ctypes import (
    CFUNCTYPE,
    POINTER,
    Structure,
    Union,
    c_bool,
    c_uint32,
    c_void_p,
)

from pyclay.enums import (
    ErrorType,
    ExitTransitionSiblingOrdering,
    FloatingAttachPointType,
    FloatingAttachToElement,
    FloatingClipToElement,
    LayoutAlignmentX,
    LayoutAlignmentY,
    LayoutDirection,
    PointerCaptureMode,
    PointerDataInteractionState,
    RenderCommandType,
    SizingType,
    TextAlignment,
    TextElementConfigWrapMode,
    TransitionEnterTriggerType,
    TransitionExitTriggerType,
    TransitionInteractionHandlingType,
    TransitionProperty,
    TransitionState,
)

# ruff: disable[N801,N803,N815]

# --- Utility structs ---

class Clay_Context(Structure):
    """The clay context."""

    # Since there is no public definition of Clay_Context in clay.h, don't
    # define anything here either.

class Clay_String(Structure):
    """Base string structure. Either null-terminated C-string, or a slice."""

    isStaticallyAllocated: bool  # True if string lives for the program lifetime.
    length: int
    chars: bytes | None  # Underlying character memory.

    def __init__(
        self,
        isStaticallyAllocated: bool | None = ...,
        length: int | None = ...,
        chars: bytes | None = ...,
    ) -> None: ...

class Clay_StringSlice(Structure):
    """Represents non-owning string slices."""

    length: int
    chars: bytes | None
    baseChars: bytes | None  # Source string the slice was derived from.

    def __init__(
        self,
        length: int | None = ...,
        chars: bytes | None = ...,
        baseChars: bytes | None = ...,
    ) -> None: ...

class Clay_Arena(Structure):
    """Memory arena structure to manage clay's internal allocations."""

    nextAllocation: int  # uintptr_t to next allocation.
    capacity: int
    memory: bytes | None

    def __init__(
        self,
        nextAllocation: int | None = ...,
        capacity: int | None = ...,
        memory: bytes | None = ...,
    ) -> None: ...

class Clay_Dimensions(Structure):
    """Dimensions of an object."""

    width: float
    height: float

    def __init__(
        self,
        width: float | None = ...,
        height: float | None = ...,
    ) -> None: ...

class Clay_Vector2(Structure):
    """Two-dimensional vector."""

    x: float
    y: float

    def __init__(
        self,
        x: float | None = ...,
        y: float | None = ...,
    ) -> None: ...

class Clay_Color(Structure):
    """Color represented as RGBA.

    Note: Internally clay represents these colors as values in the range 0-255, but
    interpretation is up to the renderer.
    """

    r: float
    g: float
    b: float
    a: float

    def __init__(
        self,
        r: float | None = ...,
        g: float | None = ...,
        b: float | None = ...,
        a: float | None = ...,
    ) -> None: ...

class Clay_BoundingBox(Structure):
    """Bounding box of an object."""

    x: float
    y: float
    width: float
    height: float

    def __init__(
        self,
        x: float | None = ...,
        y: float | None = ...,
        width: float | None = ...,
        height: float | None = ...,
    ) -> None: ...

class Clay_ElementId(Structure):
    """Hashed string ID of specific UI elements.

    Represents a hashed string ID used for identifying and finding specific clay UI
    elements.
    Primarily created automatically via  << TODO: add examples;
    """

    id: int  # Resulting hash generated from other fields.
    offset: int  # Numerical offset applied after computing the hash from stringId.
    baseId: int  # Base hash value to start from.
    stringId: Clay_String  # The string id to hash.

    def __init__(
        self,
        id: int | None = ...,  # noqa: A002
        offset: int | None = ...,
        baseId: int | None = ...,
        stringId: Clay_String | None = ...,
    ) -> None: ...

class Clay_ElementIdArray(Structure):
    """Sized array of Clay_ElementId."""

    capacity: int
    length: int
    internalArray: type[POINTER(Clay_ElementId)] | None  # None if empty.

    def __init__(
        self,
        capacity: int | None = ...,
        length: int | None = ...,
        internalArray: type[POINTER(Clay_ElementId)] | None = ...,
    ) -> None: ...

class Clay_CornerRadius(Structure):
    """Controls the "radius", or corner rounding of elements."""

    topLeft: float
    topRight: float
    bottomLeft: float
    bottomRight: float

    def __init__(
        self,
        topLeft: float | None = ...,
        topRight: float | None = ...,
        bottomLeft: float | None = ...,
        bottomRight: float | None = ...,
    ) -> None: ...

# --- Element Configs ---
# see _clay_enums.py for enums

class Clay_ChildAlignment(Structure):
    """Controls how child elements are aligned on each axis."""

    x: LayoutAlignmentX
    y: LayoutAlignmentY

    def __init__(
        self,
        x: LayoutAlignmentX | None = ...,
        y: LayoutAlignmentY | None = ...,
    ) -> None: ...

class Clay_SizingMinMax(Structure):
    """Controls minimum and maximum size of an element in pixels."""

    min: float
    max: float

    # ruff: disable[A002]
    def __init__(
        self,
        min: float | None = ...,
        max: float | None = ...,
    ) -> None: ...
    # ruff: enable[A002]

class Clay_SizingAxis(Structure):
    """Controls the sizing of an element along one axis inside its parent container."""
    class _U(Union):
        minMax: Clay_SizingMinMax
        percent: float  # 0-1 range. Percent of parent's space the element can occupy.

        def __init__(
            self,
            minMax: Clay_SizingMinMax | None = ...,
            percent: float | None = ...,
        ) -> None: ...

    size: _U
    type: SizingType

    def __init__(
        self,
        size: _U | None = ...,
        type: SizingType | None = ...,  # noqa: A002
    ) -> None: ...

class Clay_Sizing(Structure):
    """Controls the sizing of an element along one axis inside its parent container."""

    width: Clay_SizingAxis
    height: Clay_SizingAxis

    def __init__(
        self,
        width: Clay_SizingAxis | None = ...,
        height: Clay_SizingAxis | None = ...,
    ) -> None: ...

class Clay_Padding(Structure):
    """Controls the padding (gap between the bounding box and children) in pixels."""

    left: int
    right: int
    top: int
    bottom: int

    def __init__(
        self,
        left: int | None = ...,
        right: int | None = ...,
        top: int | None = ...,
        bottom: int | None = ...,
    ) -> None: ...

class Clay_LayoutConfig(Structure):
    """Controls the layout of an element and its children."""

    sizing: Clay_Sizing  # Sizing of this element inside its parent container.
    padding: Clay_Padding  # Padding between this element's border and its children.
    childGap: int  # Gap between children in pixels along the child layout axis.
    childAlignment: Clay_ChildAlignment
    layoutDirection: LayoutDirection

    def __init__(
        self,
        sizing: Clay_Sizing | None = ...,
        padding: Clay_Padding | None = ...,
        childGap: int | None = ...,
        childAlignment: Clay_ChildAlignment | None = ...,
        layoutDirection: LayoutDirection | None = ...,
    ) -> None: ...

class Clay_TextElementConfig(Structure):
    """Controls text elements.

    Settings related to fonts are passed to Clay_MeasureText to actually measure the
    text in pixels.
    """

    userData: c_void_p | None  # Pointer transparently passed to the renderer.
    textColor: Clay_Color
    fontId: int  # Integer transparently passed to Clay_MeasureText.
    fontSize: int
    letterSpacing: int
    lineHeight: int
    wrapMode: TextElementConfigWrapMode
    textAlignment: TextAlignment

    def __init__(
        self,
        userData: c_void_p | None = ...,
        textColor: Clay_Color | None = ...,
        fontId: int | None = ...,
        fontSize: int | None = ...,
        letterSpacing: int | None = ...,
        lineHeight: int | None = ...,
        wrapMode: TextElementConfigWrapMode | None = ...,
        textAlignment: TextAlignment | None = ...,
    ) -> None: ...

# --- Aspect Ratio ---

class Clay_AspectRatioElementConfig(Structure):
    """Controls elements which are scaled by the aspect ratio."""

    aspectRatio: float  # Represents target aspect ratio: final width / final height.

    def __init__(
        self,
        aspectRatio: float | None = ...,
    ) -> None: ...

# --- Image ---

class Clay_ImageElementConfig(Structure):
    """Controls image elements."""

    imageData: c_void_p | None  # Transparent pointer passed to the renderer.

    def __init__(
        self,
        imageData: c_void_p | None = ...,
    ) -> None: ...

# --- Floating ---

class Clay_FloatingAttachPoints(Structure):
    """Controls where a floating element is offset relative to its parent."""

    element: FloatingAttachPointType  # Origin point that gets attached to parent.
    parent: FloatingAttachPointType  # Point on parent the element is attached to.

    def __init__(
        self,
        element: FloatingAttachPointType | None = ...,
        parent: FloatingAttachPointType | None = ...,
    ) -> None: ...

class Clay_FloatingElementConfig(Structure):
    """Controls floating elements."""

    offset: Clay_Vector2  # Offset relative from element's attachPoints.
    expand: Clay_Dimensions  # Expand boundaries without affecting children.
    parentId: int  # Attach element to parent if attaching via ID.
    zIndex: int  # Sorted in ascending order. Passed to the renderer.
    attachPoints: Clay_FloatingAttachPoints
    pointerCaptureMode: PointerCaptureMode
    attachTo: FloatingAttachToElement  # How the floating element is attached.
    clipTo: FloatingClipToElement

    def __init__(
        self,
        offset: Clay_Vector2 | None = ...,
        expand: Clay_Dimensions | None = ...,
        parentId: int | None = ...,
        zIndex: int | None = ...,
        attachPoints: Clay_FloatingAttachPoints | None = ...,
        pointerCaptureMode: PointerCaptureMode | None = ...,
        attachTo: FloatingAttachToElement | None = ...,
        clipTo: FloatingClipToElement | None = ...,
    ) -> None: ...

# --- Custom ---

class Clay_CustomElementConfig(Structure):
    """Controls custom elements. Generates *CUSTOM render commands."""

    customData: c_void_p | None  # Transparent pointer passed to the renderer.

    def __init__(
        self,
        customData: c_void_p | None = ...,
    ) -> None: ...

# --- Scroll ---

class Clay_ClipElementConfig(Structure):
    """Controls the scrolling axis of an element.

    Overflowing elements in the specified direction get clipped, which allows for
    scrolling in that direction.
    """

    horizontal: bool
    vertical: bool
    childOffset: Clay_Vector2  # Offset positions of all children.

    def __init__(
        self,
        horizontal: bool | None = ...,
        vertical: bool | None = ...,
        childOffset: Clay_Vector2 | None = ...,
    ) -> None: ...

# --- Border ---

class Clay_BorderWidth(Structure):
    """Controls the widths of individual element borders.

    Also creates borders with specified width between children elements, if specified.
    Borders between children are created depending on the layoutDirection:
      - if "left to right", borders will be vertical lines
      - if "top to bottom", borders will be horizontal lines
    betweenChildren borders will result in individual RECTANGLE render commands.
    """

    left: int
    right: int
    top: int
    bottom: int
    betweenChildren: int

    def __init__(
        self,
        left: int | None = ...,
        right: int | None = ...,
        top: int | None = ...,
        bottom: int | None = ...,
        betweenChildren: int | None = ...,
    ) -> None: ...

class Clay_BorderElementConfig(Structure):
    """Controls element borders."""

    color: Clay_Color  # Color of all borders with width > 0.
    width: Clay_BorderWidth

    def __init__(
        self,
        color: Clay_Color | None = ...,
        width: Clay_BorderWidth | None = ...,
    ) -> None: ...

# --- Transitions ---

class Clay_TransitionData(Structure):
    """Controls properties that are modified in a transition."""

    boundingBox: Clay_BoundingBox
    backgroundColor: Clay_Color
    overlayColor: Clay_Color
    borderColor: Clay_Color
    borderWidth: Clay_BorderWidth

    def __init__(
        self,
        boundingBox: Clay_BoundingBox | None = ...,
        backgroundColor: Clay_Color | None = ...,
        overlayColor: Clay_Color | None = ...,
        borderColor: Clay_Color | None = ...,
        borderWidth: Clay_BorderWidth | None = ...,
    ) -> None: ...

class Clay_TransitionCallbackArguments(Structure):
    """Arguments to pass to a transition function (?)."""

    transitionState: TransitionState  # Current transition state.
    initial: Clay_TransitionData  # Initial settings before the transition.
    current: type[POINTER(Clay_TransitionData)] | None  # Current (changing) data.
    target: Clay_TransitionData  # Target settings after the transition.
    elapsedTime: float
    duration: float
    properties: TransitionProperty

    def __init__(
        self,
        transitionState: TransitionState | None = ...,
        initial: Clay_TransitionData | None = ...,
        current: type[POINTER(Clay_TransitionData)] | None = ...,
        target: Clay_TransitionData | None = ...,
        elapsedTime: float | None = ...,
        duration: float | None = ...,
        properties: TransitionProperty | None = ...,
    ) -> None: ...

class Clay_TransitionElementConfig(Structure):
    """Controls transitions."""
    class _enter(Structure):
        # Clay_TransitionData (*setInitialState)(
        #   Clay_TransitionData targetState,
        #   Clay_TransitionProperty properties
        # )
        setInitialState: type[
            CFUNCTYPE(Clay_TransitionData, Clay_TransitionData, c_uint32)
        ]
        trigger: TransitionEnterTriggerType

        def __init__(
            self,
            setInitialState: type[
                CFUNCTYPE(Clay_TransitionData, Clay_TransitionData, c_uint32)
            ]
            | None = ...,
            trigger: TransitionEnterTriggerType | None = ...,
        ) -> None: ...

    class _exit(Structure):
        # Clay_TransitionData (*setFinalState)(
        #   Clay_TransitionData initialState,
        #   Clay_TransitionProperty properties
        # )
        setFinalState: type[
            CFUNCTYPE(
                Clay_TransitionData,
                Clay_TransitionData,
                c_uint32,
            )
        ]
        trigger: TransitionExitTriggerType
        siblingOrdering: ExitTransitionSiblingOrdering

        def __init__(
            self,
            setFinalState: type[
                CFUNCTYPE(
                    Clay_TransitionData,
                    Clay_TransitionData,
                    c_uint32,
                )
            ]
            | None = ...,
            trigger: TransitionExitTriggerType | None = ...,
            siblingOrdering: ExitTransitionSiblingOrdering | None = ...,
        ) -> None: ...

    handler: type[CFUNCTYPE(c_bool, Clay_TransitionCallbackArguments)]
    duration: float
    properties: TransitionProperty
    interactionHandling: TransitionInteractionHandlingType
    enter: _enter
    exit: _exit

    def __init__(
        self,
        handler: type[CFUNCTYPE(c_bool, Clay_TransitionCallbackArguments)] | None = ...,
        duration: float | None = ...,
        properties: TransitionProperty | None = ...,
        interactionHandling: TransitionInteractionHandlingType | None = ...,
        enter: _enter | None = ...,
        exit: _exit | None = ...,  # noqa: A002
    ) -> None: ...

# --- Render Command data ---

class Clay_TextRenderData(Structure):
    """Render command data when type is TEXT."""

    stringContents: Clay_StringSlice  # String slice containing the text to be rendered.
    textColor: Clay_Color
    fontId: int  # Transparently passed to the renderer.
    fontSize: int
    letterSpacing: int
    lineHeight: int

    def __init__(
        self,
        stringContents: Clay_StringSlice | None = ...,
        textColor: Clay_Color | None = ...,
        fontId: int | None = ...,
        fontSize: int | None = ...,
        letterSpacing: int | None = ...,
        lineHeight: int | None = ...,
    ) -> None: ...

class Clay_RectangleRenderData(Structure):
    """Render command data when is RECTANGLE."""

    backgroundColor: Clay_Color  # Color to fill the rectangle with.
    cornerRadius: Clay_CornerRadius

    def __init__(
        self,
        backgroundColor: Clay_Color | None = ...,
        cornerRadius: Clay_CornerRadius | None = ...,
    ) -> None: ...

class Clay_ImageRenderData(Structure):
    """Render command data when type is IMAGE."""

    backgroundColor: Clay_Color  # Tint color for the image. 0,0,0,0 should mean no tint
    cornerRadius: Clay_CornerRadius
    imageData: c_void_p | None  # Transparently passed to the renderer.

    def __init__(
        self,
        backgroundColor: Clay_Color | None = ...,
        cornerRadius: Clay_CornerRadius | None = ...,
        imageData: c_void_p | None = ...,
    ) -> None: ...

class Clay_CustomRenderData(Structure):
    """Render command data when type is CUSTOM.

    Every field is transparently passed to the renderer.
    """

    backgroundColor: Clay_Color
    cornerRadius: Clay_CornerRadius
    imageData: c_void_p | None

    def __init__(
        self,
        backgroundColor: Clay_Color | None = ...,
        cornerRadius: Clay_CornerRadius | None = ...,
        imageData: c_void_p | None = ...,
    ) -> None: ...

class Clay_ClipRenderData(Structure):
    """Render command data when type is SCISSOR_START or SCISSOR_END."""

    horizontal: bool
    vertical: bool

    def __init__(
        self,
        horizontal: bool | None = ...,
        vertical: bool | None = ...,
    ) -> None: ...

class Clay_OverlayColorRenderData(Structure):
    """Render command data when type is OVERLAY_START or OVERLAY_END."""

    color: Clay_Color

    def __init__(
        self,
        color: Clay_Color | None = ...,
    ) -> None: ...

class Clay_BorderRenderData(Structure):
    """Render command data when type is BORDER."""

    color: Clay_Color
    cornerRadius: Clay_CornerRadius
    width: Clay_BorderWidth

    def __init__(
        self,
        color: Clay_Color | None = ...,
        cornerRadius: Clay_CornerRadius | None = ...,
        width: Clay_BorderWidth | None = ...,
    ) -> None: ...

class Clay_RenderData(Union):
    """Union of structs containing data specific to a render command."""

    rectangle: Clay_RectangleRenderData
    text: Clay_TextRenderData
    image: Clay_ImageRenderData
    custom: Clay_CustomRenderData
    border: Clay_BorderRenderData
    clip: Clay_ClipRenderData
    overlayColor: Clay_OverlayColorRenderData

    def __init__(
        self,
        rectangle: Clay_RectangleRenderData | None = ...,
        text: Clay_TextRenderData | None = ...,
        image: Clay_ImageRenderData | None = ...,
        custom: Clay_CustomRenderData | None = ...,
        border: Clay_BorderRenderData | None = ...,
        clip: Clay_ClipRenderData | None = ...,
        overlayColor: Clay_OverlayColorRenderData | None = ...,
    ) -> None: ...

class Clay_RenderCommand(Structure):
    """Represents a render command sent to a renderer."""

    boundingBox: Clay_BoundingBox  # Bounding box with position relative to layour root.
    renderData: Clay_RenderData  # Render data specific to current commandType.
    userData: c_void_p | None  # Transparently passed to the renderer.
    id: int  # ID of the element, transparently passed to the renderer.
    zIndex: int  # Final z order to draw the command correctly.
    commandType: RenderCommandType  # Specifies how to handle the command.

    def __init__(
        self,
        boundingBox: Clay_BoundingBox | None = ...,
        renderData: Clay_RenderData | None = ...,
        userData: c_void_p | None = ...,
        id: int | None = ...,  # noqa: A002
        zIndex: int | None = ...,
        commandType: RenderCommandType | None = ...,
    ) -> None: ...

class Clay_RenderCommandArray(Structure):
    """Sized array of Clay_RenderCommand."""

    capacity: int
    length: int
    internalArray: type[POINTER(Clay_RenderCommand)] | None

    def __init__(
        self,
        capacity: int | None = ...,
        length: int | None = ...,
        internalArray: type[POINTER(Clay_RenderCommand)] | None = ...,
    ) -> None: ...

# --- Miscellaneous Structs ---

class Clay_ScrollContainerData(Structure):
    """Represents the current internal state of a scrolling element."""

    scrollPosition: type[POINTER(Clay_Vector2)]  # Real internal scroll position.
    scrollContainerDimensions: Clay_Dimensions
    contentDimensions: Clay_Dimensions
    config: Clay_ClipElementConfig
    found: bool

    def __init__(
        self,
        scrollPosition: type[POINTER(Clay_Vector2)] | None = ...,
        scrollContainerDimensions: Clay_Dimensions | None = ...,
        contentDimensions: Clay_Dimensions | None = ...,
        config: Clay_ClipElementConfig | None = ...,
        found: bool | None = ...,
    ) -> None: ...

class Clay_ElementData(Structure):
    """Data for a specific UI element."""

    boundingBox: Clay_BoundingBox  # Bounding box with position relative to layour root.
    found: bool

    def __init__(
        self,
        boundingBox: Clay_BoundingBox | None = ...,
        found: bool | None = ...,
    ) -> None: ...

class Clay_PointerData(Structure):
    """Information on the current state of pointer interaction."""

    position: Clay_Vector2  # Position of the pointer relative to layout root.
    state: PointerDataInteractionState  # State in the current frame.

    def __init__(
        self,
        position: Clay_Vector2 | None = ...,
        state: PointerDataInteractionState | None = ...,
    ) -> None: ...

class Clay_ElementDeclaration(Structure):
    """Declaration of an element."""

    layout: Clay_LayoutConfig  # Layout of the element and its children.
    backgroundColor: Clay_Color  # If nothing else set, color of resulting rectangle.
    overlayColor: Clay_Color  # Color to overlay on the elemt and its children.
    cornerRadius: Clay_CornerRadius
    aspectRatio: Clay_AspectRatioElementConfig  # Desired aspect ratio of the element.
    floating: Clay_FloatingElementConfig  # Controls how the elemnt floats above others.
    custom: Clay_CustomElementConfig  # Configuration for CUSTOM render commands.
    clip: Clay_ClipElementConfig  # Controls content clipping of the element.
    border: Clay_BorderElementConfig
    transition: Clay_TransitionElementConfig
    userData: c_void_p | None  # Transparently passed to the renderer.

    def __init__(
        self,
        layout: Clay_LayoutConfig | None = ...,
        backgroundColor: Clay_Color | None = ...,
        overlayColor: Clay_Color | None = ...,
        cornerRadius: Clay_CornerRadius | None = ...,
        aspectRatio: Clay_AspectRatioElementConfig | None = ...,
        floating: Clay_FloatingElementConfig | None = ...,
        custom: Clay_CustomElementConfig | None = ...,
        clip: Clay_ClipElementConfig | None = ...,
        border: Clay_BorderElementConfig | None = ...,
        transition: Clay_TransitionElementConfig | None = ...,
        userData: c_void_p | None = ...,
    ) -> None: ...

# --- Errors ---

class Clay_ErrorData(Structure):
    """Data to identify the error that clay has encountered."""

    errorType: ErrorType  # Error encountered while computing layout.
    errorText: Clay_String  # Human-readable error text.
    userData: c_void_p | None  # Transparently passed from the first error handler.

    def __init__(
        self,
        errorType: ErrorType | None = ...,
        errorText: Clay_String | None = ...,
        userData: c_void_p | None = ...,
    ) -> None: ...

class Clay_ErrorHandler(Structure):
    """Wrapper struct around Clay's error handler function."""

    errorHandlerFunction: type[CFUNCTYPE(None, Clay_ErrorData)]  # User-provided.
    userData: c_void_p | None  # Transparently passed to the error handler.

    def __init__(
        self,
        errorHandlerFunction: type[CFUNCTYPE(None, Clay_ErrorData)] | None = ...,
        userData: c_void_p | None = ...,
    ) -> None: ...

# ruff: enable[N801,N803,N815]
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
"""User-defined callback called when the pointer enters an element's bounding box."""

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
"""User-defined callback called by Clay to calculate the dimensions of text."""

# Clay_Vector2 (*queryScrollOffsetFunction)(
#   uint32_t elementId,
#   void *userData
# )
queryScrollOffsetFunction = CFUNCTYPE(
    Clay_Vector2,
    c_uint32,
    c_void_p,
)
"""(EXPERIMENTAL) called for external scroll offset queries."""

# Via: Clay_ErrorHandler
# void (*errorHandlerFunction)(Clay_ErrorData errorText)
errorHandlerFunction = CFUNCTYPE(None, Clay_ErrorData)
"""User-defined callback called when Clay encounters an error."""

# Via: Clay_TransitionElementConfig
# bool (*handler)(Clay_TransitionCallbackArguments arguments)
transitionHandlerFunction = CFUNCTYPE(c_bool, Clay_TransitionCallbackArguments)
"""User-defined callback to handle transitions (?)."""

# ruff: enable[N816]
