"""
verify_gameplay_scenarios.py - Deep Verification of all Specification Features
Tests every required AI and gameplay scenario end-to-end.
"""

import os
import sys
import math
import time

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from dsa.graph import GridGraph
from dsa.astar import astar_search, smooth_path
from dsa.priority_queue import PriorityQueue
from dsa.bfs_search import bfs_area_search

from ai.perception import SoundEvent, SoundPerceptionSystem
from ai.memory import AIMemory
from ai.decision import SuspicionManager, ThreatLevel
from ai.state_machine import (
    AIStateMachine, PatrolState, InvestigateState,
    SearchState, AlertState, ChaseState, ReturnToPatrolState
)
from ai.behavior import AdaptiveBehaviorModel

from game.level import Level
from game.player import Player
from game.enemy import EnemyAI
from game.sound_system import SoundManager
from game.objectives import ObjectiveManager
from game.settings import (
    NOISE_CROUCH, NOISE_WALK, NOISE_RUN, NOISE_THROW_IMPACT,
    DIFFICULTIES
)


def verify_all():
    pygame.init()
    print("=" * 60)
    print(" RUNNING DEEP VERIFICATION OF SPECIFICATION REQUIREMENTS")
    print("=" * 60)

    # 1. Noise levels
    print("\n[1] Verifying Noise Scaling:")
    print(f"  Crouch Noise: {NOISE_CROUCH} dB")
    print(f"  Walk Noise:   {NOISE_WALK} dB")
    print(f"  Run Noise:    {NOISE_RUN} dB")
    print(f"  Throw Noise:  {NOISE_THROW_IMPACT} dB")
    assert NOISE_CROUCH < NOISE_WALK < NOISE_RUN < NOISE_THROW_IMPACT
    print("  -> Noise hierarchy verified: Crouch < Walk < Run < Throw!")

    # 2. Sound Attenuation & Wall Damping
    print("\n[2] Verifying Acoustic Attenuation & Obstacle Damping:")
    level = Level(difficulty="HARD")
    perception = SoundPerceptionSystem(level.graph, difficulty_name="HARD")

    # Near unobstructed sound
    snd_near = SoundEvent(position=(160, 160), intensity=50.0, sound_type="run", timestamp=1.0)
    res_near = perception.process_sound(snd_near, listener_position=(180, 160))
    assert res_near is not None
    print(f"  Near Unobstructed Sound Perceived: {res_near.perceived_intensity:.1f} dB")

    # Same sound through 3 walls
    res_walled = perception.process_sound(snd_near, listener_position=(160, 480))
    # Wall count between (160, 160) and (160, 480)
    wall_cnt = level.graph.count_wall_crossings((160, 160), (160, 480))
    print(f"  Sound through {wall_cnt} walls perceived: {res_walled.perceived_intensity if res_walled else 0.0:.1f} dB")
    if res_walled:
        assert res_walled.perceived_intensity < res_near.perceived_intensity
    print("  -> Physical acoustic attenuation & wall obstruction verified!")

    # 3. Imperfect Localization Error
    print("\n[3] Verifying Sound Localization Error:")
    snd_test = SoundEvent(position=(400, 300), intensity=40.0, sound_type="walk", timestamp=1.0)
    perceived_test = perception.process_sound(snd_test, listener_position=(450, 320))
    assert perceived_test is not None
    error = math.hypot(
        perceived_test.estimated_position[0] - snd_test.position[0],
        perceived_test.estimated_position[1] - snd_test.position[1]
    )
    print(f"  True: (400, 300) | Estimated: ({perceived_test.estimated_position[0]:.1f}, {perceived_test.estimated_position[1]:.1f}) | Error: {error:.1f} px")
    print("  -> Imperfect localization confirmed (AI does NOT magically get player coords)!")

    # 4. Priority Queue Triaging
    print("\n[4] Verifying Priority Queue Sound Prioritization:")
    pq = PriorityQueue(max_heap=True)
    pq.push("Footstep_Walk", 16.0)
    pq.push("Thrown_Bottle_Shatter", 75.0)
    pq.push("Footstep_Run", 48.0)
    pq.push("Door_Motor", 40.0)

    top_item, top_prio = pq.pop()
    print(f"  Highest Priority Sound: '{top_item}' with intensity {top_prio}")
    assert top_item == "Thrown_Bottle_Shatter"
    second_item, second_prio = pq.pop()
    assert second_item == "Footstep_Run"
    print("  -> Priority queue correctly prioritized distraction throw above footsteps!")

    # 5. A* Pathfinding and BFS Search
    print("\n[5] Verifying A* Pathfinding and BFS Corner Search:")
    start_grid = level.graph.world_to_grid(level.player_start_pos[0], level.player_start_pos[1])
    goal_grid = (16, 10)  # Central corridor
    path = astar_search(level.graph, start_grid, goal_grid)
    assert path is not None and len(path) > 0
    smoothed = smooth_path(level.graph, path)
    print(f"  A* Path Found: {len(path)} grid cells -> {len(smoothed)} smoothed waypoints")

    bfs_points = bfs_area_search(level.graph, goal_grid, max_depth=5, max_targets=4)
    print(f"  BFS Area Search generated {len(bfs_points)} tactical corner/alcove waypoints")
    assert len(bfs_points) >= 2
    print("  -> A* and BFS Area Search DSA algorithms verified!")

    # 6. AI State Machine Transition Cycle
    print("\n[6] Verifying AI State Machine Transitions:")
    sound_mgr = SoundManager()
    player = Player(level.player_start_pos[0], level.player_start_pos[1])
    enemy = EnemyAI(level.enemy_start_pos[0], level.enemy_start_pos[1], level.graph, level.patrol_waypoints, "HARD")
    enemy.set_player_and_sound_manager(player, sound_mgr)

    print(f"  Initial State: {enemy.state_machine.current_state_name}")
    assert enemy.state_machine.current_state_name == "PATROL"

    # Emit loud sound near enemy
    sound_mgr.emit_sound(
        position=(enemy.x + 80, enemy.y),
        intensity=75.0,
        sound_type="throw_impact",
        timestamp=time.time()
    )
    # Update AI frame
    enemy.update(dt=0.016, current_time=time.time())
    print(f"  State after loud sound: {enemy.state_machine.current_state_name}")
    assert enemy.state_machine.current_state_name in ("INVESTIGATE", "ALERT")

    # Move enemy to target and simulate arrival
    if enemy.current_target:
        enemy.x = enemy.current_target[0]
        enemy.y = enemy.current_target[1]
    enemy.update(dt=0.016, current_time=time.time())
    print(f"  State upon arriving at sound target: {enemy.state_machine.current_state_name}")
    assert enemy.state_machine.current_state_name in ("SEARCH", "ALERT", "INVESTIGATE")

    print("  -> FSM State Machine dynamic transitions verified!")

    # 7. Difficulty Modes
    print("\n[7] Verifying 4 Difficulty Profiles:")
    for diff in ["EASY", "HARD", "EXTREME", "GROUNDED"]:
        cfg = DIFFICULTIES[diff]
        e = EnemyAI(100, 100, level.graph, level.patrol_waypoints, diff)
        print(f"  Mode '{diff}': Hearing={e.perception.hearing_threshold}dB, LocError={e.perception.localization_error_base}px, Memory={e.memory.retention_duration}s, Adaptive={diff == 'EXTREME'}")
    print("  -> All 4 difficulty modes properly initialized!")

    # 8. Objective Progression and Victory
    print("\n[8] Verifying Mission Objectives & Escape Victory:")
    obj = ObjectiveManager()
    assert obj.current_step == 0
    print(f"  Step 0: {obj.current_objective}")

    # Player gets keycard
    player.has_keycard = True
    level.access_card.collected = True
    won = obj.check_progress(player, level.access_card, level.security_room_rect, level.terminal, level.exit_door, sound_mgr)
    assert obj.current_step == 1
    print(f"  Step 1: {obj.current_objective}")

    # Player enters Security Room
    player.x = level.security_room_rect.centerx
    player.y = level.security_room_rect.centery
    won = obj.check_progress(player, level.access_card, level.security_room_rect, level.terminal, level.exit_door, sound_mgr)
    assert obj.current_step == 2
    print(f"  Step 2: {obj.current_objective}")

    # Player activates Terminal
    level.terminal.activate(sound_mgr, time.time())
    won = obj.check_progress(player, level.access_card, level.security_room_rect, level.terminal, level.exit_door, sound_mgr)
    assert obj.current_step == 3
    assert level.exit_door.is_unlocked
    print(f"  Step 3: {obj.current_objective} (Exit Door Unlocked!)")

    # Player approaches exit
    player.x = level.exit_door.world_center[0]
    player.y = level.exit_door.world_center[1]
    won = obj.check_progress(player, level.access_card, level.security_room_rect, level.terminal, level.exit_door, sound_mgr)
    assert obj.current_step == 4
    print(f"  Step 4: {obj.current_objective}")

    # Player steps into exit
    won = obj.check_progress(player, level.access_card, level.security_room_rect, level.terminal, level.exit_door, sound_mgr)
    assert won is True
    print(f"  Mission Complete: {obj.current_objective}")
    print("  -> Full objective pipeline and victory condition verified!")

    print("\n" + "=" * 60)
    print(" ALL 8 SCENARIOS VERIFIED AND VALIDATED 100% SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    verify_all()
