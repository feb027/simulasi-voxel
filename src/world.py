from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, Tuple

import numpy as np

from src import settings

AIR = 0
GRASS = 1
DIRT = 2
STONE = 3

BLOCK_COLORS = {
    AIR: (0.0, 0.0, 0.0),
    GRASS: (0.33, 0.72, 0.28),
    DIRT: (0.50, 0.34, 0.19),
    STONE: (0.58, 0.60, 0.64),
}


@dataclass
class Chunk:
    position: Tuple[int, int, int]
    blocks: np.ndarray


class VoxelWorld:
    def __init__(self, chunk_counts: Tuple[int, int, int] = settings.WORLD_CHUNKS, chunk_size: int = settings.CHUNK_SIZE):
        self.chunk_counts = chunk_counts
        self.chunk_size = chunk_size
        self.world_size = (
            chunk_counts[0] * chunk_size,
            chunk_counts[1] * chunk_size,
            chunk_counts[2] * chunk_size,
        )
        self.chunks: Dict[Tuple[int, int, int], Chunk] = {}
        self._generate()

    def _generate(self) -> None:
        for cx in range(self.chunk_counts[0]):
            for cy in range(self.chunk_counts[1]):
                for cz in range(self.chunk_counts[2]):
                    self.chunks[(cx, cy, cz)] = Chunk(
                        position=(cx, cy, cz),
                        blocks=np.zeros((self.chunk_size, self.chunk_size, self.chunk_size), dtype=np.uint8),
                    )

        max_height = self.world_size[1] - 1
        for x in range(self.world_size[0]):
            for z in range(self.world_size[2]):
                terrain_height = self.height_at(x, z)
                for y in range(terrain_height + 1):
                    if y == terrain_height:
                        block = GRASS
                    elif y >= terrain_height - 2:
                        block = DIRT
                    else:
                        block = STONE
                    self.set_block_world(x, y, z, block)

                # Add a small plateau and trench so the terrain feels less flat.
                if 12 <= x <= 18 and 12 <= z <= 18:
                    for y in range(terrain_height + 1, min(terrain_height + 4, max_height)):
                        self.set_block_world(x, y, z, STONE if y < terrain_height + 3 else GRASS)
                if 34 <= x <= 40 and 20 <= z <= 28:
                    for y in range(max(0, terrain_height - 2), terrain_height + 1):
                        self.set_block_world(x, y, z, AIR)

    def height_at(self, x: int, z: int) -> int:
        base_height = 8.0
        wave_a = np.sin((x + settings.WORLD_SEED) * 0.18) * 2.4
        wave_b = np.cos((z - settings.WORLD_SEED) * 0.16) * 1.8
        wave_c = np.sin((x + z) * 0.09) * 1.2
        height = int(round(base_height + wave_a + wave_b + wave_c))
        return int(np.clip(height, 3, self.world_size[1] - 4))

    def iter_chunks(self) -> Iterable[Tuple[Tuple[int, int, int], Chunk]]:
        return self.chunks.items()

    def in_bounds(self, x: int, y: int, z: int) -> bool:
        return 0 <= x < self.world_size[0] and 0 <= y < self.world_size[1] and 0 <= z < self.world_size[2]

    def chunk_and_local(self, x: int, y: int, z: int) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        cx, lx = divmod(x, self.chunk_size)
        cy, ly = divmod(y, self.chunk_size)
        cz, lz = divmod(z, self.chunk_size)
        return (cx, cy, cz), (lx, ly, lz)

    def get_chunk(self, chunk_pos: Tuple[int, int, int]) -> Chunk | None:
        return self.chunks.get(chunk_pos)

    def get_block_world(self, x: int, y: int, z: int) -> int:
        if not self.in_bounds(x, y, z):
            return AIR
        chunk_pos, local_pos = self.chunk_and_local(x, y, z)
        chunk = self.chunks[chunk_pos]
        return int(chunk.blocks[local_pos])

    def set_block_world(self, x: int, y: int, z: int, block_id: int) -> None:
        if not self.in_bounds(x, y, z):
            return
        chunk_pos, local_pos = self.chunk_and_local(x, y, z)
        self.chunks[chunk_pos].blocks[local_pos] = block_id

    def is_solid(self, x: int, y: int, z: int) -> bool:
        return self.get_block_world(x, y, z) != AIR

    def solid_blocks_in_aabb(self, minimum: np.ndarray, maximum: np.ndarray) -> Iterator[Tuple[int, int, int]]:
        start = np.floor(minimum).astype(int)
        end = np.ceil(maximum).astype(int) - 1
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                for z in range(start[2], end[2] + 1):
                    if self.is_solid(x, y, z):
                        yield (x, y, z)

    def collides_aabb(self, minimum: np.ndarray, maximum: np.ndarray) -> bool:
        return any(True for _ in self.solid_blocks_in_aabb(minimum, maximum))

    def find_spawn_point(self) -> np.ndarray:
        x = self.world_size[0] // 2
        z = self.world_size[2] // 2
        y = self.height_at(x, z) + 2
        return np.array([float(x) + 0.5, float(y), float(z) + 0.5], dtype=np.float32)

    def chunks_touched_by_block(self, x: int, y: int, z: int) -> set[Tuple[int, int, int]]:
        touched = set()
        chunk_pos, local_pos = self.chunk_and_local(x, y, z)
        touched.add(chunk_pos)
        for axis, local in enumerate(local_pos):
            if local == 0:
                neighbor = list(chunk_pos)
                neighbor[axis] -= 1
                touched.add(tuple(neighbor))
            elif local == self.chunk_size - 1:
                neighbor = list(chunk_pos)
                neighbor[axis] += 1
                touched.add(tuple(neighbor))
        return {pos for pos in touched if pos in self.chunks}

