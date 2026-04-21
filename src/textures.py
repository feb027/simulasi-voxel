from __future__ import annotations

import numpy as np

from src.world import DIRT, GRASS, STONE

TILE_SIZE = 16
ATLAS_GRID = (2, 2)
ATLAS_WIDTH = TILE_SIZE * ATLAS_GRID[0]
ATLAS_HEIGHT = TILE_SIZE * ATLAS_GRID[1]

TILE_GRASS_TOP = (0, 0)
TILE_DIRT = (1, 0)
TILE_STONE = (0, 1)
TILE_GRASS_SIDE = (1, 1)


def _make_noise(seed: int, base_color: tuple[int, int, int], variation: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    tile = np.zeros((TILE_SIZE, TILE_SIZE, 3), dtype=np.uint8)
    for y in range(TILE_SIZE):
        for x in range(TILE_SIZE):
            noise = rng.integers(-variation, variation + 1, size=3)
            color = np.clip(np.array(base_color) + noise, 0, 255)
            tile[y, x] = color.astype(np.uint8)
    return tile


def _grass_top_tile() -> np.ndarray:
    tile = _make_noise(11, (86, 168, 60), 16)
    for y in range(0, TILE_SIZE, 4):
        tile[y : y + 1, :, 1] = np.clip(tile[y : y + 1, :, 1] + 18, 0, 255)
    return tile


def _dirt_tile() -> np.ndarray:
    tile = _make_noise(17, (124, 88, 52), 14)
    for x in range(1, TILE_SIZE, 5):
        tile[:, x : x + 1] = np.clip(tile[:, x : x + 1] - 10, 0, 255)
    return tile


def _stone_tile() -> np.ndarray:
    tile = _make_noise(23, (136, 140, 148), 12)
    for y in range(2, TILE_SIZE, 5):
        tile[y : y + 1] = np.clip(tile[y : y + 1] + 8, 0, 255)
    return tile


def _grass_side_tile() -> np.ndarray:
    dirt = _dirt_tile()
    grass = _grass_top_tile()
    tile = dirt.copy()
    tile[:4, :, :] = np.clip(grass[:4, :, :] * np.array([0.9, 1.0, 0.9]), 0, 255).astype(np.uint8)
    tile[4:6, :, :] = np.array([96, 78, 46], dtype=np.uint8)
    return tile


def generate_texture_atlas() -> np.ndarray:
    atlas = np.zeros((ATLAS_HEIGHT, ATLAS_WIDTH, 3), dtype=np.uint8)
    tiles = {
        TILE_GRASS_TOP: _grass_top_tile(),
        TILE_DIRT: _dirt_tile(),
        TILE_STONE: _stone_tile(),
        TILE_GRASS_SIDE: _grass_side_tile(),
    }
    for (tx, ty), tile in tiles.items():
        y0 = ty * TILE_SIZE
        x0 = tx * TILE_SIZE
        atlas[y0 : y0 + TILE_SIZE, x0 : x0 + TILE_SIZE] = tile
    return atlas


def block_tile(block_id: int, normal: tuple[int, int, int]) -> tuple[int, int]:
    if block_id == GRASS:
        if normal == (0, 1, 0):
            return TILE_GRASS_TOP
        if normal == (0, -1, 0):
            return TILE_DIRT
        return TILE_GRASS_SIDE
    if block_id == DIRT:
        return TILE_DIRT
    if block_id == STONE:
        return TILE_STONE
    return TILE_STONE


def atlas_uvs(tile: tuple[int, int], padding: float = 0.0015) -> tuple[tuple[float, float], ...]:
    tile_width = 1.0 / ATLAS_GRID[0]
    tile_height = 1.0 / ATLAS_GRID[1]
    u0 = tile[0] * tile_width + padding
    v0 = tile[1] * tile_height + padding
    u1 = (tile[0] + 1) * tile_width - padding
    v1 = (tile[1] + 1) * tile_height - padding
    return (
        (u0, v1),
        (u0, v0),
        (u1, v0),
        (u1, v1),
    )

