import unittest

import numpy as np

from src.meshing import FACE_DEFINITIONS, build_chunk_mesh
from src.raycast import raycast
from src.world import AIR, STONE, VoxelWorld


class MeshingTests(unittest.TestCase):
    def test_single_block_generates_six_faces(self) -> None:
        world = VoxelWorld(chunk_counts=(1, 1, 1), chunk_size=4)
        chunk = world.get_chunk((0, 0, 0))
        chunk.blocks.fill(AIR)
        world.set_block_world(1, 1, 1, STONE)

        vertices, indices = build_chunk_mesh(world, (0, 0, 0))
        self.assertEqual(vertices.size // 9, 24)
        self.assertEqual(indices.size, 36)

    def test_adjacent_blocks_hide_internal_faces(self) -> None:
        world = VoxelWorld(chunk_counts=(1, 1, 1), chunk_size=4)
        chunk = world.get_chunk((0, 0, 0))
        chunk.blocks.fill(AIR)
        world.set_block_world(1, 1, 1, STONE)
        world.set_block_world(2, 1, 1, STONE)

        vertices, indices = build_chunk_mesh(world, (0, 0, 0))
        self.assertEqual(vertices.size // 9, 40)
        self.assertEqual(indices.size, 60)

    def test_raycast_hits_target_block(self) -> None:
        world = VoxelWorld(chunk_counts=(1, 1, 1), chunk_size=8)
        chunk = world.get_chunk((0, 0, 0))
        chunk.blocks.fill(AIR)
        world.set_block_world(3, 3, 3, STONE)
        hit = raycast(
            world,
            np.array([0.5, 3.5, 3.5], dtype=np.float32),
            np.array([1.0, 0.0, 0.0], dtype=np.float32),
            10.0,
        )
        self.assertIsNotNone(hit)
        assert hit is not None
        self.assertEqual(hit.block, (3, 3, 3))
        self.assertEqual(hit.previous, (2, 3, 3))

    def test_face_vertex_order_matches_outward_normal(self) -> None:
        for normal, face_vertices, _brightness in FACE_DEFINITIONS:
            p0 = np.array(face_vertices[0], dtype=np.float32)
            p1 = np.array(face_vertices[1], dtype=np.float32)
            p2 = np.array(face_vertices[2], dtype=np.float32)
            computed = np.cross(p1 - p0, p2 - p0)
            expected = np.array(normal, dtype=np.float32)
            self.assertGreater(float(np.dot(computed, expected)), 0.0)


if __name__ == "__main__":
    unittest.main()
