"""Pytest shared test fixtures."""

import ctypes

import pytest

from pyclay._clay import _lib as clay_lib_module
from pyclay._clay import _types as ct

# --- BASIC ---


@pytest.fixture(scope="session")
def clay_lib() -> ctypes.CDLL:
    """Provide a loaded Clay library."""
    return clay_lib_module._lib


@pytest.fixture
def initialized_clay(
    clay_lib: ctypes.CDLL,
    arena_memory: tuple[ct.Clay_Arena, ctypes.Array[ctypes.c_char]],
) -> tuple[ct.Clay_Arena, ctypes.Array[ctypes.c_char]]:
    """Initialize Clay with a given arena and return the arena and memory.

    Also define a raising error handler, which raises exceptions as soon as clay
    encounters an error.

    :param clay_lib: Initialized Clay library.
    :type clay_lib: CDLL
    :param arena: Arena and allocated bytes.
    :type arena: tuple[Clay_Arena, Array[c_char]]
    :return: Same as the `arena` parameter.
    :rtype: tuple[Clay_Arena, Array[c_char]]
    """
    arena_struct, mem = arena_memory

    from pyclay._clay._enums import Clay_ErrorType

    @ctypes.CFUNCTYPE(None, ct.Clay_ErrorData)
    def raise_handler(error_data: ct.Clay_ErrorData) -> None:
        e_type: Clay_ErrorType = error_data.errorType
        if error_data.errorText.chars:
            e_text: str = error_data.errorText.chars.decode("utf-8")
        else:
            e_text: str = "<no error text provided>"
        raise RuntimeError(f"{e_type}: {e_text}")

    error_handler = ct.Clay_ErrorHandler(
        errorHandlerFunction=raise_handler,
        userData=ctypes.c_void_p(),
    )

    clay_lib.Clay_Initialize(
        arena_struct,
        ct.Clay_Dimensions(width=800, height=600),
        error_handler,
    )

    # clay doesn't provide a deinitialize function.
    return arena_struct, mem


# --- MEMORY ---


@pytest.fixture
def min_memory_size() -> int:
    """Return the minimum amount of memory in bytes that Clay requires.

    :return: Amount of bytes Clay needs to operate.
    :rtype: int
    """
    min_mem: int = clay_lib_module.clay_min_memory_size()
    assert min_mem > 0
    return min_mem


@pytest.fixture
def arena_memory(
    clay_lib: ctypes.CDLL,
    min_memory_size: int,
) -> tuple[ct.Clay_Arena, ctypes.Array[ctypes.c_char]]:
    """Return an allocated buffer for a Clay arena with a size of min_mem_size.

    :param clay_lib: Initialized Clay library.
    :type clay_lib: CDLL
    :param min_memory_size: Amount of bytes to allocate.
    :type min_memory_size: int
    :return: Arena and allocated bytes.
    :rtype: tuple[Clay_Arena, Array[c_char]]
    """
    mem: ctypes.Array[ctypes.c_char] = (ctypes.c_char * min_memory_size)()
    arena: ct.Clay_Arena = clay_lib.Clay_CreateArenaWithCapacityAndMemory(
        min_memory_size,
        ctypes.cast(mem, ctypes.c_void_p),
    )
    # notice that we save a reference to mem so it doesn't get deallocated
    return arena, mem
