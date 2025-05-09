# 🎮 Gameplay Basics

## Game Overview

Alien Invasion is a modern take on the classic Space Invaders game, featuring
unique mechanics and modern graphics. The game is built using Pygame and offers
a smooth, engaging experience.

## Game Flow

1. **Main Menu**

    - Start Game
    - Options
    - Controls
    - Exit

2. **Main Game**

    - Control your spaceship
    - Shoot down aliens
    - Avoid enemy fire
    - Collect power-ups
    - Score points

3. **Game Over**
    - View your score
    - Save statistics
    - Return to main menu

## Core Mechanics

### Ship Control

- Move your ship left and right
- Fire at aliens
- Collect power-ups
- Avoid collisions

### Alien Behavior

- Move in formation
- Shoot at the player
- Drop power-ups when destroyed
- Increase in speed and aggression as levels progress

### Scoring System

- Points for each alien destroyed
- Bonus points for completing levels
- High score tracking
- Statistics persistence

### Power-ups

- Extra lives
- Weapon upgrades
- Temporary shields
- Score multipliers

## Game States

The game features several states to manage different aspects of gameplay:

- **Menu State**: Main menu and options
- **Game State**: Active gameplay
- **Pause State**: Game paused
- **Game Over State**: End of game screen

## Localization

The game supports multiple languages through a JSON-based translation system:

- Automatic language detection
- Dynamic text rendering
- Easy addition of new languages

## Audio System

The game features a comprehensive audio system:

- Background music
- Sound effects
- Volume control
- Mute options
