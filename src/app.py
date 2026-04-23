from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
import pyglet
from pyglet.window import key, mouse

from src import settings
from src.camera import Camera
from src.daynight import DayNightCycle
from src.player import PlayerController
from src.raycast import RaycastHit, raycast
from src.renderer import VoxelRenderer
from src.window import VoxelWindow
from src.world import AIR, DIRT, VoxelWorld


@dataclass
class AppOptions:
    smoke_test: bool = False


class GameApp:
    def __init__(self, options: AppOptions):
        self.options = options
        self.world = VoxelWorld()
        self.camera = Camera()
        self.player = PlayerController(position=self.world.find_spawn_point())
        self.camera.position = self.player.eye_position()
        self.window = VoxelWindow(self, visible=not options.smoke_test)
        self.camera.aspect_ratio = self.window.width / max(self.window.height, 1)
        self.renderer = VoxelRenderer()
        self.renderer.resize(self.window.width, self.window.height)
        self.renderer.rebuild_world(self.world)
        self.day_night = DayNightCycle(
            cycle_seconds=settings.DAY_NIGHT_CYCLE_SECONDS,
            initial_time=settings.INITIAL_TIME_OF_DAY,
        )
        self.current_environment = self.day_night.sample()
        self.hud_text = ""
        self.fps = 0.0
        self.current_hit: RaycastHit | None = None

        pyglet.clock.schedule_interval(self.update, 1.0 / 120.0)
        if options.smoke_test:
            pyglet.clock.schedule_once(lambda _dt: self.window.close(), 0.35)

    def update(self, dt: float) -> None:
        raw_dt = max(dt, 1.0e-6)
        instant_fps = 1.0 / raw_dt
        if self.fps == 0.0:
            self.fps = instant_fps
        else:
            self.fps = self.fps * 0.9 + instant_fps * 0.1
        dt = min(dt, 1.0 / 30.0)
        input_state = {
            "forward": bool(self.window.keys[key.W]),
            "backward": bool(self.window.keys[key.S]),
            "left": bool(self.window.keys[key.A]),
            "right": bool(self.window.keys[key.D]),
            "jump": bool(self.window.keys[key.SPACE]),
        }
        self.player.update(dt, input_state, self.camera, self.world)
        self.day_night.update(dt)
        self.current_environment = self.day_night.sample()
        self.camera.position = self.player.eye_position()
        self.current_hit = raycast(self.world, self.camera.position, self.camera.forward(), settings.MAX_RAY_DISTANCE)
        self._update_hud()

    def draw(self) -> None:
        target = self.current_hit.block if self.current_hit else None
        self.renderer.draw(self.camera, self.current_environment, target_block=target)

    def on_resize(self, width: int, height: int) -> None:
        self.camera.aspect_ratio = width / max(height, 1)
        self.renderer.resize(width, height)

    def on_mouse_look(self, delta_x: float, delta_y: float) -> None:
        self.camera.rotate(delta_x, delta_y)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        del modifiers
        if symbol == key.R:
            self.player.position = self.world.find_spawn_point()
            self.player.velocity[:] = 0.0
            self.camera.position = self.player.eye_position()

    def on_mouse_press(self, button: int, modifiers: int) -> None:
        del modifiers
        if self.current_hit is None:
            return

        if button == mouse.LEFT:
            x, y, z = self.current_hit.block
            self.world.set_block_world(x, y, z, AIR)
            self._rebuild_for_block(x, y, z)
        elif button == mouse.RIGHT:
            x, y, z = self.current_hit.previous
            if self.world.get_block_world(x, y, z) != AIR:
                return

            self.world.set_block_world(x, y, z, DIRT)
            minimum, maximum = self.player.aabb_for()
            if self.world.collides_aabb(minimum, maximum):
                self.world.set_block_world(x, y, z, AIR)
                return
            self._rebuild_for_block(x, y, z)

    def _rebuild_for_block(self, x: int, y: int, z: int) -> None:
        for chunk_pos in self.world.chunks_touched_by_block(x, y, z):
            self.renderer.rebuild_chunk(self.world, chunk_pos)

    def _update_hud(self) -> None:
        block_text = "None"
        if self.current_hit is not None:
            block_text = f"{self.current_hit.block}"

        self.hud_text = (
            "Voxel OpenGL Demo\n"
            f"FPS: {self.fps:.1f}\n"
            f"Time: {self.day_night.time_of_day * 24.0:05.2f}h\n"
            f"Pos: ({self.player.position[0]:.2f}, {self.player.position[1]:.2f}, {self.player.position[2]:.2f})\n"
            f"Yaw/Pitch: ({self.camera.yaw:.1f}, {self.camera.pitch:.1f})\n"
            f"Chunks: {len(self.renderer.chunk_meshes)} / {len(self.world.chunks)}\n"
            f"Target: {block_text}\n"
            "Move: WASD | Jump: Space | Break: Left Click | Place Dirt: Right Click | Mouse Lock: TAB"
        )

    def run(self) -> None:
        pyglet.app.run()

    def shutdown(self) -> None:
        pyglet.clock.unschedule(self.update)
        self.renderer.delete()


def parse_args(argv: list[str] | None = None) -> AppOptions:
    parser = argparse.ArgumentParser(description="Voxel OpenGL tech demo")
    parser.add_argument("--smoke-test", action="store_true", help="Create the OpenGL app briefly, then exit")
    args = parser.parse_args(argv)
    return AppOptions(smoke_test=args.smoke_test)


def main(argv: list[str] | None = None) -> int:
    options = parse_args(argv)
    app: GameApp | None = None
    try:
        app = GameApp(options)
        app.run()
    finally:
        if app is not None:
            app.shutdown()
    return 0
