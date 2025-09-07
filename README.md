# 🏁 Typing Racer Game

A cute and loveable typing game featuring chibi cars, pastel colors, and smooth animations. Race against time by typing words that move across the screen!

## Features

- 🚗 **Adorable chibi-style cars** drawn with simple shapes
- 🎨 **Pastel color palette** for a friendly, welcoming feel  
- ⚡ **Dynamic word movement** from corner to corner
- 🏆 **Local leaderboard** with persistent high scores
- 🎵 **Cute sound effects** for typing and completion
- ✨ **Particle confetti** when you win
- 📊 **Real-time stats**: WPM, accuracy, score tracking
- 🎮 **Multiple difficulty levels**: Easy, Normal, Hard, Endless
- ⚙️ **Customizable settings**: volume, colors, accessibility options
- 🎯 **Tutorial mode** to learn the game

## How to Run

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### Installation & Startup

**Windows:**
```cmd
pip install -r requirements.txt
python main.py
```

**macOS/Linux:**
```bash
pip install -r requirements.txt
python3 main.py
```

**Using convenience scripts:**
```bash
# Unix/macOS
./run.sh

# Windows  
run.bat
```

## How to Play

1. **Start**: Choose "Play" from the main menu
2. **Type**: Words will appear and move across the screen
3. **Race**: Type each word completely before it reaches the edge
4. **Progress**: Your car moves forward as you type correctly
5. **Win**: Reach the finish line before time runs out!

### Controls
- **Type letters** to match the current word
- **Backspace** to correct mistakes
- **Enter** to confirm word (optional)
- **ESC** to pause/return to menu

### Scoring
- **Accuracy**: Percentage of correctly typed characters
- **WPM**: Standard words per minute calculation  
- **Combo**: Consecutive correct words multiply your score
- **Bonus**: Completing words gives speed boosts

## Game Modes

- **Easy**: Slower words, shorter distance, common vocabulary
- **Normal**: Balanced gameplay for casual players
- **Hard**: Fast words, longer distance, challenging vocabulary  
- **Endless**: Keep typing until you can't keep up!

## Technical Details

### Architecture
The game uses a modular design with separate components:

- `game.py` - Main game loop and state management
- `ui.py` - User interface and menu systems  
- `car.py` - Car animation and movement logic
- `words.py` - Word generation and movement
- `particles.py` - Visual effects and animations
- `audio.py` - Sound effect management
- `assets.py` - Procedural graphics and embedded assets
- `leaderboard.py` - Score persistence  
- `settings.py` - Configuration management

### Asset Generation
All graphics and sounds are generated procedurally at runtime - no external files needed! The `assets.py` module creates:

- Chibi car graphics using pygame shapes
- Pastel UI elements with rounded corners
- Sound effects using mathematical waveforms
- Particle effects for celebrations

### Data Persistence
Game data is stored locally in JSON files:
- `data/settings.json` - User preferences
- `data/leaderboard.json` - High scores

## Building Executable

See `BUILD_NOTES.md` for instructions on creating standalone executables with PyInstaller.

## License

MIT License - see `LICENSE` file for details.

## Development

### Running Tests
```bash
python tests/smoke_test.py
```

### Code Structure
The codebase follows clean architecture principles with clear separation of concerns, comprehensive docstrings, and type hints where appropriate.

---

Made with 💖 for typing enthusiasts everywhere!