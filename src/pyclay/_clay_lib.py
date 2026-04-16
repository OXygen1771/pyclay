"""Low-level bindings for the Clay library using ctypes."""

import ctypes
import importlib.util
from ctypes import (
    CDLL,
    CFUNCTYPE,
    POINTER,
    _CFunctionType,
    _Pointer,
    c_bool,
    c_float,
    c_int32,
    c_size_t,
    c_uint32,
    c_void_p,
)
from importlib.machinery import ModuleSpec

from pyclay import _clay_types as ct
from pyclay._clay_types import Clay_ElementData, Clay_RenderCommand


class _ClayLib:
    """Clay library provider."""

    def __init__(self) -> None:
        self._lib: CDLL = self._load_library()
        self._define_functions()

    def _load_library(self) -> CDLL:
        """Load an already compiled clay library.

        :raises RuntimeError: If _claylib (a build of clay) can't be found,
            the library can't be loaded.
        :return: Instance of the Clay library.
        :rtype: CDLL
        """
        module: str = "pyclay._claylib"
        spec: ModuleSpec | None = importlib.util.find_spec(module)

        if spec and spec.origin:
            return CDLL(spec.origin)

        raise RuntimeError(
            "Could not find the compiled clay library! "
            "Try running: uv pip install -e .",
        )

    def _define_functions(self) -> None:
        """Define function signatures for all Clay functions."""
        lib: ctypes.CDLL = self._lib

        # --- Public API ---

        lib.Clay_MinMemorySize.argtypes = []
        lib.Clay_MinMemorySize.restype = c_uint32

        lib.Clay_CreateArenaWithCapacityAndMemory.argtypes = [c_size_t, c_void_p]
        lib.Clay_CreateArenaWithCapacityAndMemory.restype = ct.Clay_Arena

        lib.Clay_SetPointerState.argtypes = [ct.Clay_Vector2, c_bool]
        lib.Clay_SetPointerState.restype = None

        lib.Clay_GetPointerState.argtypes = []
        lib.Clay_GetPointerState.restype = ct.Clay_PointerData

        lib.Clay_Initialize.argtypes = [
            ct.Clay_Arena,
            ct.Clay_Dimensions,
            ct.Clay_ErrorHandler,
        ]
        lib.Clay_Initialize.restype = POINTER(ct.Clay_Context)

        lib.Clay_GetCurrentContext.argtypes = []
        lib.Clay_GetCurrentContext.restype = POINTER(ct.Clay_Context)

        lib.Clay_SetCurrentContext.argtypes = [POINTER(ct.Clay_Context)]
        lib.Clay_SetCurrentContext.restype = None

        lib.Clay_UpdateScrollContainers.argtypes = [c_bool, ct.Clay_Vector2, c_float]
        lib.Clay_UpdateScrollContainers.restype = None

        lib.Clay_GetScrollOffset.argtypes = []
        lib.Clay_GetScrollOffset.restype = ct.Clay_Vector2

        lib.Clay_SetLayoutDimensions.argtypes = [ct.Clay_Dimensions]
        lib.Clay_SetLayoutDimensions.restype = None

        lib.Clay_BeginLayout.argtypes = []
        lib.Clay_BeginLayout.restype = None

        lib.Clay_EndLayout.argtypes = [c_float]
        lib.Clay_EndLayout.restype = ct.Clay_RenderCommandArray

        lib.Clay_GetOpenElementId.argtypes = []
        lib.Clay_GetOpenElementId.restype = c_uint32

        lib.Clay_GetElementId.argtypes = [ct.Clay_String]
        lib.Clay_GetElementId.restype = ct.Clay_ElementId

        lib.Clay_GetElementIdWithIndex.argtypes = [ct.Clay_String, c_uint32]
        lib.Clay_GetElementIdWithIndex.restype = ct.Clay_ElementId

        lib.Clay_GetElementData.argtypes = [ct.Clay_ElementId]
        lib.Clay_GetElementData.restype = ct.Clay_ElementData

        lib.Clay_Hovered.argtypes = []
        lib.Clay_Hovered.restype = c_bool

        lib.Clay_OnHover.argtypes = [onHoverFunction, c_void_p]
        lib.Clay_OnHover.restype = None

        lib.Clay_PointerOver.argtypes = [ct.Clay_ElementId]
        lib.Clay_PointerOver.restype = c_bool

        lib.Clay_GetPointerOverIds.argtypes = []
        lib.Clay_GetPointerOverIds.restype = ct.Clay_ElementIdArray

        lib.Clay_GetScrollContainerData.argtypes = [ct.Clay_ElementId]
        lib.Clay_GetScrollContainerData.restype = ct.Clay_ScrollContainerData

        lib.Clay_SetMeasureTextFunction.argtypes = [measureTextFunction, c_void_p]
        lib.Clay_SetMeasureTextFunction.restype = None

        lib.Clay_SetQueryScrollOffsetFunction.argtypes = [
            queryScrollOffsetFunction,
            c_void_p,
        ]
        lib.Clay_SetQueryScrollOffsetFunction.restype = None

        lib.Clay_RenderCommandArray_Get.argtypes = [
            ct.Clay_RenderCommandArray,
            c_int32,
        ]
        lib.Clay_RenderCommandArray_Get.restype = POINTER(Clay_RenderCommand)

        lib.Clay_SetDebugModeEnabled.argtypes = [c_bool]
        lib.Clay_SetDebugModeEnabled.restype = None

        lib.Clay_IsDebugModeEnabled.argtypes = []
        lib.Clay_IsDebugModeEnabled.restype = c_bool

        lib.Clay_SetCullingEnabled.argtypes = [c_bool]
        lib.Clay_SetCullingEnabled.restype = None

        lib.Clay_GetMaxElementCount.argtypes = []
        lib.Clay_GetMaxElementCount.restype = c_int32

        lib.Clay_SetMaxElementCount.argtypes = [c_int32]
        lib.Clay_SetMaxElementCount.restype = None

        lib.Clay_GetMaxMeasureTextCacheWordCount.argtypes = []
        lib.Clay_GetMaxMeasureTextCacheWordCount.restype = c_int32

        lib.Clay_SetMaxMeasureTextCacheWordCount.argtypes = [c_int32]
        lib.Clay_SetMaxMeasureTextCacheWordCount.restype = None

        lib.Clay_ResetMeasureTextCache.argtypes = []
        lib.Clay_ResetMeasureTextCache.restype = None

        lib.Clay_EaseOut.argtypes = [ct.Clay_TransitionCallbackArguments]
        lib.Clay_EaseOut.restype = c_bool

        # --- Internal API ---

        lib.Clay__OpenElement.argtypes = []
        lib.Clay__OpenElement.restype = None

        lib.Clay__OpenElementWithId.argtypes = [ct.Clay_ElementId]
        lib.Clay__OpenElementWithId.restype = None

        lib.Clay__ConfigureOpenElement.argtypes = [ct.Clay_ElementDeclaration]
        lib.Clay__ConfigureOpenElement.restype = None

        lib.Clay__ConfigureOpenElementPtr.argtypes = [
            POINTER(ct.Clay_ElementDeclaration),
        ]
        lib.Clay__ConfigureOpenElementPtr.restype = None

        lib.Clay__CloseElement.argtypes = []
        lib.Clay__CloseElement.restype = None

        lib.Clay__HashString.argtypes = [ct.Clay_String, c_uint32]
        lib.Clay__HashString.restype = ct.Clay_ElementId

        lib.Clay__HashStringWithOffset.argtypes = [ct.Clay_String, c_uint32, c_uint32]
        lib.Clay__HashStringWithOffset.restype = ct.Clay_ElementId

        lib.Clay__OpenTextElement.argtypes = [
            ct.Clay_String,
            ct.Clay_TextElementConfig,
        ]
        lib.Clay__OpenTextElement.restype = None

        self._lib = lib

    @property
    def lib(self) -> CDLL:
        return self._lib


# singleton library instance. couldn't think of a better way to do it...
_clay: _ClayLib = _ClayLib()
_lib: CDLL = _clay.lib


# --- Function pointers ---

# void (*onHoverFunction)(
#   Clay_ElementId elementId,
#   Clay_PointerData pointerData,
#   void *userData
# )
onHoverFunction: type[_CFunctionType] = CFUNCTYPE(  # noqa: N816
    None,
    ct.Clay_ElementId,
    ct.Clay_PointerData,
    c_void_p,
)

# Clay_Dimensions (*measureTextFunction)(
#   Clay_StringSlice text,
#   Clay_TextElementConfig *config,
#   void *userData
# )
measureTextFunction: type[_CFunctionType] = CFUNCTYPE(  # noqa: N816
    ct.Clay_Dimensions,
    ct.Clay_StringSlice,
    ct.Clay_TextElementConfig,
    c_void_p,
)

# Clay_Vector2 (*queryScrollOffsetFunction)(
#   uint32_t elementId,
#   void *userData
# )
queryScrollOffsetFunction: type[_CFunctionType] = CFUNCTYPE(  # noqa: N816
    c_uint32,
    ct.Clay_TextElementConfig,
)


# --- Public API functions ---
# Might be sensible to move to a separate file?


def clay_min_memory_size() -> int:
    return _lib.Clay_MinMemorySize()


def clay_create_arena_with_capacity_and_memory(
    capacity: int,
    memory: c_void_p,
) -> ct.Clay_Arena:
    return _lib.Clay_CreateArenaWithCapacityAndMemory(capacity, memory)


def clay_set_pointer_state(position: ct.Clay_Vector2, pointer_down: bool) -> None:
    return _lib.Clay_SetPointerState(position, pointer_down)


def clay_get_pointer_state() -> ct.Clay_PointerData:
    return _lib.Clay_GetPointerState()


def clay_initialize(
    arena: ct.Clay_Arena,
    layout_dimensions: ct.Clay_Dimensions,
    error_handler: ct.Clay_ErrorHandler,
) -> _Pointer[ct.Clay_Context]:
    return _lib.Clay_Initialize(arena, layout_dimensions, error_handler)


def clay_get_current_context() -> _Pointer[ct.Clay_Context]:
    return _lib.Clay_GetCurrentContext()


def clay_set_current_context(context: _Pointer[ct.Clay_Context]) -> None:
    return _lib.Clay_SetCurrentContext(context)


def clay_update_scroll_containers(
    enable_drag_scrolling: bool,
    scroll_delta: ct.Clay_Vector2,
    delta_time: float,
) -> None:
    return _lib.Clay_UpdateScrollContainers(
        enable_drag_scrolling,
        scroll_delta,
        delta_time,
    )


def clay_get_scroll_offset() -> ct.Clay_Vector2:
    return _lib.Clay_GetScrollOffset()


def clay_set_layout_dimensions(dimensions: ct.Clay_Dimensions) -> None:
    return _lib.Clay_SetLayoutDimensions(dimensions)


def clay_begin_layout() -> None:
    return _lib.Clay_BeginLayout()


def clay_end_layout(delta_time: float) -> ct.Clay_RenderCommandArray:
    return _lib.Clay_EndLayout(delta_time)


def clay_get_open_element_id() -> int:
    return _lib.Clay_GetOpenElementId()


def clay_get_element_id(id_string: ct.Clay_String) -> ct.Clay_ElementId:
    return _lib.Clay_GetElementId(id_string)


def clay_get_element_id_with_index(
    id_string: ct.Clay_String,
    index: int,
) -> ct.Clay_ElementId:
    return _lib.Clay_GetElementIdWithIndex(id_string, index)


def clay_get_element_data(element_id: ct.Clay_ElementId) -> Clay_ElementData:
    return _lib.Clay_GetElementData(element_id)


def clay_hovered() -> bool:
    return _lib.Clay_Hovered()


def clay_on_hover(on_hover_callback, user_data: c_void_p) -> None:
    callback: _CFunctionType = onHoverFunction(on_hover_callback)
    return _lib.Clay_OnHover(callback, user_data)


def clay_pointer_over(element_id: ct.Clay_ElementId) -> bool:
    return _lib.Clay_PointerOver(element_id)


def clay_get_pointer_over_ids() -> ct.Clay_ElementIdArray:
    return _lib.Clay_GetPointerOverIds()


def clay_get_scroll_container_data(
    element_id: ct.Clay_ElementId,
) -> ct.Clay_ScrollContainerData:
    return _lib.Clay_GetScrollContainerData(element_id)


def clay_set_measure_text_function(measure_text_callback, user_data: c_void_p) -> None:
    callback: _CFunctionType = measureTextFunction(measure_text_callback)
    return _lib.Clay_SetMeasureTextFunction(callback, user_data)


def clay_set_query_scroll_offset_function(
    query_scroll_offset_callback,
    user_data: c_void_p,
) -> None:
    callback: _CFunctionType = queryScrollOffsetFunction(query_scroll_offset_callback)
    return _lib.Clay_SetQueryScrollOffsetFunction(callback, user_data)


def clay_render_command_array_get(
    array: _Pointer[ct.Clay_RenderCommandArray],
    index: int,
) -> _Pointer[ct.Clay_RenderCommand]:
    return _lib.Clay_RenderCommandArray_Get(array, index)


def clay_set_debug_mode_enabled(enabled: bool) -> None:
    return _lib.Clay_SetDebugModeEnabled(enabled)


def clay_is_debug_mode_enabled() -> bool:
    return _lib.Clay_IsDebugModeEnabled()


def clay_set_culling_enabled(enabled: bool) -> None:
    return _lib.Clay_SetCullingEnabled(enabled)


def clay_get_max_element_count() -> int:
    return _lib.Clay_GetMaxElementCount()


def clay_set_max_element_count(max_element_count: int) -> None:
    return _lib.Clay_SetMaxElementCount(max_element_count)


def clay_get_max_measure_text_cache_word_count() -> int:
    return _lib.Clay_GetMaxMeasureTextCacheWordCount()


def clay_set_max_measure_text_cache_word_count(
    max_measure_text_cache_word_count: int,
) -> None:
    return _lib.Clay_SetMaxMeasureTextCacheWordCount(max_measure_text_cache_word_count)


def clay_reset_measure_text_cache() -> None:
    return _lib.Clay_ResetMeasureTextCache()


def clay_ease_out(arguments: ct.Clay_TransitionCallbackArguments) -> bool:
    return _lib.Clay_EaseOut(arguments)


# --- Internal API functions ---


def clay__open_element() -> None:
    return _lib.Clay__OpenElement()


def clay__open_element_with_id(element_id: ct.Clay_ElementId) -> None:
    return _lib.Clay__OpenElementWithId(element_id)


def clay__configure_open_element(config: ct.Clay_ElementDeclaration) -> None:
    return _lib.Clay__ConfigureOpenElement(config)


def clay__configure_open_element_ptr(
    config_ptr: _Pointer[ct.Clay_ElementDeclaration],
) -> None:
    return _lib.Clay__ConfigureOpenElementPtr(config_ptr)


def clay__hash_string(key: ct.Clay_String, seed: int) -> ct.Clay_ElementId:
    return _lib.Clay__HashString(key, seed)


def clay__hash_string_with_offset(
    key: ct.Clay_String,
    offset: int,
    seed: int,
) -> ct.Clay_ElementId:
    return _lib.Clay__HashStringWithOffset(key, offset, seed)


def clay__open_text_element(
    text: ct.Clay_String,
    text_config: ct.Clay_TextElementConfig,
) -> None:
    return _lib.Clay__OpenTextElement(text, text_config)
