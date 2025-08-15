# 2D Space Shooter Game

A classic 2D space shooter game built with Python and Pygame. Control your spaceship, shoot down enemies, and survive as long as possible!

## Features

- **Player Control**: Move your spaceship left/right using arrow keys or WASD
- **Shooting**: Press spacebar to shoot bullets upward
- **Enemies**: Two types of enemies (aliens and meteors) spawn from the top
- **Collision Detection**: Realistic collision between bullets, enemies, and player
- **Scoring System**: Earn points for each enemy destroyed
- **Lives System**: Start with 3 lives, game over when all lives are lost
- **Visual Effects**: Animated starfield background and colorful graphics
- **Sound Effects**: Shooting and explosion sounds (programmatically generated)
- **Game Over Screen**: Display final score with restart option

## Screenshots

The game features:
- Cyan triangular spaceship with blue cockpit
- Red square aliens with white centers
- Gray triangular meteors
- Yellow bullet projectiles
- Animated white stars in the background
- Clean UI showing score and lives

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the game files**
   ```bash
   # If you have git:
   git clone <repository-url>
   cd 2d-space-shooter
   
   # Or simply download the files to a folder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install pygame directly:
   ```bash
   pip install pygame
   ```

3. **Run the game**
   ```bash
   python space_shooter.py
   ```

## How to Play

### Controls
- **Arrow Keys** or **WASD**: Move spaceship left/right
- **Spacebar**: Shoot bullets
- **R**: Restart game (when game over)
- **Close Window**: Quit game

### Gameplay
1. Control your spaceship at the bottom of the screen
2. Shoot down enemies (aliens and meteors) as they fall from the top
3. Avoid collisions with enemies - each collision costs 1 life
4. Destroy enemies to earn points (10 points per enemy)
5. Survive as long as possible and achieve the highest score!

### Game Elements
- **Player**: Cyan triangular spaceship with 3 lives
- **Bullets**: Yellow projectiles that travel upward
- **Aliens**: Red square enemies with white centers
- **Meteors**: Gray triangular enemies
- **Stars**: Animated background elements for visual appeal

## Code Structure

The game is organized into several classes:

- **`Player`**: Handles player movement, lives, and scoring
- **`Bullet`**: Manages bullet movement and collision detection
- **`Enemy`**: Controls enemy spawning, movement, and types
- **`Star`**: Creates animated background stars
- **`Game`**: Main game loop, collision detection, and rendering

## Customization

You can easily modify the game by adjusting the constants at the top of the file:

- `SCREEN_WIDTH` and `SCREEN_HEIGHT`: Change window size
- `PLAYER_SPEED`: Adjust player movement speed
- `BULLET_SPEED`: Change bullet velocity
- `ENEMY_SPEED`: Modify enemy movement speed
- `ENEMY_SPAWN_RATE`: Control how frequently enemies appear
- `FPS`: Adjust game frame rate

## Troubleshooting

### Common Issues

1. **"pygame module not found"**
   - Make sure you've installed pygame: `pip install pygame`

2. **Game runs slowly**
   - Lower the FPS value or reduce the number of background stars

3. **Sound not working**
   - The game creates sounds programmatically, so it should work on most systems
   - If you have issues, the game will continue without sound

4. **Window not responding**
   - Make sure you're running the latest version of Python and Pygame
   - Try closing other applications to free up system resources

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.6 or higher
- **Memory**: 100MB RAM minimum
- **Graphics**: Any graphics card that supports basic 2D rendering

## Contributing

Feel free to modify and improve the game! Some ideas for enhancements:
- Add power-ups and special weapons
- Implement different enemy types with unique behaviors
- Add boss battles
- Include high score tracking
- Create multiple difficulty levels
- Add particle effects for explosions

## License

This project is open source and available under the MIT License.

## Credits

Created as a Python/Pygame learning project. Built with clean, modular code that's easy to understand and modify.

---

**Enjoy the game!** 🚀👾
