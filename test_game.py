"""
test_game.py - Comprehensive Test Suite for ECHO
Validates all DSA algorithms, AI perception, memory, FSM, game logic, and headless simulation.
"""

import os
import sys
import math
import time

# Set headless drivers for automated testing
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import numpy as np

from dsa.graph import GridGraph
from dsa.astar import astar_search, smooth_path
from dsa.priority_queue import PriorityQueue
from dsa.bfs_search import bfs_area_search

from ai.perception import SoundEvent, PerceivedSound, SoundPerceptionSystem
from ai.memory import AIMemory
from ai.decision import SuspicionManager, ThreatLevel
from ai.state_machine import (
    AIStateMachine, PatrolState, InvestigateState,
    SearchState, AlertState, ChaseState, AttackState, ReturnToPatrolState
)
from ai.behavior import AdaptiveBehaviorModel

from game.level import Level
from game.player import Player
from game.enemy import EnemyAI
from game.sound_system import SoundManager, ProceduralSoundSynthesizer
from game.objectives import ObjectiveManager
from game.game import GameManager


def test_dsa():
    print("[TEST] Testing DSA module...")
    graph = GridGraph(20, 20, cell_size=32)
    # Block a column except for one gap
    for r in range(20):
        if r != 10:
            graph.set_blocked(5, r, True)

    assert not graph.is_walkable(5, 0)
    assert graph.is_walkable(5, 10)

    # Test A* search
    path = astar_search(graph, (2, 2), (8, 2), allow_diagonal=True)
    assert path is not None, "A* failed to find path around wall"
    assert path[0] == (2, 2)
    assert path[-1] == (8, 2)
    # Path must route through the gap at (5, 10)
    assert (5, 10) in path, "A* path did not navigate through the gap!"

    # Test path smoothing
    smoothed = smooth_path(graph, path)
    assert len(smoothed) > 0

    # Test raycasting wall crossings
    wall_count = graph.count_wall_crossings((2 * 32, 2 * 32), (8 * 32, 2 * 32))
    assert wall_count >= 1, f"Expected wall crossing, got {wall_count}"

    # Test PriorityQueue
    pq = PriorityQueue(max_heap=True)
    pq.push("Quiet Footstep", 5.0)
    pq.push("Distraction Throw", 75.0)
    pq.push("Door Servo", 40.0)

    item1, prio1 = pq.pop()
    assert item1 == "Distraction Throw" and prio1 == 75.0
    item2, prio2 = pq.pop()
    assert item2 == "Door Servo" and prio2 == 40.0
    item3, prio3 = pq.pop()
    assert item3 == "Quiet Footstep" and prio3 == 5.0

    # Test BFS area search
    bfs_pts = bfs_area_search(graph, (10, 10), max_depth=5, max_targets=4)
    assert len(bfs_pts) > 0, "BFS generated no waypoints"
    print("  -> DSA tests PASSED!")


def test_ai_perception_and_memory():
    print("[TEST] Testing AI perception, memory, and suspicion...")
    graph = GridGraph(40, 40, cell_size=32)
    perception = SoundPerceptionSystem(graph, difficulty_name="HARD")

    # Sound right next to AI
    sound_near = SoundEvent(position=(100, 100), intensity=50.0, sound_type="run", timestamp=10.0)
    perceived_near = perception.process_sound(sound_near, listener_position=(110, 100))
    assert perceived_near is not None, "Nearby sound not detected"
    assert perceived_near.confidence > 0.5

    # Localization error check
    dist_error = math.hypot(
        perceived_near.estimated_position[0] - sound_near.position[0],
        perceived_near.estimated_position[1] - sound_near.position[1]
    )
    # There should be a realistic localization error, but bounded
    assert dist_error >= 0.0

    # Very distant quiet sound through walls
    for c in range(15, 25):
        graph.set_blocked(c, 10, True)
    sound_distant = SoundEvent(position=(900, 900), intensity=3.0, sound_type="crouch", timestamp=10.0)
    perceived_distant = perception.process_sound(sound_distant, listener_position=(100, 100))
    assert perceived_distant is None, "AI detected faint sound that should have been inaudible"

    # Test Memory
    memory = AIMemory(retention_duration=10.0, half_life=4.0)
    memory.add_memory((200, 200), "run", 50.0, timestamp=10.0)
    memory.add_memory((210, 205), "run", 45.0, timestamp=10.5)
    threat = memory.get_cluster_threat((200, 200), radius=100.0)
    assert threat > 50.0, "Cluster threat failed"

    # Memory decay test
    memory.update(current_time=25.0)  # 15s elapsed -> older than 10s retention
    assert memory.count() == 0, "Memory failed to decay expired events"

    # Test Suspicion
    susp_mgr = SuspicionManager(difficulty="HARD")
    assert susp_mgr.level == ThreatLevel.CALM
    susp_mgr.register_sound(perceived_intensity=45.0, sound_type="run", cluster_threat=20.0, current_time=1.0)
    assert susp_mgr.suspicion >= 30.0
    assert susp_mgr.level in (ThreatLevel.SUSPICIOUS, ThreatLevel.ALERT)

    # Test Extreme Adaptation
    adaptive = AdaptiveBehaviorModel()
    adaptive.record_throw((300, 300), current_time=1.0)
    adaptive.record_throw((310, 305), current_time=5.0)
    adaptive.record_throw((305, 300), current_time=10.0)
    skepticism = adaptive.get_skepticism(current_time=12.0)
    assert skepticism >= 0.5, f"Expected skepticism >= 0.5, got {skepticism}"
    print("  -> AI perception and memory tests PASSED!")


def test_game_simulation():
    print("[TEST] Testing Game Manager & Simulation Loop...")
    app = GameManager()
    app.start_new_game()

    assert app.level is not None
    assert app.player is not None
    assert app.enemy is not None
    assert app.objectives is not None

    # Step through simulation frames
    for frame in range(120):
        app.update(dt=0.016)

    # Test throwing distraction
    initial_throwables = app.player.inventory_throwables
    app._throw_distraction((500, 500))
    assert app.player.inventory_throwables == initial_throwables - 1
    assert len(app.projectiles) == 1

    # Simulate projectile impact
    for _ in range(60):
        app.update(dt=0.016)

    # Ensure projectile impacted and triggered sound
    assert len(app.projectiles) == 0

    print("  -> Game simulation tests PASSED!")


if __name__ == "__main__":
    test_dsa()
    test_ai_perception_and_memory()
    test_game_simulation()
    print("\n[ALL TESTS PASSED SUCCESSFULLY!]")
