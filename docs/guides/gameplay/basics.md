# 🎮 Gameplay Basics

## Overview

Alien Invasion is a classic Space Invaders-style game built with Pygame. You
pilot a ship at the bottom of the screen, destroy alien fleets, and advance
through progressively faster waves.

## Game Flow

1. **Start** the game from the main menu.
2. **Play** by moving the ship and firing bullets.
3. **Advance** when all aliens are destroyed.
4. **Game Over** occurs when you run out of ships.

## Core Mechanics

### Ship Control

- Move left and right
- Fire bullets
- Pause and resume the game

### Alien Behavior

- Move in formation
- Reverse direction at screen edges
- Drop down when changing direction
- Speed up as the game progresses

### Scoring

- Points are awarded per alien destroyed
- Score value increases as levels advance
- High scores are saved automatically

## Game States

The game tracks several states via `Statistics`:

- **Active**: gameplay is running
- **Paused**: gameplay is halted
- **Game Over**: no ships remaining

## Audio

The game includes background music and sound effects. You can toggle both at
runtime using keyboard shortcuts.
