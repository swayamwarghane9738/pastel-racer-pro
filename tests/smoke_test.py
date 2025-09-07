#!/usr/bin/env python3
"""
Typing Racer Game - Smoke Test
Automated test to verify the game launches without errors.
"""

import sys
import os
import pygame
import time
import threading
from unittest.mock import patch

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

def test_imports():
    """Test that all modules can be imported without errors."""
    try:
        import game
        import ui 
        import words
        import car
        import particles
        import audio
        import leaderboard
        import settings
        import assets
        print("✓ All modules import successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_pygame_initialization():
    """Test pygame initialization."""
    try:
        # Set SDL to use dummy video driver for headless testing
        os.environ['SDL_VIDEODRIVER'] = 'dummy' 
        
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.init()
        
        # Create a minimal surface
        screen = pygame.display.set_mode((100, 100))
        
        print("✓ Pygame initializes successfully")
        return True
    except Exception as e:
        print(f"✗ Pygame initialization error: {e}")
        return False

def test_asset_creation():
    """Test asset manager initialization."""
    try:
        from assets import AssetManager
        
        asset_manager = AssetManager()
        asset_manager.initialize()
        
        # Test color palette
        colors = asset_manager.get_color_palette()
        assert 'bg' in colors
        assert 'text' in colors
        
        print("✓ Asset manager works correctly")
        return True
    except Exception as e:
        print(f"✗ Asset manager error: {e}")
        return False

def test_settings_manager():
    """Test settings persistence."""
    try:
        from settings import SettingsManager
        
        settings = SettingsManager()
        
        # Test getting/setting values
        original_volume = settings.get_master_volume()
        settings.set_master_volume(0.5)
        assert settings.get_master_volume() == 0.5
        
        # Test saving/loading
        settings.save_settings()
        
        print("✓ Settings manager works correctly") 
        return True
    except Exception as e:
        print(f"✗ Settings manager error: {e}")
        return False

def test_leaderboard_manager():
    """Test leaderboard functionality.""" 
    try:
        from leaderboard import LeaderboardManager
        
        leaderboard = LeaderboardManager()
        
        # Test adding a score
        leaderboard.add_score("TestPlayer", 1000, 45.5, 98.5, "normal")
        
        # Test getting scores
        scores = leaderboard.get_scores(limit=1)
        assert len(scores) >= 1
        
        # Clean up test data
        leaderboard.clear_scores()
        
        print("✓ Leaderboard manager works correctly")
        return True
    except Exception as e:
        print(f"✗ Leaderboard manager error: {e}")
        return False

def test_game_components():
    """Test individual game components."""
    try:
        from car import Car
        from words import WordManager
        from particles import ParticleSystem
        from audio import AudioManager
        from settings import SettingsManager
        
        # Test car
        car = Car(800, 600)
        car.update(0.016)  # One frame at 60 FPS
        assert car.get_progress() == 0.0
        
        # Test word manager
        settings = SettingsManager()
        word_manager = WordManager(800, 600, settings)
        word = word_manager.get_next_word()
        assert isinstance(word, str) and len(word) > 0
        
        # Test particles
        particles = ParticleSystem()
        particles.add_word_completion_effect(100, 100)
        particles.update(0.016)
        
        # Test audio (should not crash even without numpy)
        audio = AudioManager(settings)
        audio.play_sound('correct')  # Should not crash
        
        print("✓ All game components work correctly")
        return True
    except Exception as e:
        print(f"✗ Game components error: {e}")
        return False

def test_game_initialization():
    """Test that the main game class can be initialized."""
    try:
        from game import TypingRacerGame
        
        # Set headless mode
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        
        # Initialize pygame
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.init()
        
        # Create game instance
        game = TypingRacerGame()
        
        # Test basic functionality
        assert game.state.value == 'menu'
        assert game.running == True
        
        print("✓ Game initializes successfully")
        return True
    except Exception as e:
        print(f"✗ Game initialization error: {e}")
        return False

def test_headless_game_loop():
    """Test running a few frames of the game loop in headless mode."""
    try:
        from game import TypingRacerGame
        
        # Set headless mode
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        
        # Initialize pygame
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.init()
        
        # Create game
        game = TypingRacerGame()
        
        # Run a few update cycles
        for i in range(10):
            game.handle_events = lambda: None  # Mock event handling
            game.update(0.016)  # 60 FPS frame time
            
            # Don't actually draw to screen in test
            if hasattr(game, 'draw'):
                pass  # Skip drawing
                
        print("✓ Game loop runs without crashing")
        return True
    except Exception as e:
        print(f"✗ Game loop error: {e}")
        return False

def run_all_tests():
    """Run all smoke tests."""
    print("🧪 Running Typing Racer Smoke Tests...\n")
    
    tests = [
        test_imports,
        test_pygame_initialization, 
        test_asset_creation,
        test_settings_manager,
        test_leaderboard_manager,
        test_game_components,
        test_game_initialization,
        test_headless_game_loop
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            failed += 1
            
    print(f"\n📊 Test Results:")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Total:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! The game should run correctly.")
        return True
    else:
        print(f"\n❌ {failed} test(s) failed. There may be issues with the game.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    
    # Cleanup
    try:
        pygame.quit()
    except:
        pass
        
    sys.exit(0 if success else 1)