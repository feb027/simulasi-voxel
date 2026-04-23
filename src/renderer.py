from __future__ import annotations

import ctypes
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_BLEND,
    GL_CLAMP_TO_EDGE,
    GL_COLOR_BUFFER_BIT,
    GL_COMPILE_STATUS,
    GL_CULL_FACE,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_DYNAMIC_DRAW,
    GL_ELEMENT_ARRAY_BUFFER,
    GL_FALSE,
    GL_FILL,
    GL_FLOAT,
    GL_FRAGMENT_SHADER,
    GL_FRONT_AND_BACK,
    GL_LESS,
    GL_LINES,
    GL_LINE_SMOOTH,
    GL_LINK_STATUS,
    GL_NEAREST,
    GL_ONE,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_RGB,
    GL_SRC_ALPHA,
    GL_STATIC_DRAW,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_TEXTURE0,
    GL_TRIANGLES,
    GL_TRUE,
    GL_UNSIGNED_INT,
    GL_UNSIGNED_BYTE,
    GL_VERTEX_SHADER,
    glActiveTexture,
    glAttachShader,
    glBindBuffer,
    glBindTexture,
    glBindVertexArray,
    glBufferData,
    glClear,
    glClearColor,
    glBlendFunc,
    glDeleteBuffers,
    glDeleteProgram,
    glDeleteShader,
    glDeleteTextures,
    glDeleteVertexArrays,
    glDepthFunc,
    glDisable,
    glDrawElements,
    glEnable,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenTextures,
    glGenVertexArrays,
    glGetProgramInfoLog,
    glGetProgramiv,
    glGetShaderInfoLog,
    glGetShaderiv,
    glGetUniformLocation,
    glLinkProgram,
    glPolygonMode,
    glShaderSource,
    glTexImage2D,
    glTexParameteri,
    glUniform3f,
    glUniform1f,
    glUniform1i,
    glUniformMatrix4fv,
    glUseProgram,
    glVertexAttribPointer,
    glViewport,
    glCreateProgram,
    glCreateShader,
    glCompileShader,
)

from src import settings
from src.camera import Camera
from src.daynight import DayNightState
from src.meshing import build_chunk_mesh
from src.textures import generate_texture_atlas
from src.world import VoxelWorld


@dataclass
class ChunkMesh:
    vao: int
    vbo: int
    ebo: int
    index_count: int


class ShaderProgram:
    def __init__(self, vertex_path: Path, fragment_path: Path):
        self.program = glCreateProgram()
        vertex_shader = self._compile_shader(vertex_path.read_text(encoding="utf-8"), GL_VERTEX_SHADER)
        fragment_shader = self._compile_shader(fragment_path.read_text(encoding="utf-8"), GL_FRAGMENT_SHADER)
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)
        if glGetProgramiv(self.program, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(self.program).decode("utf-8"))
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    def _compile_shader(self, source: str, shader_type: int) -> int:
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(shader).decode("utf-8"))
        return shader

    def use(self) -> None:
        glUseProgram(self.program)

    def set_mat4(self, name: str, matrix: np.ndarray) -> None:
        location = glGetUniformLocation(self.program, name)
        glUniformMatrix4fv(location, 1, GL_TRUE, matrix)

    def set_vec3(self, name: str, value: tuple[float, float, float] | np.ndarray) -> None:
        location = glGetUniformLocation(self.program, name)
        glUniform3f(location, float(value[0]), float(value[1]), float(value[2]))

    def set_int(self, name: str, value: int) -> None:
        location = glGetUniformLocation(self.program, name)
        glUniform1i(location, value)

    def set_float(self, name: str, value: float) -> None:
        location = glGetUniformLocation(self.program, name)
        glUniform1f(location, value)

    def delete(self) -> None:
        glDeleteProgram(self.program)


class VoxelRenderer:
    def __init__(self) -> None:
        shader_dir = Path(__file__).resolve().parent.parent / "assets" / "shaders"
        self.voxel_shader = ShaderProgram(shader_dir / "voxel.vert", shader_dir / "voxel.frag")
        self.outline_shader = ShaderProgram(shader_dir / "outline.vert", shader_dir / "outline.frag")
        self.celestial_shader = ShaderProgram(shader_dir / "celestial.vert", shader_dir / "celestial.frag")
        self.chunk_meshes: dict[tuple[int, int, int], ChunkMesh] = {}
        self.atlas_texture = self._create_texture_atlas()
        self.outline_mesh = self._create_outline_mesh()
        self.celestial_mesh = self._create_celestial_mesh()
        self.configure_state()

    def configure_state(self) -> None:
        glClearColor(*settings.CLEAR_COLOR)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_CULL_FACE)
        glEnable(GL_LINE_SMOOTH)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def resize(self, width: int, height: int) -> None:
        glViewport(0, 0, width, height)

    def rebuild_world(self, world: VoxelWorld) -> None:
        for chunk_pos, _chunk in world.iter_chunks():
            self.rebuild_chunk(world, chunk_pos)

    def rebuild_chunk(self, world: VoxelWorld, chunk_pos: tuple[int, int, int]) -> None:
        old_mesh = self.chunk_meshes.pop(chunk_pos, None)
        if old_mesh is not None:
            self._delete_mesh(old_mesh)

        vertices, indices = build_chunk_mesh(world, chunk_pos)
        if indices.size == 0:
            return
        self.chunk_meshes[chunk_pos] = self._upload_mesh(vertices, indices, dynamic=False)

    def draw(
        self,
        camera: Camera,
        env: DayNightState,
        target_block: tuple[int, int, int] | None = None,
    ) -> None:
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClearColor(*env.clear_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        projection = camera.projection_matrix()
        view = camera.view_matrix()

        self._draw_celestial(camera, projection, view, env)

        self.voxel_shader.use()
        self.voxel_shader.set_mat4("u_projection", projection)
        self.voxel_shader.set_mat4("u_view", view)
        self.voxel_shader.set_vec3("u_camera_pos", camera.position)
        self.voxel_shader.set_vec3("u_fog_color", env.fog_color)
        self.voxel_shader.set_vec3("u_sun_direction", env.light_direction)
        self.voxel_shader.set_vec3("u_light_color", env.light_color)
        self.voxel_shader.set_float("u_ambient_strength", env.ambient_strength)
        self.voxel_shader.set_float("u_diffuse_strength", env.diffuse_strength)
        self.voxel_shader.set_int("u_texture_atlas", 0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.atlas_texture)

        for mesh in self.chunk_meshes.values():
            glBindVertexArray(mesh.vao)
            glDrawElements(GL_TRIANGLES, mesh.index_count, GL_UNSIGNED_INT, None)

        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)

        if target_block is not None:
            self._draw_outline(camera, target_block)

    def _upload_mesh(self, vertices: np.ndarray, indices: np.ndarray, dynamic: bool) -> ChunkMesh:
        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        ebo = glGenBuffers(1)

        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW if dynamic else GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_DYNAMIC_DRAW if dynamic else GL_STATIC_DRAW)

        stride = 9 * ctypes.sizeof(ctypes.c_float)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(20))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(32))

        glBindVertexArray(0)
        return ChunkMesh(vao=vao, vbo=vbo, ebo=ebo, index_count=int(indices.size))

    def _create_texture_atlas(self) -> int:
        atlas = generate_texture_atlas()
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            atlas.shape[1],
            atlas.shape[0],
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            atlas,
        )
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture

    def _create_outline_mesh(self) -> ChunkMesh:
        vertices = np.zeros(8 * 3, dtype=np.float32)
        indices = np.array(
            [
                0, 1, 1, 2, 2, 3, 3, 0,
                4, 5, 5, 6, 6, 7, 7, 4,
                0, 4, 1, 5, 2, 6, 3, 7,
            ],
            dtype=np.uint32,
        )

        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        ebo = glGenBuffers(1)
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
        glBindVertexArray(0)
        return ChunkMesh(vao=vao, vbo=vbo, ebo=ebo, index_count=int(indices.size))

    def _create_celestial_mesh(self) -> ChunkMesh:
        vertices = np.array(
            [
                0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0, 1.0,
                0.0, 0.0, 0.0, 0.0, 1.0,
            ],
            dtype=np.float32,
        )
        indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)

        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        ebo = glGenBuffers(1)
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
        glBindVertexArray(0)
        return ChunkMesh(vao=vao, vbo=vbo, ebo=ebo, index_count=int(indices.size))

    def _draw_celestial(self, camera: Camera, projection: np.ndarray, view: np.ndarray, env: DayNightState) -> None:
        self.celestial_shader.use()
        self.celestial_shader.set_mat4("u_projection", projection)
        self.celestial_shader.set_mat4("u_view", view)

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glBindVertexArray(self.celestial_mesh.vao)

        if env.sun_visibility > 0.0:
            self.celestial_shader.set_vec3("u_color", env.sun_color)
            self.celestial_shader.set_float("u_visibility", env.sun_visibility)
            self.celestial_shader.set_float("u_core_strength", 1.95)
            self.celestial_shader.set_float("u_halo_strength", 1.25)
            self.celestial_shader.set_float("u_halo_radius", 1.34)
            self.celestial_shader.set_float("u_edge_softness", 0.95)
            self._draw_celestial_body(
                camera,
                camera.position + env.sun_direction * settings.CELESTIAL_DISTANCE,
                settings.SUN_RADIUS_WORLD,
            )

        if env.moon_visibility > 0.0:
            self.celestial_shader.set_vec3("u_color", env.moon_color)
            self.celestial_shader.set_float("u_visibility", env.moon_visibility)
            self.celestial_shader.set_float("u_core_strength", 0.86)
            self.celestial_shader.set_float("u_halo_strength", 0.38)
            self.celestial_shader.set_float("u_halo_radius", 1.26)
            self.celestial_shader.set_float("u_edge_softness", 0.72)
            self._draw_celestial_body(
                camera,
                camera.position + env.moon_direction * settings.CELESTIAL_DISTANCE,
                settings.MOON_RADIUS_WORLD,
            )

        glBindVertexArray(0)
        glDisable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)

    def _draw_celestial_body(self, camera: Camera, center: np.ndarray, radius: float) -> None:
        right = camera.right()
        up = np.cross(right, camera.forward())
        up_norm = np.linalg.norm(up)
        if up_norm <= 1.0e-8:
            up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        else:
            up = (up / up_norm).astype(np.float32)

        p0 = center - right * radius - up * radius
        p1 = center + right * radius - up * radius
        p2 = center + right * radius + up * radius
        p3 = center - right * radius + up * radius

        vertices = np.array(
            [
                p0[0], p0[1], p0[2], 0.0, 0.0,
                p1[0], p1[1], p1[2], 1.0, 0.0,
                p2[0], p2[1], p2[2], 1.0, 1.0,
                p3[0], p3[1], p3[2], 0.0, 1.0,
            ],
            dtype=np.float32,
        )
        glBindBuffer(GL_ARRAY_BUFFER, self.celestial_mesh.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
        glDrawElements(GL_TRIANGLES, self.celestial_mesh.index_count, GL_UNSIGNED_INT, None)

    def _draw_outline(self, camera: Camera, block: tuple[int, int, int]) -> None:
        x, y, z = block
        pad = 0.002
        vertices = np.array(
            [
                x - pad, y - pad, z - pad,
                x + 1 + pad, y - pad, z - pad,
                x + 1 + pad, y + 1 + pad, z - pad,
                x - pad, y + 1 + pad, z - pad,
                x - pad, y - pad, z + 1 + pad,
                x + 1 + pad, y - pad, z + 1 + pad,
                x + 1 + pad, y + 1 + pad, z + 1 + pad,
                x - pad, y + 1 + pad, z + 1 + pad,
            ],
            dtype=np.float32,
        )
        glBindBuffer(GL_ARRAY_BUFFER, self.outline_mesh.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)

        self.outline_shader.use()
        self.outline_shader.set_mat4("u_projection", camera.projection_matrix())
        self.outline_shader.set_mat4("u_view", camera.view_matrix())
        self.outline_shader.set_vec3("u_color", (0.05, 0.05, 0.05))

        glDisable(GL_CULL_FACE)
        glBindVertexArray(self.outline_mesh.vao)
        glDrawElements(GL_LINES, self.outline_mesh.index_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        glEnable(GL_CULL_FACE)

    def _delete_mesh(self, mesh: ChunkMesh) -> None:
        glDeleteVertexArrays(1, [mesh.vao])
        glDeleteBuffers(1, [mesh.vbo])
        glDeleteBuffers(1, [mesh.ebo])

    def delete(self) -> None:
        for mesh in self.chunk_meshes.values():
            self._delete_mesh(mesh)
        self.chunk_meshes.clear()
        self._delete_mesh(self.outline_mesh)
        self._delete_mesh(self.celestial_mesh)
        glDeleteTextures(1, [self.atlas_texture])
        self.voxel_shader.delete()
        self.outline_shader.delete()
        self.celestial_shader.delete()
