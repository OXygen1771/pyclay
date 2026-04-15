"""Pytest shared test fixtures."""

import pytest

from pyclay import _clay_lib as clay


# --- MEMORY ---
@pytest.fixture
def min_memory_size() -> int:
    """Return the minimum amount of memory in bytes that Clay requires."""
    min_mem: int = clay.clay_min_memory_size()

    return min_mem
