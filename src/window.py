from __future__ import annotations

import pyglet
from OpenGL.GL import GL_CULL_FACE, GL_DEPTH_TEST, glDisable, glEnable
from pyglet.window import key, mouse

from src import settings


class VoxelWindow(pyglet.window.Window):
    def __init__(self, app: "GameApp", visible: bool = True):
        self.mouse_captured = visible
        rich_config = pyglet.gl.Config(
            major_version=3,
            minor_version=3,
            depth_size=24,
            double_buffer=True,
            sample_buffers=1,
            samples=4,
        )
        try:
            super().__init__(
                width=settings.WINDOW_WIDTH,
                height=settings.WINDOW_HEIGHT,
                caption=settings.WINDOW_TITLE,
                resizable=True,
                vsync=True,
                config=rich_config,
                visible=visible,
            )
        except pyglet.window.NoSuchConfigException:
            fallback_config = pyglet.gl.Config(depth_size=24, double_buffer=True)
            super().__init__(
                width=settings.WINDOW_WIDTH,
                height=settings.WINDOW_HEIGHT,
                caption=settings.WINDOW_TITLE,
                resizable=True,
                vsync=True,
                config=fallback_config,
                visible=visible,
            )
        self.app = app
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.set_minimum_size(960, 540)
        self.set_exclusive_mouse(self.mouse_captured)

        self.hud = pyglet.text.Label(
            "",
            x=16,
            y=self.height - 16,
            anchor_x="left",
            anchor_y="top",
            multiline=True,
            width=450,
            color=(22, 25, 33, 255),
        )
        self.crosshair = pyglet.text.Label(
            "+",
            x=self.width // 2,
            y=self.height // 2,
            anchor_x="center",
            anchor_y="center",
            font_size=18,
            color=(32, 32, 32, 255),
        )

    def on_draw(self) -> None:
        self.app.draw()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        self.hud.text = self.app.hud_text
        self.hud.y = self.height - 16
        self.hud.draw()
        self.crosshair.x = self.width // 2
        self.crosshair.y = self.height // 2
        self.crosshair.draw()
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)

    def on_resize(self, width: int, height: int) -> None:
        self.app.on_resize(width, height)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        if self.mouse_captured:
            self.app.on_mouse_look(dx, dy)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == key.ESCAPE:
            self.close()
        elif symbol == key.TAB:
            self.mouse_captured = not self.mouse_captured
            self.set_exclusive_mouse(self.mouse_captured)
        self.app.on_key_press(symbol, modifiers)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        if not self.mouse_captured:
            self.mouse_captured = True
            self.set_exclusive_mouse(True)
            return
        self.app.on_mouse_press(button, modifiers)
