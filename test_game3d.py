"""
test_game3d.py - Headless Verification of ECHO 3D Architecture and Subsystems
"""

import os
import sys
import math
import time

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from ursina import Ursina, Vec3, destroy

def test_3d_engine():
    print("[TEST 3D] Initializing headless Ursina environment...")
    app = Ursina(headless=True)

    from game3d.level_3d import Level3D, grid_to_world_3d, world_to_grid_3d
    from game3d.player_3d import Player3D
    from game3d.enemy_3d import EnemyAI3D
    from game3d.sound_system_3d import SoundManager3D
    from game3d.ui_3d import GameUI3D
    from game3d.game_3d import GameManager3D

    print("[TEST 3D] Testing 3D Level & Geometry...")
    level = Level3D()
    assert len(level.walls) > 0, "No 3D walls generated"
    assert len(level.doors) > 0, "No 3D doors generated"
    assert level.terminal is not None, "3D Terminal missing"
    assert level.exit_door is not None, "3D Exit Door missing"
    assert level.access_card is not None, "3D Access Card missing"
    print(f"  -> Generated {len(level.walls)} 3D bulkheads and {len(level.doors)} doors!")

    print("[TEST 3D] Testing 3D Sound & Floor Shockwaves...")
    sound_mgr = SoundManager3D()
    test_event = sound_mgr.emit_sound(
        position=(10.0, 10.0),
        intensity=75.0,
        sound_type="throw_impact",
        timestamp=time.time()
    )
    assert test_event is not None
    print("  -> 3D Acoustic system and shockwaves verified!")

    print("[TEST 3D] Testing 3D Hunter AI (A* & PriorityQueue in 3D)...")
    player = Player3D(level.player_start_pos)
    enemy = EnemyAI3D(
        start_pos=level.enemy_start_pos,
        grid_graph=level.graph,
        patrol_waypoints=level.patrol_waypoints,
        difficulty="HARD"
    )
    enemy.set_player_and_sound_manager(player, sound_mgr)
    assert enemy.state_machine.current_state_name == "PATROL"
    assert hasattr(enemy, 'torso'), "Enemy missing cybernetic torso chassis"
    assert hasattr(enemy, 'right_arm'), "Enemy missing articulated hydraulic right arm"
    assert hasattr(enemy, 'knuckle_glow'), "Enemy missing high-tech knuckle glow emitter"

    # Test High-Tech Knock Animations
    print("[TEST 3D] Testing High-Tech Knocking Animations & Echolocation...")
    enemy.perform_door_knock(level.doors[0])
    assert enemy.knock_mode == "DOOR_KNOCK", "Enemy should enter DOOR_KNOCK mode"
    enemy.trigger_sonar_scan(time.time())

    enemy.perform_knock_attack()
    assert enemy.knock_mode == "PLAYER_STRIKE", "Enemy should enter PLAYER_STRIKE mode"

    # Test Player Knockdown Simulation
    player.knock_down()
    assert player.is_knocked_down, "Player should be in knocked down state"
    player.reset_knockdown()
    assert not player.is_knocked_down, "Player knockdown should reset"
    print("  -> High-tech knocking animations, sonar scan, and player knockdown verified!")

    # Test 3D A* Pathfinding
    has_path = enemy.compute_path_to((20.0, 20.0))
    assert has_path, "3D A* failed to find path"
    assert len(enemy.current_path) > 0
    print(f"  -> 3D A* computed path with {len(enemy.current_path)} 3D waypoints!")

    print("[TEST 3D] Testing 3D Manager Simulation Loop & Entity Updates...")
    manager = GameManager3D(fullscreen=False)
    assert manager.game_state == "MENU", "Game should start in MENU state"

    # 1. Test Difficulty Selection via input
    manager.on_input('2')
    assert manager.game_state == "PLAYING", "Should transition to PLAYING on key '2'"
    assert manager.difficulty == "MEDIUM", f"Expected MEDIUM, got {manager.difficulty}"
    print("  -> Menu difficulty selection confirmed!")

    # 2. Test Simulation update frames
    for _ in range(30):
        manager.update()
        app.step()

    # 3. Test Interaction Prompt near Keycard
    if manager.level.access_card:
        manager.player.position = Vec3(manager.level.access_card.position)
        manager.update()
        assert manager.ui.prompt_text.enabled, "Interaction prompt should be enabled near keycard"
        assert "Keycard" in manager.ui.prompt_text.text, f"Unexpected prompt text: {manager.ui.prompt_text.text}"
        print(f"  -> Context interaction prompt verified: '{manager.ui.prompt_text.text}'")

        # Pick up keycard via input('e')
        manager.on_input('e')
        assert manager.player.has_keycard, "Player should have collected keycard"
        print("  -> 'E' keycard interaction collected successfully!")

    # 4. Test Pause Menu & Resume
    manager.on_input('escape')
    assert manager.game_state == "PAUSED", "Game should be PAUSED after ESC"
    assert manager.ui.pause_panel.enabled, "Pause panel should be visible"
    print("  -> Pause menu activated on ESC!")

    manager.on_input('1')  # Resume
    assert manager.game_state == "PLAYING", "Game should resume to PLAYING"
    assert not manager.ui.pause_panel.enabled, "Pause panel should be hidden"
    print("  -> Mission resumed successfully!")

    # 5. Test Field Manual Overlay ('H' key)
    manager.on_input('h')
    assert manager.ui.help_panel.enabled, "Help manual should be enabled on 'h'"
    manager.on_input('h')
    assert not manager.ui.help_panel.enabled, "Help manual should toggle off on 'h'"
    print("  -> In-field tactical help manual verified!")

    # 6. Test Debriefing Screen on Game Over and Victory
    manager.trigger_game_over()
    assert manager.game_state == "GAME_OVER"
    assert manager.ui.debrief_panel.enabled, "Debrief panel should be visible on game over"
    assert "FAILED" in manager.ui.debrief_title.text
    print("  -> Tactical failure debriefing screen verified!")

    manager.on_input('r')
    assert manager.game_state == "PLAYING"
    assert not manager.ui.debrief_panel.enabled

    manager.trigger_victory()
    assert manager.game_state == "VICTORY"
    assert manager.ui.debrief_panel.enabled, "Debrief panel should be visible on victory"
    assert "SUCCESSFUL" in manager.ui.debrief_title.text
    print("  -> Tactical victory debriefing screen verified!")

    # Return to menu via 'd'
    manager.on_input('d')
    assert manager.game_state == "MENU"
    assert manager.ui.menu_panel.enabled
    print("  -> Reconfigure difficulty return to menu confirmed!")

    # 7. Test Restart Game
    manager.start_game_with_difficulty("EASY")
    manager.restart_game()
    assert manager.game_state == "PLAYING"
    assert not manager.player.has_keycard, "Keycard should be reset on restart"
    assert (manager.player.position - manager.level.player_start_pos).length() < 0.1, "Player should be at spawn point"
    print("  -> Mission restart verified!")

    print("\n[ALL 3D ENGINE TESTS PASSED SUCCESSFULLY!]")

if __name__ == "__main__":
    test_3d_engine()
