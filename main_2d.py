"""
ECHO 2D -- AI THAT HEARS YOU
===========================
Tactical Top-Down Stealth Experience (Pygame Engine).
Fullscreen with F3 AI Debug telemetry overlay.
"""

import sys

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

from game.game import GameManager

if __name__ == "__main__":
    print("=" * 60)
    print(" ECHO 2D -- AI THAT HEARS YOU")
    print(" Launching 2D Tactical Stealth Mode (Pygame)...")
    print("=" * 60)
    app = GameManager()
    app.run()
