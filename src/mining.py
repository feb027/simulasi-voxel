"""Hold-to-break mining system.

Non-blocking, frame-rate-independent state machine that tracks mining
progress and emits a "block broken" event when the required duration
has elapsed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from src.block_registry import get_mining_duration
from src.raycast import RaycastHit


@dataclass
class MiningState:
    """Snapshot of the current mining progress."""

    is_mining: bool = False
    target_block: Tuple[int, int, int] | None = None
    mining_time: float = 0.0
    mining_duration: float = 0.0

    @property
    def progress(self) -> float:
        """Normalised progress in [0.0, 1.0]."""
        if self.mining_duration <= 0.0:
            return 0.0
        return min(self.mining_time / self.mining_duration, 1.0)

    @property
    def crack_stage(self) -> int:
        """Discrete crack stage 0–9 (10 stages, like Minecraft)."""
        return min(int(self.progress * 10), 9)


class MiningSystem:
    """Manages hold-to-break mining logic.

    Call :meth:`update` once per frame from the game loop.  It returns
    the world-space block coordinate when a block has been fully mined,
    or ``None`` otherwise.
    """

    def __init__(self) -> None:
        self.state = MiningState()

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def start_mining(
        self,
        block_pos: Tuple[int, int, int],
        block_id: int,
        tool_speed: float = 1.0,
    ) -> None:
        """Begin mining a new block target."""
        self.state.is_mining = True
        self.state.target_block = block_pos
        self.state.mining_time = 0.0
        self.state.mining_duration = get_mining_duration(block_id, tool_speed)

    def stop_mining(self) -> None:
        """Cancel / reset all mining state."""
        self.state.is_mining = False
        self.state.target_block = None
        self.state.mining_time = 0.0
        self.state.mining_duration = 0.0

    # ------------------------------------------------------------------
    # Per-frame update
    # ------------------------------------------------------------------

    def update(
        self,
        dt: float,
        current_hit: RaycastHit | None,
        mouse_held: bool,
        world: "VoxelWorld",  # noqa: F821 — avoid circular import
    ) -> Tuple[int, int, int] | None:
        """Advance mining progress and return broken block position or *None*.

        Parameters
        ----------
        dt:
            Frame delta-time (seconds).
        current_hit:
            Result of the per-frame raycast.  ``None`` when the player
            is not looking at any solid block.
        mouse_held:
            Whether the left mouse button is currently pressed.
        world:
            The voxel world, used to query the block type of the target.

        Returns
        -------
        tuple or None
            World-space ``(x, y, z)`` of the destroyed block, or
            ``None`` if mining is still in progress (or idle).
        """

        # ---- Mouse released or no target → cancel mining ----
        if not mouse_held or current_hit is None:
            if self.state.is_mining:
                self.stop_mining()
            return None

        target = current_hit.block

        # ---- Target changed → restart mining on new block ----
        if target != self.state.target_block:
            block_id = world.get_block_world(*target)
            self.start_mining(target, block_id)

        # ---- Accumulate time ----
        self.state.mining_time += dt

        # ---- Check completion ----
        if self.state.mining_time >= self.state.mining_duration:
            broken = self.state.target_block
            self.stop_mining()
            return broken

        return None
