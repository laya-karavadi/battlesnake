# Battlesnake Python Project

A Python implementation of Battlesnake AI with two different strategies: an intelligent minimax-based snake and a simple random-move snake for testing and practice.

## 🐍 What is Battlesnake?

Battlesnake is a competitive programming game where you control a snake on a grid. Your snake must eat food to grow while avoiding walls, other snakes, and its own body. The last snake surviving wins!

## 📁 Project Structure

```
battlesnake-python/
├── main.py          # Intelligent snake with minimax algorithm
├── simple.py        # Simple random-move snake for testing
├── server.py        # Flask server to handle Battlesnake API
└── README.md        # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Flask (`pip install flask`)

### Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install flask
   ```

### Running Your Snake

#### Main Snake (Minimax Algorithm)
```bash
python main.py
```

#### Simple Snake (Random Moves)
```bash
python simple.py
```

Both will start a server at `http://localhost:8000` by default.

### Custom Port
```bash
python main.py --port 8001
python simple.py --port 8002
```

### Random Seed (Simple Snake Only)
For reproducible testing:
```bash
python simple.py --seed 12345
```

## 🤖 Snake Strategies

### Main Snake (`main.py`)
**Author:** lalaloo  
**Appearance:** Orange color, bendr head, sharp tail

**Features:**
- **Minimax Algorithm**: Uses game tree search with alpha-beta pruning (depth 3)
- **Evaluation Function**: Considers health, length advantage, food proximity, and move safety
- **Safety Checks**: Avoids walls, self-collision, and other snakes
- **Trap Avoidance**: Tries to avoid moves that lead to dead ends
- **Food Strategy**: Prioritizes food when health is below 50

**Algorithm Weights:**
- Health: 30%
- Length advantage: 40%
- Food proximity: 20%
- Move safety: 10%

### Simple Snake (`simple.py`)
**Author:** snake2  
**Appearance:** Dark blue color, default head and tail

**Features:**
- **Random Strategy**: Makes random safe moves
- **Basic Safety**: Avoids walls and snake collisions
- **Tail Following**: Can move to tail position when safe
- **Deterministic Testing**: Supports seeded random for consistent testing

## 🎮 Testing & Practice

### Local Testing
1. Start both snakes on different ports:
   ```bash
   python main.py --port 8000
   python simple.py --port 8001
   ```

2. Create a custom game on [play.battlesnake.com](https://play.battlesnake.com)

3. Add both snakes:
   - Snake 1: `http://your-domain:8000`
   - Snake 2: `http://your-domain:8001`

### Online Deployment
Deploy to platforms like:
- Heroku
- Railway
- Replit
- DigitalOcean

Make sure to set the `PORT` environment variable for production deployment.

## 🔧 Customization

### Changing Appearance
Edit the `info()` function in either file:
```python
return {
    "apiversion": "1",
    "author": "your-username",
    "color": "#FF0000",  # Red color
    "head": "default",   # See battlesnake.com for options
    "tail": "default",   # See battlesnake.com for options
}
```

### Adjusting Strategy
For the main snake, modify:
- **Minimax depth**: Change `depth=3` in the `move()` function
- **Evaluation weights**: Adjust the coefficients in `evaluation_function()`
- **Health threshold**: Change the `< 50` condition for food-seeking behavior

## 📊 Performance Notes

### Main Snake
- **Search Depth**: 3 moves ahead (adjustable)
- **Branching Factor**: Up to 4 moves per turn
- **Time Complexity**: O(4^depth)
- **Recommended for**: Competitive play

### Simple Snake
- **Decision Time**: Instant
- **Memory Usage**: Minimal
- **Recommended for**: Testing, practice opponent

## 🐛 Troubleshooting

### Common Issues

1. **"No safe moves detected"**: Snake will default to "down" - check collision detection logic
2. **Server won't start**: Port might be in use, try a different port
3. **Snake moves randomly**: Minimax might be failing, check evaluation function

### Debug Output
Both snakes print move decisions to console:
```
MOVE 1: right
MOVE 2: up
```

## 🎯 Strategy Tips

### For the Main Snake
- Increase minimax depth for stronger play (but slower response)
- Adjust evaluation function weights based on game analysis
- Consider opponent modeling for better predictions

### For Competitive Play
- Test against various opponent strategies
- Analyze game replays to identify weaknesses
- Consider additional factors like area control and snake positioning

## 📝 API Reference

This project implements the [Battlesnake API](https://docs.battlesnake.com/api):
- `GET /` - Snake information
- `POST /start` - Game start
- `POST /move` - Move decision
- `POST /end` - Game end

## 🤝 Contributing

Feel free to fork this project and experiment with:
- Different evaluation functions
- Alternative search algorithms (MCTS, neural networks)
- Advanced strategies (area control, opponent prediction)
- Performance optimizations

## 🏆 Competition Ready

The main snake is designed for competitive play with:
- Robust safety checks
- Strategic decision making
- Efficient search algorithms
- Fallback mechanisms

Good luck in your Battlesnake battles! 🐍
