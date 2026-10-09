# ECHO — The AI That Hears You

> *"The enemy doesn't need to see you. It only needs to hear you."*

**ECHO** is an advanced AI stealth game engineered in Python 3, featuring both:
- **ECHO 3D (Default)**: Full First-Person 3D horror stealth experience powered by the **Ursina 3D Engine**, featuring first-person flashlight illumination, volumetric facility fog, 3D floor acoustic shockwaves, and 3D ballistic bottle physics.
- **ECHO 2D**: Tactical Top-Down stealth experience powered by **Pygame**, featuring dynamic radial darkness lighting, tactical HUD, mini-map, and comprehensive F3 debug telemetry.

Both versions share the exact same un-faked artificial intelligence decision-making and fundamental Data Structures & Algorithms (DSA):
- **A\* Pathfinding** with Octile heuristics and Line-of-Sight string-pulling smoothing.
- **Priority Queue (Min/Max Heap using `heapq`)** for multi-sensory acoustic stimulus triaging.
- **Breadth-First Search (BFS)** for area investigation and corner sweeping.
- **Hierarchical Finite State Machine (FSM)** with clean object-oriented state classes.
- **Acoustic Physics Model** with distance attenuation, obstacle raycasting, and Gaussian localization error.
- **Episodic Memory Decay** with spatial threat clustering.
- **Statistical Adaptive Counter-Tactics** (Extreme Mode) that learns from repetitive player distractions.
- **Procedural Synthesizer Engine** (NumPy + Pygame Mixer) providing 10 standalone sound effects without requiring external downloads or assets.

---

## Table of Contents
1. [Overview & Core Concept](#overview--core-concept)
2. [Installation & Quick Start](#installation--quick-start)
3. [Controls](#controls)
4. [AI & DSA Architecture](#ai--dsa-architecture)
   - [A* Pathfinding Algorithm](#1-a-pathfinding-algorithm)
   - [Priority Queue Sensory Triaging](#2-priority-queue-sensory-triaging)
   - [BFS Area Search & Room Clearing](#3-bfs-area-search--room-clearing)
   - [Acoustic Propagation & Wall Attenuation](#4-acoustic-propagation--wall-attenuation)
   - [Imperfect Sound Localization](#5-imperfect-sound-localization)
   - [Suspicion Dynamics & Episodic Memory](#6-suspicion-dynamics--episodic-memory)
   - [Finite State Machine (FSM)](#7-finite-state-machine-fsm)
   - [Adaptive AI (Extreme Mode)](#8-adaptive-ai-extreme-mode)
5. [Operational Difficulty Modes](#operational-difficulty-modes)
6. [Mission Progression & Objectives](#mission-progression--objectives)
7. [F3 Developer / Viva Telemetry Overlay](#f3-developer--viva-telemetry-overlay)
8. [Project File Structure](#project-file-structure)
9. [Viva & Technical Interview Guide](#viva--technical-interview-guide)
10. [Future Improvements](#future-improvements)

---

## Overview & Core Concept

You are an operative trapped inside the decommissioned **Site-9 Aetheria Research Facility**. The complex is stalked by an experimental acoustic predator. 

Unlike traditional stealth games where enemies have omniscient vision cones or artificial radar, **the Hunter is blind in darkness**. It hunts through sound alone. Every footstep, every sliding bulkhead door, and every distraction bottle thrown sends physical acoustic shockwaves through the corridors.

The core gameplay centers on **psychological acoustic manipulation**:
1. Sneaking silently to stay below the Hunter's hearing threshold.
2. Throwing glass bottles and metal cans to lure the Hunter into adjacent rooms.
3. Exploiting acoustic wall damping to sprint when thick bulkheads isolate you from the creature.

---

## Installation & Quick Start

### Prerequisites
- Python 3.10+ (tested on Python 3.10 & 3.11)
- Windows / Linux / macOS

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Dependencies: `ursina>=7.0.0`, `pygame>=2.5.0`, `numpy>=1.24.0`)*

### 2. Launch the Game
- **Launch 3D First-Person Mode (Default)**:
  ```bash
  python main.py
  # or directly:
  python main_3d.py
  ```
- **Launch 2D Tactical Top-Down Mode**:
  ```bash
  python main.py --2d
  # or directly:
  python main_2d.py
  ```

### 3. Run Automated Test Suites
```bash
python test_game3d.py
python test_game.py
python verify_gameplay_scenarios.py
```

---

## Controls

| Key / Input | Action | Acoustic Impact |
| :--- | :--- | :--- |
| **W / A / S / D** | Movement | Normal Walk: **16 dB** (moderate) |
| **LEFT SHIFT** | Sprint | Heavy Footsteps: **48 dB** (loud!) |
| **LEFT CTRL** | Crouch Sneak | Muffled Steps: **3 dB** (near-silent) |
| **E** | Interact | Pick up items, toggle doors (**40 dB**), hack mainframe (**28 dB**) |
| **F** or **Left Click** | Aim & Throw Bottle | Shatter Clatter: **75 dB** (lures AI across facility!) |
| **F3** | Toggle AI Debug Telemetry | Displays A* path lines, BFS nodes, memory decay, and localization error |
| **F11** or **Alt+Enter** | Toggle Fullscreen / Windowed | Automatically scales display canvas to native monitor resolution |
| **ESC** | Pause Menu | Resume, restart, or return to main menu |

---

## AI & DSA Architecture

```
                    ┌────────────────────────┐
                    │      PLAYER ACTION     │
                    │ Crouch / Walk / Sprint │
                    └───────────┬────────────┘
                                │ Emits SoundEvent(pos, intensity, type)
                                ▼
                    ┌────────────────────────┐
                    │   ACOUSTIC PROPAGATION │
                    │ - Euclidean Distance   │
                    │ - Raycast Wall Damping │
                    └───────────┬────────────┘
                                │
                  [Perceived Intensity >= Threshold?]
                     ├── NO  ──> Sound Ignored
                     └── YES ──> Add Localization Error (Gaussian Noise)
                                │
                                ▼
                    ┌────────────────────────┐
                    │    PRIORITY QUEUE      │
                    │  (heapq Max-Heap)      │
                    └───────────┬────────────┘
                                │ Pops Highest Intensity Event First
                                ▼
                    ┌────────────────────────┐
                    │     AI DECISION        │
                    │ - Suspicion Manager    │
                    │ - Episodic Memory Store│
                    └───────────┬────────────┘
                                │
                                ▼
         ┌──────────────────────────────────────────────────┐
         │              FINITE STATE MACHINE                │
         │  PATROL ──> INVESTIGATE ──> SEARCH ──> CHASE     │
         │    ▲              │           │          │       │
         │    │              ▼           ▼          ▼       │
         │    └──────── A* Pathfinding   BFS Sweep  Attack  │
         └──────────────────────────────────────────────────┘
```

### 1. A* Pathfinding Algorithm
Located in [`dsa/astar.py`](file:///c:/Users/Personal%20Pc/OneDrive/Desktop/New%20folder/dsa/astar.py).
- **Graph Representation**: 2D tile grid ([`dsa/graph.py`](file:///c:/Users/Personal%20Pc/OneDrive/Desktop/New%20folder/dsa/graph.py)) where walkable tiles are vertices and impassable bulkheads are blocked.
- **Cost Formulation**:
  $$f(n) = g(n) + h(n)$$
  - $g(n)$: Exact path cost accumulated from the start node to node $n$ (orthogonal = $1.0$, diagonal = $\sqrt{2} \approx 1.414$).
  - $h(n)$: **Octile Distance** heuristic:
    $$h(n) = (|dx| + |dy|) + (\sqrt{2} - 2) \cdot \min(|dx|, |dy|)$$
    Admissible and consistent, ensuring optimal shortest paths.
- **Path Smoothing (String-Pulling)**: Removes zigzagging grid artifacts using Bresenham line-of-sight raycasting.

### 2. Priority Queue Sensory Triaging
Located in [`dsa/priority_queue.py`](file:///c:/Users/Personal%20Pc/OneDrive/Desktop/New%20folder/dsa/priority_queue.py).
- Powered by Python's `heapq` standard library module.
- If multiple sounds occur simultaneously (e.g. Crouch Footstep $3\text{ dB}$, Running $48\text{ dB}$, and Thrown Bottle Smash $75\text{ dB}$):
  $$\text{Priority} = -\text{Intensity}$$
- The AI prioritizes the loudest/most critical event first, making distraction mechanics mathematically guaranteed.

### 3. BFS Area Search & Room Clearing
Located in [`dsa/bfs_search.py`](file:///c:/Users/Personal%20Pc/OneDrive/Desktop/New%20folder/dsa/bfs_search.py).
- When the Hunter reaches an estimated sound target and finds nothing, it initiates the `SEARCH` state.
- **Breadth-First Search** traverses outwards from the target cell using a FIFO queue (`collections.deque`).
- Identifies tactical corners, alcoves, and hiding niches (cells with $\ge 2$ adjacent walls) to sweep the room systematically.

### 4. Acoustic Propagation & Wall Attenuation
Located in [`ai/perception.py`](file:///c:/Users/Personal%20Pc/OneDrive/Desktop/New%20folder/ai/perception.py).
- **Distance Attenuation**:
  $$\text{decayed\_intensity} = \frac{\text{intensity}}{1.0 + \text{distance} \cdot \alpha}$$
- **Obstacle Penetration Damping**:
  Uses Bresenham raycasting to count wall tiles intersecting the direct acoustic ray:
  $$\text{transmission} = (1.0 - \text{damping\_factor})^{\text{wall\_count}}$$
  $$\text{perceived\_intensity} = \text{decayed\_intensity} \cdot \text{transmission}$$
  Thick walls muffle running sounds into near-silent murmurs.

### 5. Imperfect Sound Localization
Located in [`ai/perception.py`](file:///c:/Users/Personal%20Pc/OneDrive/Desktop/New%20folder/ai/perception.py).
- The Hunter is **never** given the player's true coordinates.
- Localization error is inversely proportional to perceived clarity:
  $$\sigma = \text{base\_error} \cdot \left(1.0 - 0.75 \cdot \frac{\text{perceived\_intensity}}{75.0}\right)$$
  $$\text{Estimated Pos} = \text{True Pos} + \mathcal{N}(0, \sigma^2)$$
  A distant or muffled sound produces a large search circle; a loud crash right nearby gives pinpoint precision.

### 6. Suspicion Dynamics & Episodic Memory
Located in [`ai/decision.py`](file:///c:/Users/Personal%20Pc/OneDrive/Desktop/New%20folder/ai/decision.py) and [`ai/memory.py`](file:///c:/Users/Personal%20Pc/OneDrive/Desktop/New%20folder/ai/memory.py).
- **Continuous Suspicion Index**: $0 \le S \le 100$.
  - $0 - 20$: **CALM** (Routine patrol circuit)
  - $20 - 50$: **SUSPICIOUS** (Investigates acoustic anomaly)
  - $50 - 80$: **ALERT** (Aggressive multi-node sweep)
  - $80 - 100$: **HUNT** (Target locked, sprinting chase)
- **Episodic Decay**: Remembers recent sounds with exponential half-life decay:
  $$\text{strength}(t) = \text{strength}_0 \cdot 2^{-\frac{\Delta t}{t_{1/2}}}$$
- **Spatial Threat Clustering**: Repeated sounds in the same corridor accumulate spatial threat bonuses, rapidly pushing the AI into ALERT mode.

### 7. Finite State Machine (FSM)
Located in [`ai/state_machine.py`](file:///c:/Users/Personal%20Pc/OneDrive/Desktop/New%20folder/ai/state_machine.py).
Object-oriented state classes implementing `enter()`, `update()`, and `exit()`:
- `PatrolState`: Walks pre-calculated facility patrol loop.
- `InvestigateState`: Navigates via A* to prioritized sound location.
- `SearchState`: Sweeps BFS corner nodes around target.
- `AlertState`: High vigilance state checking recent memory hotspots.
- `ChaseState`: Full sprint pursuit with dynamic A* re-pathing.
- `AttackState`: Captures player within grab proximity.
- `ReturnToPatrolState`: A* pathfinding back to nearest patrol route node.

### 8. Adaptive AI (Extreme Mode)
Located in [`ai/behavior.py`](file:///c:/Users/Personal%20Pc/OneDrive/Desktop/New%20folder/ai/behavior.py).
Statistical model tracking:
- **Distraction Skepticism**: If the player throws 3+ distraction bottles in under 45 seconds, the AI increases skepticism ($\le 0.85$). Instead of running blindly to the bottle crash, it traces a vector backward toward the thrower's likely origin point!
- **Corridor Preference**: Biases patrol circuits toward sectors where the player spends the most time.

---

## Operational Difficulty Modes

| Difficulty | Hearing Threshold | Localization Error | Memory Retention | Speed Multiplier | Adaptive AI |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **EASY** | $6.0\text{ dB}$ | $\pm 130\text{ px}$ | $8.0\text{ s}$ | $0.88\times$ | No |
| **HARD** *(Default)* | $3.0\text{ dB}$ | $\pm 70\text{ px}$ | $18.0\text{ s}$ | $1.00\times$ | No |
| **EXTREME** | $1.5\text{ dB}$ | $\pm 35\text{ px}$ | $28.0\text{ s}$ | $1.15\times$ | **Yes** (Distraction skepticism & prediction) |
| **GROUNDED** | $2.5\text{ dB}$ | $\pm 65\text{ px}$ | $20.0\text{ s}$ | $1.00\times$ | No (Pure physical acoustic simulation) |

---

## Mission Progression & Objectives

1. **Find the Security Keycard**: Hidden in either Specimen Lab A or Quarantine Storage (randomized each playthrough).
2. **Infiltrate Security Operations Center (SOC)**: Unlock the restricted southern door using the keycard.
3. **Override Facility Terminal**: Access the mainframe to release the security quarantine and open the blast exit.
4. **Reach Extraction Airlock**: Navigate past the alert Hunter to the heavy blast doors at the east end of the complex.
5. **Escape Facility**: Cross the threshold to complete the mission and receive your Stealth Performance Evaluation (**S**, **A**, **B**, or **C** Rank).

---

## F3 Developer / Viva Telemetry Overlay

Press **`F3`** at any point during gameplay to toggle real-time telemetry:
- **A\* Path Line**: Visualized in green/cyan connecting navigation nodes.
- **BFS Search Nodes**: Displayed as purple circles (`BFS_1`, `BFS_2`, etc.) showing tactical corner investigation points.
- **Imperfect Localization Vector**: Yellow crosshair showing the AI's estimated sound position, connected to the true sound source with a dashed error line.
- **Hearing Radius & Vision Cone**: Displaying detection boundaries.
- **Telemetry HUD**: Continuous readout of FSM State, Suspicion %, Priority Queue size, Active Memory count, and Adaptive Skepticism rating.

---

## Project File Structure

```
ECHO/
│
├── main.py                     # Application entry point with DPI scaling
├── requirements.txt           # Python package dependencies
├── README.md                  # Comprehensive documentation and viva guide
├── test_game.py               # Automated unit tests for DSA and AI
├── verify_gameplay_scenarios.py # End-to-end scenario verification
├── generate_assets.py         # Procedural WAV sound asset exporter
│
├── game/                      # Core Game Engine
│   ├── __init__.py
│   ├── game.py                # State manager, menus, and game loop
│   ├── settings.py            # Physics, tuning constants, and color palette
│   ├── level.py               # Facility layout, room generation, and collision
│   ├── player.py              # Player kinematics, noise generation, and inventory
│   ├── enemy.py               # AI Hunter entity integrating all subsystems
│   ├── objects.py             # Doors, keycards, terminals, and throwable physics
│   ├── sound_system.py        # Sound manager, ripples, and procedural synth
│   ├── objectives.py          # Mission objective pipeline
│   └── ui.py                  # Lighting shader, HUD, mini-map, and F3 telemetry
│
├── ai/                        # Artificial Intelligence Subsystems
│   ├── __init__.py
│   ├── state_machine.py       # Object-oriented Finite State Machine (FSM)
│   ├── perception.py          # Sound propagation, wall damping, and localization
│   ├── memory.py              # Episodic memory with exponential decay
│   ├── decision.py            # Continuous suspicion system (0-100)
│   └── behavior.py            # Statistical adaptive behavior model
│
├── dsa/                       # Data Structures & Algorithms
│   ├── __init__.py
│   ├── astar.py               # A* search with Octile heuristic & path smoothing
│   ├── priority_queue.py      # Min/Max Heap wrapper via heapq
│   ├── bfs_search.py          # Breadth-First Search for corner/alcove clearing
│   └── graph.py               # 2D GridGraph & Bresenham acoustic raycasting
│
├── assets/                    # Standalone Media Assets
│   ├── sounds/                # 10 Synthesized 16-bit 44.1kHz WAV sound effects
│   ├── images/
│   └── fonts/
│
└── data/
    └── level.json             # Facility layout room data & acoustic thresholds
```

---

## Viva & Technical Interview Guide

### Q1: How does A* differ from Dijkstra's and Greedy Best-First Search?
**Answer**:
- **Dijkstra** uses only $g(n)$ (cost from start), exploring in all directions uniformly without goal direction.
- **Greedy Best-First** uses only $h(n)$ (heuristic to goal), which is fast but prone to suboptimal paths and dead-ends.
- **A\*** combines both: $f(n) = g(n) + h(n)$. It guarantees the shortest path if $h(n)$ is admissible (never overestimates true cost) and consistent (satisfies the triangle inequality), while guiding search efficiently toward the goal.

### Q2: Why is `heapq` used for sound triaging instead of a simple Python list or sorting?
**Answer**:
- Inserting into a sorted list takes $O(N)$ time. Sorting a list after each sound takes $O(N \log N)$.
- `heapq` implements a binary heap where insertion (`heappush`) and extraction of the maximum priority element (`heappop`) take $O(\log N)$ time. For real-time 60 FPS gameplay with frequent acoustic pulses, a heap offers optimal asymptotic and empirical performance.

### Q3: Why is BFS used for room searching instead of DFS or A*?
**Answer**:
- **BFS (Breadth-First Search)** explores vertices in concentric rings by distance from the starting node (level-by-level). This mirrors natural physical search behavior: checking immediate corners first before expanding outward.
- **DFS** dives deep down a single path, which would make the AI run across the room along a single wall before inspecting closer spots.

### Q4: How is acoustic wall damping implemented?
**Answer**:
- We use **Bresenham's Line Algorithm** to trace the straight ray between the sound source and the listener.
- We count the number of blocked wall tiles intersected by the ray.
- The perceived intensity is multiplied by $(1.0 - \text{damping\_factor})^{\text{wall\_count}}$, exponentially diminishing the sound energy for every structural wall penetrated.

---

## Future Improvements
- **Dynamic Re-mesh FOV Shadow Casting**: Expand 2D darkness mask into real-time polygonal 2D raycast shadows.
- **Spatial 3D Panning**: Stereo panning of sound effects based on relative listener angle.
- **Multi-Agent Patrols**: Cooperative hunting using hierarchical task networks (HTN).
- **Procedural Level Generation**: Cellular automata or BSP dungeon generation for infinite facility layouts.

---

**Developed with Python, Pygame, and NumPy for advanced AI & DSA demonstration.**
