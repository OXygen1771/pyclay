"""Low-level bindings for the Clay library using ctypes."""

import ctypes
import importlib.util
from ctypes import (
    CDLL,
    c_size_t,
    c_uint32,
    c_voidp,
)
from importlib.machinery import ModuleSpec

from pyclay import _clay_types


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

        # --- Memory ---
        lib.Clay_MinMemorySize.argtypes = []
        lib.Clay_MinMemorySize.restype = c_uint32

        lib.Clay_CreateArenaWithCapacityAndMemory.argtypes = [c_size_t, c_voidp]
        lib.Clay_CreateArenaWithCapacityAndMemory.restype = _clay_types.Clay_Arena

    @property
    def lib(self) -> CDLL:
        return self._lib


# singleton library instance. couldn't think of a better way to do it...
_clay: _ClayLib = _ClayLib()
_lib: CDLL = _clay.lib


def clay_min_memory_size() -> int:
    """Return the minimum amount of memory in bytes that Clay requires.

    :return: Number of bytes required by Clay under current settings.
    :rtype: int
    """
    return _lib.Clay_MinMemorySize()
