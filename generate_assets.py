"""
generate_assets.py - Exports synthesized sound effects to assets/sounds/ as standard WAV files.
"""

import os
import wave
import numpy as np

def save_wav(filename: str, mono_arr: np.ndarray, sample_rate: int = 44100):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    clamped = np.clip(mono_arr, -1.0, 1.0)
    int16_arr = (clamped * 32767).astype(np.int16)
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int16_arr.tobytes())

def generate_wavs():
    sr = 44100
    out_dir = os.path.join("assets", "sounds")
    os.makedirs(out_dir, exist_ok=True)

    # 1. Footstep Crouch
    t = np.linspace(0, 0.08, int(sr * 0.08), endpoint=False)
    w = np.sin(2 * np.pi * 90 * np.exp(-t * 28) * t) * np.exp(-t * 22) * 0.2
    save_wav(os.path.join(out_dir, "footstep_crouch.wav"), w, sr)

    # 2. Footstep Walk
    t = np.linspace(0, 0.10, int(sr * 0.10), endpoint=False)
    w = (np.sin(2 * np.pi * 130 * np.exp(-t * 28) * t) + (np.random.rand(len(t)) * 2 - 1) * 0.2) * np.exp(-t * 22) * 0.45
    save_wav(os.path.join(out_dir, "footstep_walk.wav"), w, sr)

    # 3. Footstep Run
    t = np.linspace(0, 0.14, int(sr * 0.14), endpoint=False)
    w = (np.sin(2 * np.pi * 180 * np.exp(-t * 28) * t) + (np.random.rand(len(t)) * 2 - 1) * 0.25) * np.exp(-t * 22) * 0.85
    save_wav(os.path.join(out_dir, "footstep_run.wav"), w, sr)

    # 4. Bottle impact / throw crash
    t = np.linspace(0, 0.65, int(sr * 0.65), endpoint=False)
    crack = (np.random.rand(len(t)) * 2 - 1) * np.exp(-t * 35.0)
    ring = (np.sin(2 * np.pi * 1420 * t) * np.exp(-t * 8.0) + np.sin(2 * np.pi * 2840 * t) * np.exp(-t * 12.0)) * 0.4
    save_wav(os.path.join(out_dir, "throw_impact.wav"), (crack * 0.7 + ring) * 0.8, sr)

    # 5. Door Servo
    t = np.linspace(0, 0.55, int(sr * 0.55), endpoint=False)
    freq = 220.0 + 80.0 * np.sin(np.pi * t / 0.55)
    w = np.sin(2 * np.pi * freq * t) * (np.sin(np.pi * t / 0.55) ** 0.5) * 0.5
    save_wav(os.path.join(out_dir, "door_servo.wav"), w, sr)

    # 6. Terminal Chime
    t = np.linspace(0, 0.45, int(sr * 0.45), endpoint=False)
    w = (np.sin(2 * np.pi * 587.33 * t) * np.exp(-t * 5.0) + np.sin(2 * np.pi * 880.0 * t) * np.exp(-t * 6.0)) * 0.45
    save_wav(os.path.join(out_dir, "terminal_chime.wav"), w, sr)

    # 7. Keycard Pickup
    t = np.linspace(0, 0.35, int(sr * 0.35), endpoint=False)
    w = np.sin(2 * np.pi * 1046.50 * t) * np.exp(-t * 7.0) * 0.5
    save_wav(os.path.join(out_dir, "keycard_pickup.wav"), w, sr)

    # 8. AI Alert Stinger
    t = np.linspace(0, 0.90, int(sr * 0.90), endpoint=False)
    w = np.sin(2 * np.pi * (85 + 10 * np.sin(2 * np.pi * 4 * t)) * t) * np.sin(np.pi * t / 0.9) * 0.65
    save_wav(os.path.join(out_dir, "ai_alert.wav"), w, sr)

    # 9. AI Scream / Chase
    t = np.linspace(0, 1.10, int(sr * 1.10), endpoint=False)
    f1 = 220.0 + 120.0 * (t / 1.1)
    f2 = 311.13 + 170.0 * (t / 1.1)
    w = (0.5 * np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)) * (np.sin(np.pi * t / 1.1) ** 0.3) * 0.7
    save_wav(os.path.join(out_dir, "ai_chase.wav"), w, sr)

    # 10. Ambient Drone
    t = np.linspace(0, 2.0, int(sr * 2.0), endpoint=False)
    w = np.sin(2 * np.pi * (55.0 + 2.0 * np.sin(2 * np.pi * 0.5 * t)) * t) * 0.25
    save_wav(os.path.join(out_dir, "ambient_drone.wav"), w, sr)

    print(f"[Assets] Generated 10 WAV sound effects in {out_dir}")

if __name__ == "__main__":
    generate_wavs()
