# Galactic Connect 4

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

*A space-themed Connect 4 game featuring an intelligent AI opponent powered by the Minimax algorithm with Alpha-Beta pruning.*

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [AI Algorithm](#ai-algorithm) • [Configuration](#configuration)

</div>

---

## Overview

Galactic Connect 4 is a classic two-player connection game where players take turns dropping pieces into a vertical grid. The first player to connect four pieces horizontally, vertically, or diagonally wins. Set in a space-themed environment, choose between the dark forces (X) or the light (O) and battle for galactic supremacy against a challenging AI opponent.

![Screenshot 1](https://github.com/Alexsandr52/tic-tac-toe/assets/43495209/70a12777-77aa-479e-a24e-a58c4e24d8ab)
![Screenshot 2](https://github.com/Alexsandr52/tic-tac-toe/assets/43495209/cde9d25a-8e41-419c-ba85-718d1bf5ab5b)
![Screenshot 3](https://github.com/Alexsandr52/tic-tac-toe/assets/43495209/c43cf848-90f7-47a5-bfa0-5a56526da0de)

---

## Features

- **Intelligent AI Opponent**: Powered by the Minimax algorithm with Alpha-Beta pruning for optimal decision-making
- **Space-Themed UI**: Beautiful galactic interface with animated stars and atmospheric design
- **Customizable Difficulty**: Adjust AI depth to suit your skill level
- **Symbol Selection**: Choose to play as X (dark forces) or O (light side)
- **Smooth Gameplay**: 30 FPS rendering with responsive controls
- **Modular Architecture**: Clean separation of game logic, UI, and configuration

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Alexsandr52/tic-tac-toe.git
   cd tic-tac-toe
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

### Docker Installation

1. **Build the Docker image**
   ```bash
   docker build -t galactic-connect4 .
   ```

2. **Run with X11 forwarding (Linux)**
   ```bash
   xhost +local:docker
   docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix galactic-connect4
   ```

---

## Usage

1. **Launch the game** by running `python main.py`

2. **Select your symbol** - Choose between:
   - **X** (Dark Forces) - Play first with red X symbols
   - **O** (Light Side) - Play second with green O symbols

3. **Make your move** - Click on any column to drop your piece

4. **Win the game** - Connect 4 pieces in any direction (horizontal, vertical, or diagonal)

### Controls

| Action | Input |
|--------|-------|
| Drop Piece | Left Mouse Click |
| Select Symbol | Click on button |
| Navigate Menu | Click on buttons |

---

## AI Algorithm

### Minimax with Alpha-Beta Pruning

The AI opponent uses the **Minimax algorithm** with **Alpha-Beta pruning** to determine the optimal move. This algorithm:

- Explores possible game states up to a specified depth
- Maximizes the AI's score while minimizing the player's score
- Uses Alpha-Beta pruning to eliminate unnecessary branches, improving performance
- Evaluates board positions based on strategic factors:
  - Center column preference (strategic advantage)
  - Potential winning combinations
  - Opponent threat detection

### Difficulty Levels

The AI's strength is determined by the search depth (`DEPTH` in `config.py`):

| Depth | Difficulty | Performance |
|-------|------------|-------------|
| 3 | Easy | Instant moves |
| 4 | Medium | Very fast |
| 5 | Hard | Fast (recommended) |
| 6 | Expert | Moderate |
| 7+ | Master | Slower but near-perfect |

> **Note**: At depths 6-7, the AI plays at a near-perfect level, often resulting in draws against optimal play.

### Board Evaluation

The AI evaluates positions using the following scoring system:

- 4 in a row: +100 points (win imminent)
- 3 in a row with 1 empty: +5 points
- 2 in a row with 2 empty: +2 points
- Opponent 3 in a row with 1 empty: -4 points (threat blocking)

---

## Configuration

Edit `config.py` to customize game settings:

```python
# Board Dimensions
COLUMNS = 7
ROWS = 6

# Window Settings
WIDTH = 700
HEIGHT = 600

# AI Difficulty
DEPTH = 5  # Range: 3-7 recommended

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
# ... and more
```

---

## Project Structure

```
tic-tac-toe/
├── main.py      # Entry point and game loop
├── game.py      # Game logic and AI algorithm
├── front.py     # UI components and rendering
├── config.py    # Configuration constants
├── requirements.txt
├── Dockerfile
└── README.md
```

### Module Descriptions

- **main.py**: GameApp class managing the application lifecycle
- **game.py**: Connect4 class with game logic and Minimax AI
- **front.py**: UI and Button classes for rendering
- **config.py**: All configurable constants

---

## Technical Details

- **Language**: Python 3.8+
- **Graphics**: Pygame 2.0+
- **Math**: NumPy for board operations
- **Algorithm**: Minimax with Alpha-Beta pruning
- **Frame Rate**: 30 FPS

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## Acknowledgments

- Inspired by the classic Connect 4 game
- AI algorithm based on standard game theory principles
- Space theme inspired by Star Wars universe

---

## Author

**Alexsandr** - [GitHub](https://github.com/Alexsandr52)

---

<div align="center">

**May the Force be with you!** 🚀

</div>
