from __future__ import annotations

import math

import numpy as np


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def normalize(vector: np.ndarray) -> np.ndarray:
    length = float(np.linalg.norm(vector))
    if length <= 1e-8:
        return np.zeros_like(vector, dtype=np.float32)
    return (vector / length).astype(np.float32)


def perspective(fov_degrees: float, aspect: float, near: float, far: float) -> np.ndarray:
    f = 1.0 / math.tan(math.radians(fov_degrees) * 0.5)
    matrix = np.zeros((4, 4), dtype=np.float32)
    matrix[0, 0] = f / aspect
    matrix[1, 1] = f
    matrix[2, 2] = (far + near) / (near - far)
    matrix[2, 3] = (2.0 * far * near) / (near - far)
    matrix[3, 2] = -1.0
    return matrix


def look_at(eye: np.ndarray, target: np.ndarray, up: np.ndarray) -> np.ndarray:
    forward = normalize(target - eye)
    side = normalize(np.cross(forward, up))
    true_up = np.cross(side, forward)

    matrix = np.identity(4, dtype=np.float32)
    matrix[0, :3] = side
    matrix[1, :3] = true_up
    matrix[2, :3] = -forward
    matrix[0, 3] = -np.dot(side, eye)
    matrix[1, 3] = -np.dot(true_up, eye)
    matrix[2, 3] = np.dot(forward, eye)
    return matrix

