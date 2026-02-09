<img width="1002" height="915" alt="image" src="https://github.com/user-attachments/assets/16d5f16c-2677-4e51-ab01-e497644b91c9" />


# 🐸 Frogger: Enhanced Graphics Edition


![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![Pygame](https://img.shields.io/badge/library-Pygame-green.svg)
![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-red.svg)

**Frogger Enhanced** is a modern, high-quality implementation of the classic arcade game. The project focuses on **procedural graphics** (100% code-generated) and advanced visual effects, eliminating the need for external image files.

### 🎮 Gameplay Preview
The game offers a unique visual experience through real-time code rendering:
* **Rich Procedural Details:** Logs featuring visible wood grain and vehicles with rendered headlights and underbody shadows.
* **Advanced Water Rendering:** The river background utilizes gradients and geometric patterns to simulate depth and movement.
* **Clean User Interface (UI):** Real-time score display, lives represented by heart icons, and a footer with author information.

---

## 🌟 Key Features

* **Procedural Graphics:** All elements (frog, cars, logs) are drawn dynamically using graphical primitives, gradients, and trigonometric functions.
* **Particle Engine:**
    * **Water Splashes:** Generated upon contact with the river.
    * **Jump Dust:** Subtle effects triggered by every frog movement.
    * **Collision Sparks:** Intense effects upon colliding with a vehicle.
* **Dynamic Environment:** A river featuring wave animation (sinusoidal color shifts) and vehicles equipped with a lighting system (headlights).
* **Persistent Storage:** Automatic saving of the top 5 high scores in JSON format within a hidden `.polsoft` system folder.

---

## 🛠️ Technical Specification

The game was developed using the Object-Oriented Programming (OOP) paradigm, allowing for easy expansion:

* **`ConfigManager`**: Handles reading/writing configurations and scores (cross-platform).
* **`ParticleSystem`**: An independent engine managing the lifecycle, gravity, and transparency of particles.
* **`WaterEffect`**: An algorithm that renders the animated water surface in real-time.
* **`Vehicle` & `Log`**: Entity classes featuring position wrapping logic.

---

## 🚀 Installation and Launch

### Requirements
* Python 3.10 or newer
* Pygame library

### Quick Start
1.  **Install Pygame:**
    ```bash
    pip install pygame
    ```
2.  **Run the game:**
    ```bash
    python frogger.py
    ```

---

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| **Arrows (↑ ↓ ← →)** | Move Frog / Menu Navigation |
| **Enter** | Start Game / Confirm |
| **Esc** | Exit / Return to Menu |

---

## 📂 Data Location
Scores and settings are stored in:
* **Windows:** `%USERPROFILE%\.polsoft\games\Frogger.json`
* **Linux/Mac:** `~/.polsoft/games/Frogger.json`

---

## 📝 Author Information
* **Author:** Sebastian Januchowski
* **Organization:** polsoft.ITS™ London
* **Version:** 2.0.0 (Production)
* **Status:** Stable

© 2026 Sebastian Januchowski. All Rights Reserved. A polsoft.ITS™ London project.
