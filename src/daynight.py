from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src import settings


@dataclass
class DayNightState:
    light_direction: np.ndarray
    light_color: np.ndarray
    fog_color: np.ndarray
    clear_color: tuple[float, float, float, float]
    ambient_strength: float
    diffuse_strength: float
    sun_direction: np.ndarray
    moon_direction: np.ndarray
    sun_visibility: float
    moon_visibility: float
    sun_color: np.ndarray
    moon_color: np.ndarray


class DayNightCycle:
    def __init__(self, cycle_seconds: float, initial_time: float = 0.0):
        self.cycle_seconds = max(cycle_seconds, 1.0)
        self.time_of_day = initial_time % 1.0

    def update(self, dt: float) -> None:
        self.time_of_day = (self.time_of_day + dt / self.cycle_seconds) % 1.0

    def sample(self) -> DayNightState:
        # Offset keeps the default start close to a daytime scene.
        angle = self.time_of_day * np.pi * 2.0 - np.pi * 0.5
        sun_direction = np.array([np.cos(angle), np.sin(angle), 0.26], dtype=np.float32)
        sun_direction /= np.linalg.norm(sun_direction)
        moon_direction = -sun_direction

        daylight = float(np.clip((sun_direction[1] + 0.12) / 0.8, 0.0, 1.0))

        fog_day = np.array((0.60, 0.78, 0.98), dtype=np.float32)
        fog_night = np.array((0.04, 0.07, 0.14), dtype=np.float32)
        clear_day = np.array((0.55, 0.75, 0.98, 1.0), dtype=np.float32)
        clear_night = np.array((0.02, 0.03, 0.08, 1.0), dtype=np.float32)

        fog_color = fog_night * (1.0 - daylight) + fog_day * daylight
        clear_rgba = clear_night * (1.0 - daylight) + clear_day * daylight

        twilight = float(np.clip(1.0 - abs(sun_direction[1]) * 4.0, 0.0, 1.0))
        sunset_tint = np.array((0.11, 0.05, 0.0, 0.0), dtype=np.float32)
        clear_rgba += sunset_tint * twilight

        sun_visibility = float(np.clip((sun_direction[1] + 0.05) / 0.22, 0.0, 1.0))
        moon_visibility = float(np.clip((moon_direction[1] + 0.05) / 0.22, 0.0, 1.0))

        sun_color = np.array((1.0, 0.93, 0.76), dtype=np.float32)
        moon_color = np.array((0.78, 0.84, 0.98), dtype=np.float32)

        light_direction = sun_direction if daylight > 0.17 else moon_direction
        light_color = moon_color * (1.0 - daylight) + sun_color * daylight

        ambient_strength = 0.16 + 0.20 * daylight
        diffuse_strength = 0.34 + 0.50 * daylight

        return DayNightState(
            light_direction=light_direction,
            light_color=light_color,
            fog_color=fog_color,
            clear_color=(
                float(np.clip(clear_rgba[0], 0.0, 1.0)),
                float(np.clip(clear_rgba[1], 0.0, 1.0)),
                float(np.clip(clear_rgba[2], 0.0, 1.0)),
                float(np.clip(clear_rgba[3], 0.0, 1.0)),
            ),
            ambient_strength=float(ambient_strength),
            diffuse_strength=float(diffuse_strength),
            sun_direction=sun_direction,
            moon_direction=moon_direction,
            sun_visibility=sun_visibility,
            moon_visibility=moon_visibility,
            sun_color=sun_color,
            moon_color=moon_color,
        )
