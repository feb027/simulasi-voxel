"""Block property registry.

Centralised lookup for per-block-type properties such as hardness.
Designed to be extended with tool speed modifiers, drops, etc.
"""
from __future__ import annotations

from src.world import AIR, GRASS, DIRT, STONE

# Hardness values in seconds (base mining duration without tool modifiers).
BLOCK_HARDNESS: dict[int, float] = {
    AIR: 0.0,
    GRASS: 1.0,
    DIRT: 0.8,
    STONE: 2.5,
}

# Fallback hardness when a block type is not registered.
_DEFAULT_HARDNESS = 1.5


def get_hardness(block_id: int) -> float:
    """Return the base hardness (seconds) for *block_id*."""
    return BLOCK_HARDNESS.get(block_id, _DEFAULT_HARDNESS)


def get_mining_duration(block_id: int, tool_speed: float = 1.0) -> float:
    """Return effective mining duration after applying *tool_speed*.

    A *tool_speed* of 2.0 halves the duration, etc.
    """
    speed = max(tool_speed, 0.01)  # avoid division by zero
    return get_hardness(block_id) / speed
