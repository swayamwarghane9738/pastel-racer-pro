"""
Typing Racer Game - Main Game Logic
Handles game states, main loop, and coordination between components.
"""

import pygame
import sys
import time
from enum import Enum
from typing import Optional

from ui import UI
from words import WordManager  
from car import Car
from particles import ParticleSystem
from audio import AudioManager
from leaderboard import LeaderboardManager
from settings import SettingsManager

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing" 
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SETTINGS = "settings"
    LEADERBOARD = "leaderboard"
    TUTORIAL = "tutorial"

class TypingRacerGame:
    """Main game class that manages all game states and components."""
    
    def __init__(self):
        """Initialize the game with default settings."""
        # Display settings
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60
        
        # Initialize pygame display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("🏁 Typing Racer - Cute Cars & Fast Typing!")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.MENU
        self.running = True
        
        # Initialize managers
        self.settings = SettingsManager()
        self.leaderboard = LeaderboardManager()
        self.audio = AudioManager(self.settings)
        
        # Initialize game components
        self.ui = UI(self.screen, self.settings, self.audio)
        self.word_manager = WordManager(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.settings)
        self.car = Car(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.particles = ParticleSystem()
        
        # Game state variables
        self.current_word = ""
        self.typed_text = ""
        self.wpm = 0.0
        self.accuracy = 100.0
        self.score = 0
        self.combo = 0
        self.start_time = 0
        self.game_time_limit = 60  # seconds
        self.chars_typed = 0
        self.chars_correct = 0
        self.words_completed = 0
        
        # Difficulty settings
        self.difficulty = "normal"  # easy, normal, hard, endless
        
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Handle pygame events based on current game state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state in [GameState.PAUSED, GameState.SETTINGS, 
                                      GameState.LEADERBOARD, GameState.TUTORIAL]:
                        self.state = GameState.MENU
                        
                elif self.state == GameState.MENU:
                    self.handle_menu_input(event)
                elif self.state == GameState.PLAYING:
                    self.handle_game_input(event)
                elif self.state == GameState.PAUSED:
                    self.handle_pause_input(event)
                elif self.state == GameState.GAME_OVER:
                    self.handle_game_over_input(event)
                elif self.state == GameState.SETTINGS:
                    self.handle_settings_input(event)
                elif self.state == GameState.LEADERBOARD:
                    self.handle_leaderboard_input(event)
                elif self.state == GameState.TUTORIAL:
                    self.handle_tutorial_input(event)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state != GameState.PLAYING:
                    self.handle_mouse_input(event)
    
    def handle_menu_input(self, event):
        """Handle input in the main menu."""
        key_map = {
            pygame.K_1: self.start_game,
            pygame.K_p: self.start_game,  # P for Play
            pygame.K_2: lambda: setattr(self, 'state', GameState.SETTINGS),
            pygame.K_s: lambda: setattr(self, 'state', GameState.SETTINGS),  # S for Settings  
            pygame.K_3: lambda: setattr(self, 'state', GameState.LEADERBOARD),
            pygame.K_l: lambda: setattr(self, 'state', GameState.LEADERBOARD),  # L for Leaderboard
            pygame.K_4: lambda: setattr(self, 'state', GameState.TUTORIAL),
            pygame.K_t: lambda: setattr(self, 'state', GameState.TUTORIAL),  # T for Tutorial
            pygame.K_5: lambda: setattr(self, 'running', False),
            pygame.K_q: lambda: setattr(self, 'running', False),  # Q for Quit
        }
        
        action = key_map.get(event.key)
        if action:
            action()
            self.audio.play_sound('menu_select')
    
    def handle_game_input(self, event):
        """Handle input during gameplay."""
        if event.key == pygame.K_BACKSPACE:
            if self.typed_text:
                self.typed_text = self.typed_text[:-1]
                self.audio.play_sound('backspace')
        
        elif event.unicode.isprintable() and event.unicode != ' ':
            char = event.unicode.lower()
            target_char = self.current_word[len(self.typed_text):len(self.typed_text)+1] if len(self.typed_text) < len(self.current_word) else ''
            
            self.chars_typed += 1
            
            if char == target_char.lower():
                self.typed_text += char
                self.chars_correct += 1
                self.audio.play_sound('correct')
                
                # Move car forward
                progress = len(self.typed_text) / len(self.current_word)
                self.car.move_by_progress(progress * 0.02)  # 2% of track per character
                
                # Check if word completed
                if len(self.typed_text) == len(self.current_word):
                    self.complete_word()
                    
            else:
                self.audio.play_sound('error')
                # Apply penalty (small slowdown)
                self.car.apply_penalty()
    
    def handle_pause_input(self, event):
        """Handle input when game is paused."""
        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
            self.state = GameState.PLAYING
            self.audio.play_sound('menu_select')
    
    def handle_game_over_input(self, event):
        """Handle input on game over screen."""
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            name = self.ui.get_player_name_input()
            if name:
                self.leaderboard.add_score(name, self.score, self.wpm, self.accuracy)
            self.state = GameState.MENU
            self.audio.play_sound('menu_select')
    
    def handle_settings_input(self, event):
        """Handle input in settings menu.""" 
        # Settings navigation handled by UI component
        pass
    
    def handle_leaderboard_input(self, event):
        """Handle input in leaderboard screen."""
        if event.key == pygame.K_c:
            self.leaderboard.clear_scores()
            self.audio.play_sound('menu_select')
    
    def handle_tutorial_input(self, event):
        """Handle input in tutorial screen."""
        pass  # Tutorial navigation handled by UI
    
    def handle_mouse_input(self, event):
        """Handle mouse input for UI interactions."""
        # Mouse handling delegated to UI component
        pass
    
    def start_game(self, difficulty="normal"):
        """Start a new game with specified difficulty."""
        self.difficulty = difficulty
        self.state = GameState.PLAYING
        self.reset_game_stats()
        
        # Set difficulty parameters
        if difficulty == "easy":
            self.game_time_limit = 45
            self.word_manager.set_difficulty(0.8, 4, 120)  # slower, shorter words, more time
        elif difficulty == "normal":
            self.game_time_limit = 60  
            self.word_manager.set_difficulty(1.0, 6, 100)  # normal settings
        elif difficulty == "hard":
            self.game_time_limit = 75
            self.word_manager.set_difficulty(1.5, 8, 80)  # faster, longer words, less time
        elif difficulty == "endless":
            self.game_time_limit = 999999  # Effectively infinite
            self.word_manager.set_difficulty(1.0, 6, 100)
            
        self.start_time = time.time()
        self.spawn_new_word()
        
    def reset_game_stats(self):
        """Reset all game statistics for a new game."""
        self.current_word = ""
        self.typed_text = ""
        self.wpm = 0.0
        self.accuracy = 100.0
        self.score = 0
        self.combo = 0
        self.chars_typed = 0
        self.chars_correct = 0
        self.words_completed = 0
        self.car.reset()
        self.word_manager.clear_words()
        self.particles.clear()
        
    def spawn_new_word(self):
        """Spawn a new word for the player to type."""
        self.current_word = self.word_manager.get_next_word()
        self.typed_text = ""
        
    def complete_word(self):
        """Handle word completion with scoring and effects."""
        self.words_completed += 1
        self.combo += 1
        
        # Calculate score bonus
        word_length = len(self.current_word)
        base_score = word_length * 10
        combo_bonus = min(self.combo * 5, 100)  # Max 100 bonus
        total_bonus = base_score + combo_bonus
        self.score += total_bonus
        
        # Give car speed boost
        self.car.apply_boost()
        
        # Add particles at car position
        car_pos = self.car.get_position()
        self.particles.add_word_completion_effect(car_pos[0], car_pos[1])
        
        # Play completion sound
        self.audio.play_sound('word_complete')
        
        # Check win condition
        if self.car.has_finished():
            self.win_game()
        else:
            self.spawn_new_word()
    
    def win_game(self):
        """Handle game win with celebration effects."""
        self.state = GameState.GAME_OVER
        
        # Add celebration particles
        for _ in range(20):
            x = pygame.mouse.get_pos()[0] if pygame.mouse.get_pos()[0] else self.SCREEN_WIDTH // 2
            y = pygame.mouse.get_pos()[1] if pygame.mouse.get_pos()[1] else self.SCREEN_HEIGHT // 2
            self.particles.add_celebration_effect(x, y)
            
        self.audio.play_sound('game_win')
    
    def lose_game(self):
        """Handle game loss."""
        self.state = GameState.GAME_OVER
        self.combo = 0  # Reset combo on loss
    
    def update(self, dt):
        """Update all game components."""
        if self.state == GameState.PLAYING:
            # Update game timer
            elapsed_time = time.time() - self.start_time
            remaining_time = max(0, self.game_time_limit - elapsed_time)
            
            # Check time limit (except for endless mode)
            if remaining_time <= 0 and self.difficulty != "endless":
                if not self.car.has_finished():
                    self.lose_game()
                    
            # Update statistics
            if elapsed_time > 0:
                # Calculate WPM (standard: 5 characters = 1 word)
                self.wpm = (self.chars_correct / 5) / (elapsed_time / 60)
                
                # Calculate accuracy
                if self.chars_typed > 0:
                    self.accuracy = (self.chars_correct / self.chars_typed) * 100
            
            # Update word manager
            self.word_manager.update(dt)
            
            # Update car
            self.car.update(dt)
            
            # Check if current word has expired (moved off screen)
            if self.word_manager.current_word_expired():
                # Apply penalty for missing word
                self.combo = 0
                self.car.apply_penalty()
                self.spawn_new_word()
        
        # Update particles in all states
        self.particles.update(dt)
        
        # Update UI
        self.ui.update(dt)
    
    def draw(self):
        """Render the current game state."""
        # Clear screen with pastel background
        self.screen.fill((253, 221, 210))  # Warm peach background
        
        if self.state == GameState.MENU:
            self.ui.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_game()  # Draw game in background
            self.ui.draw_pause_overlay()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()  # Draw final state
            self.ui.draw_game_over(self.score, self.wpm, self.accuracy)
        elif self.state == GameState.SETTINGS:
            self.ui.draw_settings()
        elif self.state == GameState.LEADERBOARD:
            self.ui.draw_leaderboard(self.leaderboard.get_scores())
        elif self.state == GameState.TUTORIAL:
            self.ui.draw_tutorial()
            
        pygame.display.flip()
    
    def draw_game(self):
        """Draw the main gameplay screen."""
        # Draw race track
        track_y = self.SCREEN_HEIGHT - 200
        track_color = (216, 226, 220)  # Light mint
        pygame.draw.rect(self.screen, track_color, 
                        (0, track_y, self.SCREEN_WIDTH, 100))
        
        # Draw finish line
        finish_x = self.SCREEN_WIDTH - 100
        pygame.draw.rect(self.screen, (189, 224, 254), 
                        (finish_x, track_y, 20, 100))  # Light blue
        
        # Draw car
        self.car.draw(self.screen)
        
        # Draw current word being typed
        if self.current_word:
            self.ui.draw_typing_area(self.current_word, self.typed_text)
        
        # Draw HUD
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        remaining_time = max(0, self.game_time_limit - elapsed_time)
        
        self.ui.draw_hud(self.wpm, self.accuracy, self.score, 
                        remaining_time, self.car.get_progress())
        
        # Draw particles
        self.particles.draw(self.screen)

    def get_game_state_data(self):
        """Get current game state for UI rendering."""
        return {
            'wpm': self.wpm,
            'accuracy': self.accuracy,
            'score': self.score,
            'combo': self.combo,
            'time_remaining': max(0, self.game_time_limit - (time.time() - self.start_time)) if self.start_time else 0,
            'progress': self.car.get_progress(),
            'current_word': self.current_word,
            'typed_text': self.typed_text
        }