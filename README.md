🎮 Shmebulock – Python Endless Runner (Hackathon Project)
A fast-paced endless runner developed in Python (Pygame Zero) as part of a hackathon, built by a team of 4.

The player must jump over and dodge incoming obstacles while the game progressively speeds up. The goal is to survive as long as possible.


🧠 Overview
Shmebulock is an arcade-style endless runner focused on obstacle avoidance and speed progression. The game features two types of enemies, a lives system, and dynamic difficulty scaling tied to the player's jump count.

This project was developed collaboratively during a hackathon. My personal contributions focused on the core engine-side systems rather than visuals or game design.


👤 My Contributions
Parallax Scrolling System: Implemented a dual-layer scrolling background with independent speed multipliers to create a depth effect

Speed Progression System: Designed a dynamic game speed system that scales based on the player's jump count, increasing difficulty over time

Obstacle Spawn & Timing System: Built the enemy spawn logic with randomized intervals that shorten as the game progresses, keeping difficulty balanced yet challenging


🎮 Core Features

Endless Runner Loop: Continuous scrolling with no predefined end

Two Enemy Types: Ground boxes and oscillating flying enemies

Lives System: 3 lives with invincibility frames after taking damage

Dynamic Difficulty: Speed and spawn rate increase the longer you survive

Game States: Start screen, gameplay, pause, and game over screens

Sprite Animation: Frame-based hero and environment animations


🕹️ Controls

InputActionSPACEJumpENTERStart / Pause / Resume / Restart


🛠️ Built With

Python 3

Pygame Zero (pgzero)

PyInstaller (for Windows build)


👥 Development

Team size: 4 people

Context: Hackathon project

My role: Gameplay Programmer

My focus: Background scrolling, speed progression, spawn & timing systems
