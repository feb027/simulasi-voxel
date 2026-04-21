from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np

from src.world import VoxelWorld


@dataclass
class RaycastHit:
    block: Tuple[int, int, int]
    previous: Tuple[int, int, int]
    distance: float


def raycast(world: VoxelWorld, origin: np.ndarray, direction: np.ndarray, max_distance: float) -> RaycastHit | None:
    direction = direction.astype(np.float32)
    block = np.floor(origin).astype(int)
    step = np.sign(direction).astype(int)

    t_delta = np.empty(3, dtype=np.float32)
    t_max = np.empty(3, dtype=np.float32)

    for axis in range(3):
        if abs(direction[axis]) < 1e-8:
            t_delta[axis] = np.inf
            t_max[axis] = np.inf
        else:
            if direction[axis] > 0:
                next_voxel = block[axis] + 1.0
            else:
                next_voxel = block[axis]
            t_max[axis] = (next_voxel - origin[axis]) / direction[axis]
            t_delta[axis] = abs(1.0 / direction[axis])

    previous = tuple(block.tolist())
    distance = 0.0
    while distance <= max_distance:
        current = tuple(block.tolist())
        if world.is_solid(*current):
            return RaycastHit(block=current, previous=previous, distance=distance)

        axis = int(np.argmin(t_max))
        previous = current
        block[axis] += step[axis]
        distance = float(t_max[axis])
        t_max[axis] += t_delta[axis]

    return None

