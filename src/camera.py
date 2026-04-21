from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from src import settings
from src.math3d import clamp, look_at, normalize, perspective


@dataclass
class Camera:
    position: np.ndarray = field(default_factory=lambda: np.array([0.0, 10.0, 0.0], dtype=np.float32))
    yaw: float = -90.0
    pitch: float = -18.0
    aspect_ratio: float = settings.WINDOW_WIDTH / settings.WINDOW_HEIGHT

    def rotate(self, delta_x: float, delta_y: float) -> None:
        self.yaw += delta_x * settings.MOUSE_SENSITIVITY
        self.pitch = clamp(self.pitch + delta_y * settings.MOUSE_SENSITIVITY, -89.0, 89.0)

    def forward(self) -> np.ndarray:
        yaw_radians = np.radians(self.yaw)
        pitch_radians = np.radians(self.pitch)
        direction = np.array(
            [
                np.cos(yaw_radians) * np.cos(pitch_radians),
                np.sin(pitch_radians),
                np.sin(yaw_radians) * np.cos(pitch_radians),
            ],
            dtype=np.float32,
        )
        return normalize(direction)

    def right(self) -> np.ndarray:
        return normalize(np.cross(self.forward(), np.array([0.0, 1.0, 0.0], dtype=np.float32)))

    def view_matrix(self) -> np.ndarray:
        return look_at(self.position, self.position + self.forward(), np.array([0.0, 1.0, 0.0], dtype=np.float32))

    def projection_matrix(self) -> np.ndarray:
        return perspective(settings.FOV_DEGREES, self.aspect_ratio, settings.NEAR_PLANE, settings.FAR_PLANE)

