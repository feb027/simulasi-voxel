"""Unit tests for the mining system and block registry."""
from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from src.block_registry import get_hardness, get_mining_duration
from src.mining import MiningState, MiningSystem
from src.raycast import RaycastHit
from src.world import AIR, DIRT, GRASS, STONE, VoxelWorld


class BlockRegistryTests(unittest.TestCase):
    """Tests for block_registry module."""

    def test_known_block_hardness(self):
        self.assertAlmostEqual(get_hardness(GRASS), 1.0)
        self.assertAlmostEqual(get_hardness(DIRT), 0.8)
        self.assertAlmostEqual(get_hardness(STONE), 2.5)
        self.assertAlmostEqual(get_hardness(AIR), 0.0)

    def test_unknown_block_uses_default(self):
        hardness = get_hardness(999)
        self.assertAlmostEqual(hardness, 1.5)

    def test_tool_speed_halves_duration(self):
        base = get_mining_duration(STONE, tool_speed=1.0)
        fast = get_mining_duration(STONE, tool_speed=2.0)
        self.assertAlmostEqual(fast, base / 2.0)

    def test_tool_speed_zero_clamped(self):
        # tool_speed=0 should not cause division by zero
        duration = get_mining_duration(DIRT, tool_speed=0.0)
        self.assertTrue(duration > 0.0)


class MiningStateTests(unittest.TestCase):
    """Tests for MiningState dataclass properties."""

    def test_progress_zero_when_idle(self):
        state = MiningState()
        self.assertAlmostEqual(state.progress, 0.0)

    def test_progress_halfway(self):
        state = MiningState(is_mining=True, mining_time=0.5, mining_duration=1.0)
        self.assertAlmostEqual(state.progress, 0.5)

    def test_progress_clamped_to_one(self):
        state = MiningState(is_mining=True, mining_time=2.0, mining_duration=1.0)
        self.assertAlmostEqual(state.progress, 1.0)

    def test_crack_stage_zero_at_start(self):
        state = MiningState(is_mining=True, mining_time=0.0, mining_duration=1.0)
        self.assertEqual(state.crack_stage, 0)

    def test_crack_stage_nine_at_completion(self):
        state = MiningState(is_mining=True, mining_time=1.0, mining_duration=1.0)
        self.assertEqual(state.crack_stage, 9)


class MiningSystemTests(unittest.TestCase):
    """Integration tests for the MiningSystem state machine."""

    def setUp(self):
        self.world = VoxelWorld(chunk_counts=(1, 1, 1), chunk_size=16)
        self.mining = MiningSystem()
        # Place a dirt block at (2, 8, 2)
        self.world.set_block_world(2, 8, 2, DIRT)
        self.hit_dirt = RaycastHit(block=(2, 8, 2), previous=(2, 9, 2), distance=3.0)

    def test_no_mining_when_mouse_not_held(self):
        result = self.mining.update(0.1, self.hit_dirt, False, self.world)
        self.assertIsNone(result)
        self.assertFalse(self.mining.state.is_mining)

    def test_no_mining_when_no_hit(self):
        result = self.mining.update(0.1, None, True, self.world)
        self.assertIsNone(result)
        self.assertFalse(self.mining.state.is_mining)

    def test_mining_starts_on_hold(self):
        self.mining.update(0.1, self.hit_dirt, True, self.world)
        self.assertTrue(self.mining.state.is_mining)
        self.assertEqual(self.mining.state.target_block, (2, 8, 2))

    def test_mining_accumulates_time(self):
        self.mining.update(0.3, self.hit_dirt, True, self.world)
        self.assertAlmostEqual(self.mining.state.mining_time, 0.3, places=5)
        self.mining.update(0.2, self.hit_dirt, True, self.world)
        self.assertAlmostEqual(self.mining.state.mining_time, 0.5, places=5)

    def test_mining_completes_after_duration(self):
        # Dirt hardness = 0.8s — mine in steps until completion
        result = None
        for _ in range(10):
            result = self.mining.update(0.1, self.hit_dirt, True, self.world)
            if result is not None:
                break
        self.assertEqual(result, (2, 8, 2))
        # State should be reset after completion
        self.assertFalse(self.mining.state.is_mining)

    def test_release_resets_progress(self):
        self.mining.update(0.3, self.hit_dirt, True, self.world)
        self.assertTrue(self.mining.state.is_mining)
        # Release mouse
        self.mining.update(0.0, self.hit_dirt, False, self.world)
        self.assertFalse(self.mining.state.is_mining)
        self.assertAlmostEqual(self.mining.state.mining_time, 0.0)

    def test_target_change_resets_progress(self):
        self.mining.update(0.3, self.hit_dirt, True, self.world)
        self.assertAlmostEqual(self.mining.state.mining_time, 0.3, places=5)
        # Look at a different block
        self.world.set_block_world(5, 8, 5, STONE)
        hit_stone = RaycastHit(block=(5, 8, 5), previous=(5, 9, 5), distance=4.0)
        self.mining.update(0.1, hit_stone, True, self.world)
        # Progress should reset to the new dt only
        self.assertAlmostEqual(self.mining.state.mining_time, 0.1, places=5)
        self.assertEqual(self.mining.state.target_block, (5, 8, 5))

    def test_stone_takes_longer_than_dirt(self):
        self.world.set_block_world(5, 8, 5, STONE)
        hit_stone = RaycastHit(block=(5, 8, 5), previous=(5, 9, 5), distance=4.0)

        # Mine dirt until it breaks
        result = None
        for _ in range(10):
            result = self.mining.update(0.1, self.hit_dirt, True, self.world)
            if result is not None:
                break
        self.assertIsNotNone(result)

        # Mine stone for 0.8s => should NOT complete (needs 2.5s)
        for _ in range(8):
            result = self.mining.update(0.1, hit_stone, True, self.world)
        self.assertIsNone(result)

    def test_stop_mining_explicit(self):
        self.mining.update(0.3, self.hit_dirt, True, self.world)
        self.mining.stop_mining()
        self.assertFalse(self.mining.state.is_mining)
        self.assertIsNone(self.mining.state.target_block)


if __name__ == "__main__":
    unittest.main()
