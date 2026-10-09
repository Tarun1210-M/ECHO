"""
ECHO 3D -- AI THAT HEARS YOU
===========================
Direct 3D First-Person Launcher powered by the Ursina Engine.
Features:
- 3D First-person navigation with headlamp & volumetric fog
- 3D Ballistic projectile throwing physics
- 3D Acoustic shockwaves expanding on the floor
- Un-faked A* pathfinding, heapq PriorityQueue, and BFS room clearing
- Fullscreen by default
"""

import sys

if __name__ == "__main__":
    from game3d.game_3d import start_3d_game
    print("=" * 60)
    print(" ECHO 3D -- AI THAT HEARS YOU")
    print(" Launching 3D First-Person Stealth Experience...")
    print("=" * 60)
    use_fullscreen = "--windowed" not in sys.argv
    selected_diff = None
    for i, arg in enumerate(sys.argv):
        arg_l = arg.lower().lstrip("-")
        if arg_l in ("easy", "medium", "hard", "extreme", "grounded"):
            selected_diff = arg_l.upper()
        elif arg_l == "difficulty" and i + 1 < len(sys.argv):
            selected_diff = sys.argv[i + 1].upper()

    try:
        start_3d_game(fullscreen=use_fullscreen, difficulty=selected_diff)
    except Exception as e:
        import traceback
        print(f"\n[ERROR] 3D Engine encountered an exception: {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
