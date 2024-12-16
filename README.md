# Life in Space - Game

## Overview

**Life in Space** is a 2D survival game where players control an astronaut aboard a spaceship. The objective is to survive as long as possible by maintaining oxygen, power, and health levels while repairing system failures and collecting resources. The game offers increasing difficulty over time, testing the player's ability to adapt and strategize.

---

## Features

- **Astronaut Movement**: Control the astronaut using arrow keys.
- **Resource Management**: Collect oxygen tanks, power kits, and food to maintain vital levels.
- **System Repairs**: Gather tools and repair system failures to avoid penalties.
- **Dynamic Difficulty**: The game becomes progressively challenging over time.
- **Game Over Conditions**: The game ends if oxygen, power, or health depletes completely.
- **Instructions and Legends**: Integrated "How to Play" and "Score Instructions" screens for better gameplay understanding.

---

## Controls

| Key  | Action                                |
|------|---------------------------------------|
| `↑`  | Move astronaut up                     |
| `↓`  | Move astronaut down                   |
| `←`  | Move astronaut left                   |
| `→`  | Move astronaut right                  |
| `H`  | View the "How to Play" screen         |
| `S`  | View the "Score Instructions" screen  |
| `B`  | Return to the main game               |
| `R`  | Restart the game after a Game Over    |

---

## Game Mechanics

### Vital Parameters
- **Oxygen Level**: Depletes over time and is replenished by collecting oxygen tanks.
- **Power Level**: Depletes over time and is replenished by collecting power kits.
- **Health Factor**: Affected by low oxygen, power, or weight levels.

### Items and Scoring

| Item            | Effect                                  | Score  |
|------------------|----------------------------------------|--------|
| Food            | Increases weight and health            | +100   |
| Oxygen Tank     | Increases oxygen level                 | +200   |
| Power Kit       | Increases power level                  | +150   |
| Repair System   | Fixes failures, restores oxygen/power  | +500   |
| Failure Penalty | Depletes oxygen, power, and score      | -5/sec |

### System Failures
- Randomly occur during the game.
- Must be repaired by collecting all tools and interacting with the failure location.
- Failure to repair in time results in faster depletion of resources and score penalties.

### Difficulty Scaling
- **Oxygen and Power Depletion**: Rates increase over time.
- **System Failures**: Occur more frequently.
- **Item Respawn**: Shorter respawn times for resources.

---

## Screens

### Main Game
- Navigate the astronaut, collect resources, and repair failures.

### How to Play (`H` Key)
- Displays instructions on movement, item collection, and survival tips.

### Score Instructions (`S` Key)
- Explains the scoring system for collecting items and repairing systems.

---

## How to Run the Game

1. **Prerequisites**:
   - Python 3.x
   - Pygame library (`pip install pygame`)

2. **Ensure Correct Asset Paths**:
   - Check and edit the paths in the source code (`life_in_space.py`) to correctly point to the `assets/` folder.  
     Example:
     ```python
     astronaut_image = pygame.image.load("assets/images/astronaut.png")
     ```

3. **Run the Game**:
   ```bash
   python life_in_space.py
   ```

4. **Controls**:
   Use the keys specified in the **Controls** section to play the game.

---

## Future Enhancements

- Add more resource types and challenges.
- Implement multiplayer functionality.
- Introduce different spaceship environments.
- Add achievements and leaderboard functionality.

---

## Author
Parth Lathiya

---

Enjoy surviving the challenges of **Life in Space**!
