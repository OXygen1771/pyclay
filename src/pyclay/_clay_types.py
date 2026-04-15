"""Clay structures."""

from ctypes import Structure, c_char_p, c_size_t, c_uint64

# ruff: disable[N801]


class Clay_Arena(Structure):
    """Memory arena structure to manage clay's internal allocations."""

    _fields_ = [
        # uintptr_t ~= uint64_t on most platforms, so...
        ("nextAllocation", c_uint64),
        ("capacity", c_size_t),
        ("memory", c_char_p),
    ]


# ruff: enable[N801]
