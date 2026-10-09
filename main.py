"""
ECHO -- AI THAT HEARS YOU
========================
"The enemy doesn't need to see you. It only needs to hear you."

Unified launcher for ECHO:
- Default: 3D First-Person Mode (Ursina Engine)
- Use 'python main.py --2d' or 'python main_2d.py' for 2D Tactical Top-Down Mode
- Use 'python main.py --3d' or 'python main_3d.py' for 3D First-Person Mode
"""

import sys
import os

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def launch_3d():
    print("[Launcher] Starting ECHO 3D First-Person Experience (Ursina Engine)...")
    from game3d.game_3d import start_3d_game
    use_fullscreen = "--windowed" not in sys.argv
    selected_diff = None
    for i, arg in enumerate(sys.argv):
        arg_l = arg.lower().lstrip("-")
        if arg_l in ("easy", "medium", "hard", "extreme", "grounded"):
            selected_diff = arg_l.upper()
        elif arg_l == "difficulty" and i + 1 < len(sys.argv):
            selected_diff = sys.argv[i + 1].upper()
    start_3d_game(fullscreen=use_fullscreen, difficulty=selected_diff)


def launch_2d():
    print("[Launcher] Starting ECHO 2D Top-Down Tactical Experience (Pygame Engine)...")
    from game.game import GameManager
    app = GameManager()
    app.run()


def main():
    print("=" * 60)
    print(" ECHO -- AI THAT HEARS YOU")
    print(" 'The enemy doesn't need to see you. It only needs to hear you.'")
    print("=" * 60)

    # Check CLI options
    if "--2d" in sys.argv:
        launch_2d()
    elif "--3d" in sys.argv:
        launch_3d()
    else:
        # Default to 3D mode
        print("Launching in 3D Mode (Press ESC to quit).")
        print("Tip: Run 'python main.py --2d' to switch to the 2D Top-Down Mode anytime.")
        try:
            launch_3d()
        except Exception as e:
            print(f"[Launcher] 3D launch failed ({e}), falling back to 2D Mode...")
            launch_2d()


if __name__ == "__main__":
    main()
