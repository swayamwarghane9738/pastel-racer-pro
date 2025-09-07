#!/usr/bin/env python3
"""
Typing Racer Game - Main Entry Point
A cute and loveable typing game with chibi cars and pastel colors.
"""

import sys
import os
import pygame

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game import TypingRacerGame
from assets import AssetManager

def main():
    """Initialize pygame and start the game."""
    try:
        # Initialize pygame
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.init()
        
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize asset manager (creates embedded assets)
        asset_manager = AssetManager()
        asset_manager.initialize()
        
        # Create and run the game
        game = TypingRacerGame()
        game.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()