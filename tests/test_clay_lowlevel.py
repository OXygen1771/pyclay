"""Test basic functionality of the lowlevel Clay bindings."""

import ctypes

from pyclay._clay import _types as ct


def test_library_loaded(clay_lib: ctypes.CDLL) -> None:
    """Test that the library is loaded and exports its symbols.

    This should always pass, unless somehow the C compiler breaks.
    """
    assert clay_lib is not None

    assert hasattr(clay_lib, "Clay_MinMemorySize")
    min_memory_size: int = clay_lib.Clay_MinMemorySize()
    assert isinstance(min_memory_size, int)

    from pyclay._clay._lib import clay_min_memory_size

    # also test that the functions do use the same library instance
    min_memory_size_from_func: int = clay_min_memory_size()
    assert min_memory_size == min_memory_size_from_func

    assert min_memory_size > 0


def test_create_arena(
    arena_memory: tuple[ct.Clay_Arena, ctypes.Array[ctypes.c_char]],
) -> None:
    """Test that a Clay_Arena is created corectly.

    This should also always pass, unless Clay itself breaks.
    """
    arena_struct, mem = arena_memory
    assert arena_struct.memory is not None

    expected_capacity: int = len(mem)
    assert arena_struct.capacity == expected_capacity

    # a new allocation should not point to any next allocation
    assert arena_struct.nextAllocation == 0


def test_struct_size(clay_lib: ctypes.CDLL) -> None:
    """Test that some low-level ctypes structures are the expected size."""
    _clay_lib = clay_lib

    from pyclay._clay._types import (
        Clay_ElementId,
        Clay_LayoutConfig,
        Clay_TransitionElementConfig,
    )

    # precalculated
    assert ctypes.sizeof(Clay_ElementId) == 32
    assert ctypes.sizeof(Clay_LayoutConfig) == 40
    # transitions appeared in Clay recently, they are probably subject to change!
    assert ctypes.sizeof(Clay_TransitionElementConfig) == 56


def test_begin_end_layout(
    clay_lib: ctypes.CDLL,
    initialized_clay: tuple[ct.Clay_Arena, ctypes.Array[ctypes.c_char]],
) -> None:
    """Test that Clay can begin and end a layout without errors."""
    _arena_struct, _mem = initialized_clay
    _clay_lib = clay_lib
    from pyclay._clay._lib import clay_begin_layout, clay_end_layout

    clay_begin_layout()
    clay_end_layout(delta_time=0.1)


def test_error_handler(
    clay_lib: ctypes.CDLL,
    arena_memory: tuple[ct.Clay_Arena, ctypes.Array[ctypes.c_char]],
) -> None:
    """Test that a user-defined error handler is called when an error occurs."""
    arena_struct, _mem = arena_memory
    _clay_lib = clay_lib

    from pyclay._clay._enums import Clay_ErrorType

    errors: list[tuple[Clay_ErrorType, str]] = []

    @ctypes.CFUNCTYPE(None, ct.Clay_ErrorData)
    def basic_error_handler(error_data: ct.Clay_ErrorData) -> None:
        e_type: Clay_ErrorType = error_data.errorType
        if error_data.errorText.chars:
            e_text: str = error_data.errorText.chars.decode("utf-8")
        else:
            e_text: str = "<no error text provided>"
        print(f"{e_type}: {e_text}")
        errors.append((e_type, e_text))

    error_handler: ct.Clay_ErrorHandler = ct.Clay_ErrorHandler(
        errorHandlerFunction=basic_error_handler,
        userData=ctypes.c_void_p(),
    )

    from pyclay._clay._lib import clay_end_layout, clay_initialize

    clay_initialize(
        arena=arena_struct,
        layout_dimensions=ct.Clay_Dimensions(width=800, height=600),
        error_handler=error_handler,
    )

    # not beginning a layout should raise an error
    # however, not an unbalanced open/close, but an internal error.
    clay_end_layout(0.1)

    assert len(errors) > 0
    assert errors[0][0] == Clay_ErrorType.CLAY_ERROR_TYPE_INTERNAL_ERROR


def test_simple_element(
    clay_lib: ctypes.CDLL,
    initialized_clay: tuple[ct.Clay_Arena, ctypes.Array[ctypes.c_char]],
) -> None:
    """Test that Clay can create a simple element and generate a render command."""
    _arena_struct, _mem = initialized_clay
    _clay_lib = clay_lib

    from pyclay._clay._enums import Clay_LayoutDirection
    from pyclay._clay._lib import (
        clay__close_element,
        clay__configure_open_element,
        clay__open_element,
        clay_begin_layout,
        clay_end_layout,
    )

    clay_begin_layout()

    # basically what the CLAY macro does
    rect_config: ct.Clay_ElementDeclaration = ct.Clay_ElementDeclaration(
        layout=ct.Clay_LayoutConfig(
            padding=ct.Clay_Padding(16, 16, 12, 12),
            layoutDirection=Clay_LayoutDirection.default(),
        ),
        backgroundColor=ct.Clay_Color(255, 120, 120, 255),
        cornerRadius=ct.Clay_CornerRadius(
            topLeft=16,
            topRight=16,
            bottomLeft=16,
            bottomRight=16,
        ),
        border=ct.Clay_BorderElementConfig(
            color=ct.Clay_Color(10, 10, 10, 255),
            width=ct.Clay_BorderWidth(
                left=10,
                right=10,
                top=5,
                bottom=5,
                betweenChildren=10,
            ),
        ),
    )
    clay__open_element()
    clay__configure_open_element(rect_config)
    clay__close_element()

    render_commands: ct.Clay_RenderCommandArray = clay_end_layout(0.1)

    assert render_commands.length > 0

    # could verify that the commands are, in fact, correct
