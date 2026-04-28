"""Test validation functions for the clay structure factories."""

import pytest


def test_handle_validation_errors(validation_enabled_mode: None) -> None:
    """Test that validation errors get raised."""
    _v: None = validation_enabled_mode

    from pyclay._clay.factories import _handle_validation_errors, set_error_callback

    with pytest.raises(ValueError, match="Test"):
        _handle_validation_errors("Test")

    def handle_err(msg: str) -> bool:
        print(f"Handled error: {msg}")
        return True

    def no_handle_err(msg: str) -> bool:
        print(f"Not handled error: {msg}")
        return False

    set_error_callback(handle_err)
    _handle_validation_errors("Error to be handled")

    set_error_callback(no_handle_err)
    with pytest.raises(ValueError, match=r"Error not to be handled"):
        _handle_validation_errors("Error not to be handled")


def test_check_enum_and_enum_flag(validation_enabled_mode: None) -> None:
    """Test that Enum and EnumFlag validation works."""
    _v: None = validation_enabled_mode

    from pyclay._clay.factories import _check_enum_flag_value, _check_enum_value
    from pyclay.enums import LayoutDirection, TransitionProperty

    with pytest.raises(ValueError, match=r"layout dir*"):
        _check_enum_value(-1, LayoutDirection, "layout dir")
    _check_enum_value(LayoutDirection.default(), LayoutDirection, "layout dir")

    with pytest.raises(ValueError, match=r"transition*"):
        _check_enum_flag_value(-1, TransitionProperty, "transition")
    _check_enum_flag_value(
        TransitionProperty.default(),
        TransitionProperty,
        "transition",
    )


def test_check_number_types(validation_enabled_mode: None) -> None:
    """Test that int/uint, float and size_t vaildation works."""
    _v: None = validation_enabled_mode

    from pyclay._clay.factories import (
        _check_float_0_to_1,
        _check_float_nonnegative,
        _check_int16,
        _check_int32,
        _check_size_t,
        _check_uint8,
        _check_uint16,
        _check_uint32,
        _check_uint64,
    )

    with pytest.raises(ValueError, match=r"uint*"):
        _check_uint8(-1, "uint8")
    with pytest.raises(ValueError, match=r"uint*"):
        _check_uint8(2**8, "uint8")
    _check_uint8(1, "uint8")

    with pytest.raises(ValueError, match=r"uint*"):
        _check_uint16(-1, "uint16")
    with pytest.raises(ValueError, match=r"uint*"):
        _check_uint16(2**16, "uint16")
    _check_uint16(1, "uint16")

    with pytest.raises(ValueError, match=r"uint*"):
        _check_uint32(-1, "uint32")
    with pytest.raises(ValueError, match=r"uint*"):
        _check_uint32(2**32, "uint32")
    _check_uint32(1, "uint32")

    with pytest.raises(ValueError, match=r"uint*"):
        _check_uint64(-1, "uint64")
    with pytest.raises(ValueError, match=r"uint*"):
        _check_uint64(2**64, "uint64")
    _check_uint64(1, "uint64")

    with pytest.raises(ValueError, match=r"int*"):
        _check_int16(-(2**15) - 1, "int16")
    with pytest.raises(ValueError, match=r"int*"):
        _check_int16(2**15, "int16")
    _check_int16(1, "int16")

    with pytest.raises(ValueError, match=r"int*"):
        _check_int32(-(2**31) - 1, "int32")
    with pytest.raises(ValueError, match=r"int*"):
        _check_int32(2**31, "int32")
    _check_int32(1, "int32")

    from ctypes import c_size_t, sizeof

    bits: int = 64 if sizeof(c_size_t) == 8 else 32

    with pytest.raises(ValueError, match=r"size_t*"):
        _check_size_t(-1, "size_t")
    with pytest.raises(ValueError, match=r"size_t*"):
        _check_size_t(2**bits, "size_t")
    _check_size_t(1, "size_t")

    with pytest.raises(ValueError, match=r"float*"):
        _check_float_nonnegative(-1, "float")
    _check_float_nonnegative(1, "float")

    with pytest.raises(ValueError, match=r"float*"):
        _check_float_0_to_1(-1, "float")
    with pytest.raises(ValueError, match=r"float*"):
        _check_float_0_to_1(1.1, "float")
    _check_float_0_to_1(0, "float")
    _check_float_0_to_1(1, "float")


def test_no_validation() -> None:
    """Test that no errors get thrown with validation disabled."""
    from pyclay._clay.factories import (
        _check_enum_flag_value,
        _check_enum_value,
        _check_float_0_to_1,
        _check_float_nonnegative,
        _check_int16,
        _check_int32,
        _check_size_t,
        _check_uint8,
        _check_uint16,
        _check_uint32,
        _check_uint64,
        set_validation_enabled,
    )

    set_validation_enabled(False)

    from pyclay.enums import LayoutDirection, TransitionProperty

    _check_enum_value(-1, LayoutDirection, "layout dir")
    _check_enum_flag_value(-1, TransitionProperty, "transition")

    _check_uint8(-1, "uint8")
    _check_uint8(2**8, "uint8")
    _check_uint8(1, "uint8")

    _check_uint16(-1, "uint16")
    _check_uint16(2**16, "uint16")
    _check_uint16(1, "uint16")

    _check_uint32(-1, "uint32")
    _check_uint32(2**32, "uint32")
    _check_uint32(1, "uint32")

    _check_uint64(-1, "uint64")
    _check_uint64(2**64, "uint64")
    _check_uint64(1, "uint64")

    _check_int16(-(2**15) - 1, "int16")
    _check_int16(2**15, "int16")
    _check_int16(1, "int16")

    _check_int32(-(2**31) - 1, "int32")
    _check_int32(2**31, "int32")
    _check_int32(1, "int32")

    from ctypes import c_size_t, sizeof

    bits: int = 64 if sizeof(c_size_t) == 8 else 32

    _check_size_t(-1, "size_t")
    _check_size_t(2**bits, "size_t")
    _check_size_t(1, "size_t")

    _check_float_nonnegative(-1, "float")
    _check_float_nonnegative(1, "float")

    _check_float_0_to_1(-1, "float")
    _check_float_0_to_1(1.1, "float")
    _check_float_0_to_1(0, "float")
    _check_float_0_to_1(1, "float")
