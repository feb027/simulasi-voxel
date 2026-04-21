from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from src import settings
from src.camera import Camera
from src.math3d import normalize
from src.world import VoxelWorld


@dataclass
class PlayerController:
    position: np.ndarray
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float32))
    on_ground: bool = False

    def aabb_for(self, position: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
        pos = self.position if position is None else position
        minimum = np.array(
            [pos[0] - settings.PLAYER_RADIUS, pos[1], pos[2] - settings.PLAYER_RADIUS],
            dtype=np.float32,
        )
        maximum = np.array(
            [pos[0] + settings.PLAYER_RADIUS, pos[1] + settings.PLAYER_HEIGHT, pos[2] + settings.PLAYER_RADIUS],
            dtype=np.float32,
        )
        return minimum, maximum

    def eye_position(self) -> np.ndarray:
        return self.position + np.array([0.0, settings.EYE_HEIGHT, 0.0], dtype=np.float32)

    def update(self, dt: float, input_state: dict[str, bool], camera: Camera, world: VoxelWorld) -> None:
        move_direction = np.zeros(3, dtype=np.float32)
        forward = camera.forward()
        flat_forward = normalize(np.array([forward[0], 0.0, forward[2]], dtype=np.float32))
        right = normalize(np.cross(flat_forward, np.array([0.0, 1.0, 0.0], dtype=np.float32)))

        if input_state.get("forward"):
            move_direction += flat_forward
        if input_state.get("backward"):
            move_direction -= flat_forward
        if input_state.get("right"):
            move_direction += right
        if input_state.get("left"):
            move_direction -= right

        if np.linalg.norm(move_direction) > 0.0:
            move_direction = normalize(move_direction)

        horizontal_velocity = move_direction * settings.MOVE_SPEED
        self.velocity[0] = horizontal_velocity[0]
        self.velocity[2] = horizontal_velocity[2]

        if input_state.get("jump") and self.on_ground:
            self.velocity[1] = settings.JUMP_SPEED
            self.on_ground = False

        self.velocity[1] -= settings.GRAVITY * dt

        self._move_axis(0, self.velocity[0] * dt, world)
        self._move_axis(2, self.velocity[2] * dt, world)
        self.on_ground = False
        self._move_axis(1, self.velocity[1] * dt, world)

    def _move_axis(self, axis: int, delta: float, world: VoxelWorld) -> None:
        if abs(delta) <= 1e-8:
            return

        step_direction = np.sign(delta)
        remaining = abs(delta)
        step_size = 0.05

        while remaining > 1e-8:
            amount = min(step_size, remaining) * step_direction
            candidate = self.position.copy()
            candidate[axis] += amount
            minimum, maximum = self.aabb_for(candidate)
            if world.collides_aabb(minimum, maximum):
                self.velocity[axis] = 0.0
                if axis == 1 and step_direction < 0:
                    self.on_ground = True
                return
            self.position = candidate
            remaining -= abs(amount)

