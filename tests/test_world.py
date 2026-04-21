import unittest

import numpy as np

from src.world import AIR, DIRT, STONE, VoxelWorld


class WorldTests(unittest.TestCase):
    def test_world_generates_chunks(self) -> None:
        world = VoxelWorld(chunk_counts=(2, 1, 2), chunk_size=8)
        self.assertEqual(len(world.chunks), 4)

    def test_get_and_set_block_world(self) -> None:
        world = VoxelWorld(chunk_counts=(1, 1, 1), chunk_size=8)
        world.set_block_world(3, 4, 5, DIRT)
        self.assertEqual(world.get_block_world(3, 4, 5), DIRT)
        self.assertEqual(world.get_block_world(-1, 0, 0), AIR)

    def test_collision_detects_solid_voxel(self) -> None:
        world = VoxelWorld(chunk_counts=(1, 1, 1), chunk_size=8)
        world.set_block_world(2, 2, 2, STONE)
        minimum = np.array([2.0, 2.0, 2.0], dtype=np.float32)
        maximum = np.array([2.9, 2.9, 2.9], dtype=np.float32)
        self.assertTrue(world.collides_aabb(minimum, maximum))


if __name__ == "__main__":
    unittest.main()

