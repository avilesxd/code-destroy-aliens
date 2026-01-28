# 💯 Scoring System

## Overview

Scoring is based on alien eliminations and scales as the game progresses.

## Points per Alien

Each alien destroyed awards the current `alien_points` value from configuration.
This value increases as levels advance.

## Level Scaling

When you clear a wave, the game:

- Starts a new fleet
- Increases speed via `boost_speed()`
- Increases score value via `score_scale`

## High Score

High scores are tracked and saved automatically with encrypted persistence.

## Tips

- Clear waves efficiently to reach higher scoring levels.
- Avoid losing ships to maintain momentum.

## Next Steps

- Learn about [Game Modes](modes.md)
- Master the [Controls](controls.md)
