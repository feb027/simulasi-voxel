from __future__ import annotations

from typing import Tuple

import numpy as np

from src.textures import atlas_uvs, block_tile
from src.world import AIR, VoxelWorld

FACE_DEFINITIONS = (
    ((0, 0, -1), ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)), 0.82),
    ((0, 0, 1), ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)), 1.00),
    ((-1, 0, 0), ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)), 0.88),
    ((1, 0, 0), ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)), 0.93),
    ((0, -1, 0), ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)), 0.72),
    ((0, 1, 0), ((0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)), 1.08),
)

UV_ORDER_BY_NORMAL = {
    (0, 0, -1): (0, 1, 2, 3),
    (0, 0, 1): (0, 3, 2, 1),
    (-1, 0, 0): (0, 3, 2, 1),
    (1, 0, 0): (0, 1, 2, 3),
    (0, -1, 0): (0, 3, 2, 1),
    (0, 1, 0): (0, 1, 2, 3),
}


def oriented_face_uvs(block_id: int, normal: tuple[int, int, int]) -> tuple[tuple[float, float], ...]:
    base_uvs = atlas_uvs(block_tile(block_id, normal))
    return tuple(base_uvs[index] for index in UV_ORDER_BY_NORMAL[normal])


def build_chunk_mesh(world: VoxelWorld, chunk_position: Tuple[int, int, int]) -> tuple[np.ndarray, np.ndarray]:
    chunk = world.get_chunk(chunk_position)
    if chunk is None:
        return np.array([], dtype=np.float32), np.array([], dtype=np.uint32)

    solid_positions = np.argwhere(chunk.blocks != AIR)
    if solid_positions.size == 0:
        return np.array([], dtype=np.float32), np.array([], dtype=np.uint32)

    vertices: list[float] = []
    indices: list[int] = []
    index_offset = 0

    chunk_x, chunk_y, chunk_z = chunk_position
    origin_x = chunk_x * world.chunk_size
    origin_y = chunk_y * world.chunk_size
    origin_z = chunk_z * world.chunk_size
    chunk_blocks = chunk.blocks

    for local_x, local_y, local_z in solid_positions:
        block_id = int(chunk_blocks[local_x, local_y, local_z])
        world_x = origin_x + int(local_x)
        world_y = origin_y + int(local_y)
        world_z = origin_z + int(local_z)
        for normal, face_vertices, brightness in FACE_DEFINITIONS:
            nx = int(local_x) + normal[0]
            ny = int(local_y) + normal[1]
            nz = int(local_z) + normal[2]

            if 0 <= nx < world.chunk_size and 0 <= ny < world.chunk_size and 0 <= nz < world.chunk_size:
                if int(chunk_blocks[nx, ny, nz]) != AIR:
                    continue
            else:
                if world.get_block_world(world_x + normal[0], world_y + normal[1], world_z + normal[2]) != AIR:
                    continue

            normal_array = np.array(normal, dtype=np.float32)
            face_uvs = oriented_face_uvs(block_id, normal)
            for corner, uv in zip(face_vertices, face_uvs):
                vertices.extend(
                    (
                        float(world_x + corner[0]),
                        float(world_y + corner[1]),
                        float(world_z + corner[2]),
                        float(uv[0]),
                        float(uv[1]),
                        float(normal_array[0]),
                        float(normal_array[1]),
                        float(normal_array[2]),
                        float(brightness),
                    )
                )

            indices.extend(
                (
                    index_offset,
                    index_offset + 1,
                    index_offset + 2,
                    index_offset,
                    index_offset + 2,
                    index_offset + 3,
                )
            )
            index_offset += 4

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)
