from __future__ import annotations

import ctypes
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
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
    GL_STATIC_DRAW,
    GL_TRIANGLES,
    GL_TRUE,
    GL_UNSIGNED_INT,
    GL_VERTEX_SHADER,
    glAttachShader,
    glBindBuffer,
    glBindVertexArray,
    glBufferData,
    glClear,
    glClearColor,
    glDeleteBuffers,
    glDeleteProgram,
    glDeleteShader,
    glDeleteVertexArrays,
    glDepthFunc,
    glDisable,
    glDrawElements,
    glEnable,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenVertexArrays,
    glGetProgramInfoLog,
    glGetProgramiv,
    glGetShaderInfoLog,
    glGetShaderiv,
    glGetUniformLocation,
    glLinkProgram,
    glPolygonMode,
    glShaderSource,
    glUniform3f,
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
from src.meshing import build_chunk_mesh
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

    def delete(self) -> None:
        glDeleteProgram(self.program)


class VoxelRenderer:
    def __init__(self) -> None:
        shader_dir = Path(__file__).resolve().parent.parent / "assets" / "shaders"
        self.voxel_shader = ShaderProgram(shader_dir / "voxel.vert", shader_dir / "voxel.frag")
        self.outline_shader = ShaderProgram(shader_dir / "outline.vert", shader_dir / "outline.frag")
        self.chunk_meshes: dict[tuple[int, int, int], ChunkMesh] = {}
        self.outline_mesh = self._create_outline_mesh()
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

    def draw(self, camera: Camera, target_block: tuple[int, int, int] | None = None) -> None:
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        projection = camera.projection_matrix()
        view = camera.view_matrix()

        self.voxel_shader.use()
        self.voxel_shader.set_mat4("u_projection", projection)
        self.voxel_shader.set_mat4("u_view", view)
        self.voxel_shader.set_vec3("u_camera_pos", camera.position)
        self.voxel_shader.set_vec3("u_fog_color", settings.FOG_COLOR)
        self.voxel_shader.set_vec3("u_sun_direction", (0.6, 1.0, 0.35))

        for mesh in self.chunk_meshes.values():
            glBindVertexArray(mesh.vao)
            glDrawElements(GL_TRIANGLES, mesh.index_count, GL_UNSIGNED_INT, None)

        glBindVertexArray(0)

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
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(24))

        glBindVertexArray(0)
        return ChunkMesh(vao=vao, vbo=vbo, ebo=ebo, index_count=int(indices.size))

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
        self.voxel_shader.delete()
        self.outline_shader.delete()
