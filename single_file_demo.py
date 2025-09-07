#!/usr/bin/env python3
"""
Typing Racer - Single File Demo
A complete, self-contained version of the typing racer game.
All features in one file for easy testing and distribution.
"""

import pygame
import sys
import random
import math
import time
import json
import os
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum

# Game constants
SCREEN_WIDTH = 1024  
SCREEN_HEIGHT = 768
FPS = 60

# Colors (pastel palette)
COLORS = {
    'bg': (253, 221, 210),       # Warm peach
    'bg_light': (248, 237, 235), # Light pink
    'accent': (216, 226, 220),   # Mint green
    'accent_blue': (189, 224, 254), # Light blue
    'text': (60, 60, 60),        # Dark gray
    'text_light': (120, 120, 120), # Medium gray
    'correct': (144, 238, 144),  # Light green
    'error': (255, 182, 193),    # Light pink (error)
    'white': (255, 255, 255),
    'shadow': (200, 200, 200),   # Light shadow
}

# Word lists
EASY_WORDS = [
    "cat", "dog", "sun", "run", "fun", "car", "big", "red", "hot", "cold",
    "yes", "no", "go", "up", "down", "happy", "fast", "slow", "good", "bad"
]

NORMAL_WORDS = [
    "house", "water", "computer", "keyboard", "mouse", "typing", "racing", "speed",
    "challenge", "victory", "practice", "improve", "accuracy", "champion", "winner"
]

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"

class SimpleCar:
    """Simplified chibi car for the demo."""
    
    def __init__(self):
        self.position = 0.0  # 0.0 to 1.0
        self.track_start_x = 50
        self.track_end_x = SCREEN_WIDTH - 150
        self.track_length = self.track_end_x - self.track_start_x
        self.y = SCREEN_HEIGHT - 150
        
    def get_screen_x(self):
        return self.track_start_x + (self.position * self.track_length)
        
    def move_forward(self, amount):
        self.position = min(1.0, self.position + amount)
        
    def has_finished(self):
        return self.position >= 1.0
        
    def reset(self):
        self.position = 0.0
        
    def draw(self, screen):
        x = int(self.get_screen_x())
        y = self.y
        
        # Car body (simple rounded rectangle)
        car_rect = pygame.Rect(x - 25, y - 15, 50, 30)
        pygame.draw.rect(screen, COLORS['accent_blue'], car_rect, border_radius=10)
        
        # Wheels
        pygame.draw.circle(screen, COLORS['text'], (x - 15, y + 10), 6)
        pygame.draw.circle(screen, COLORS['text'], (x + 15, y + 10), 6)
        
        # Eyes
        pygame.draw.circle(screen, COLORS['white'], (x - 8, y - 5), 3)
        pygame.draw.circle(screen, COLORS['white'], (x + 8, y - 5), 3)
        pygame.draw.circle(screen, COLORS['text'], (x - 8, y - 5), 1)
        pygame.draw.circle(screen, COLORS['text'], (x + 8, y - 5), 1)

class SimpleTypingGame:
    """Simplified typing racer game."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🏁 Typing Racer - Single File Demo")
        self.clock = pygame.time.Clock()
        
        # Fonts
        try:
            self.font_large = pygame.font.SysFont('Comic Sans MS', 48)
            self.font_medium = pygame.font.SysFont('Comic Sans MS', 32)
            self.font_small = pygame.font.SysFont('Comic Sans MS', 24)
        except:
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
            
        # Game state
        self.state = GameState.MENU
        self.running = True
        
        # Game objects
        self.car = SimpleCar()
        
        # Game variables
        self.current_word = ""
        self.typed_text = ""
        self.score = 0
        self.wpm = 0.0
        self.accuracy = 100.0
        self.start_time = 0
        self.chars_typed = 0
        self.chars_correct = 0
        self.game_time = 60  # seconds
        
        # High scores (simple in-memory storage for demo)
        self.high_scores = []
        
    def run(self):
        """Main game loop.""" 
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
        
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_q:
                        self.running = False
                        
                elif self.state == GameState.PLAYING:
                    self.handle_typing(event)
                    
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.MENU
                        
    def handle_typing(self, event):
        """Handle typing input during gameplay."""
        if event.key == pygame.K_BACKSPACE:
            if self.typed_text:
                self.typed_text = self.typed_text[:-1]
                
        elif event.unicode.isprintable():
            char = event.unicode.lower()
            target_char = ""
            
            if len(self.typed_text) < len(self.current_word):
                target_char = self.current_word[len(self.typed_text)].lower()
                
            self.chars_typed += 1
            
            if char == target_char:
                self.typed_text += char
                self.chars_correct += 1
                
                # Move car forward
                progress = len(self.typed_text) / len(self.current_word)
                self.car.move_forward(progress * 0.02)
                
                # Complete word
                if len(self.typed_text) == len(self.current_word):
                    self.complete_word()
                    
    def complete_word(self):
        """Handle word completion."""
        self.score += len(self.current_word) * 10
        self.car.move_forward(0.05)  # Bonus progress
        
        if self.car.has_finished():
            self.end_game()
        else:
            self.spawn_word()
            
    def spawn_word(self):
        """Spawn a new word to type."""
        word_list = EASY_WORDS + NORMAL_WORDS
        self.current_word = random.choice(word_list)
        self.typed_text = ""
        
    def start_game(self):
        """Start a new game."""
        self.state = GameState.PLAYING
        self.car.reset()
        self.score = 0
        self.wpm = 0.0
        self.accuracy = 100.0
        self.chars_typed = 0
        self.chars_correct = 0
        self.start_time = time.time()
        self.spawn_word()
        
    def end_game(self):
        """End the current game."""
        self.state = GameState.GAME_OVER
        
        # Add to high scores
        self.high_scores.append({
            'score': self.score,
            'wpm': self.wmp,
            'accuracy': self.accuracy
        })
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10
        
    def update(self):
        """Update game logic."""
        if self.state == GameState.PLAYING:
            # Calculate stats
            elapsed = time.time() - self.start_time
            
            # Check time limit
            if elapsed >= self.game_time:
                self.end_game()
                
            # Calculate WPM and accuracy
            if elapsed > 0:
                self.wpm = (self.chars_correct / 5) / (elapsed / 60)
                
            if self.chars_typed > 0:
                self.accuracy = (self.chars_correct / self.chars_typed) * 100
                
    def draw_rounded_rect(self, surface, color, rect, radius=15):
        """Draw a simple rounded rectangle."""
        # For demo simplicity, just draw regular rectangles
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def draw_text_centered(self, text, font, color, x, y):
        """Draw centered text."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        
    def draw(self):
        """Draw everything."""
        self.screen.fill(COLORS['bg'])
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
            
        pygame.display.flip()
        
    def draw_menu(self):
        """Draw main menu."""
        # Title
        self.draw_text_centered("🏁 TYPING RACER 🏁", self.font_large,
                               COLORS['text'], SCREEN_WIDTH // 2, 200)
        
        self.draw_text_centered("Single File Demo", self.font_medium,
                               COLORS['text_light'], SCREEN_WIDTH // 2, 260)
        
        # Instructions
        self.draw_text_centered("Press SPACE to start playing", self.font_small,
                               COLORS['text'], SCREEN_WIDTH // 2, 350)
        
        self.draw_text_centered("Press Q to quit", self.font_small,
                               COLORS['text_light'], SCREEN_WIDTH // 2, 390)
        
        # High scores
        if self.high_scores:
            self.draw_text_centered("High Scores:", self.font_small,
                                   COLORS['text'], SCREEN_WIDTH // 2, 480)
            
            for i, score in enumerate(self.high_scores[:5]):
                y = 520 + i * 30
                score_text = f"{i+1}. Score: {score['score']:,} - WPM: {score['wpm']:.1f}"
                self.draw_text_centered(score_text, pygame.font.Font(None, 20),
                                       COLORS['text_light'], SCREEN_WIDTH // 2, y)
                
    def draw_game(self):
        """Draw gameplay screen."""
        # Track
        track_y = SCREEN_HEIGHT - 200
        pygame.draw.rect(self.screen, COLORS['accent'], 
                        (0, track_y, SCREEN_WIDTH, 100))
        
        # Finish line
        finish_x = SCREEN_WIDTH - 100
        pygame.draw.rect(self.screen, COLORS['accent_blue'],
                        (finish_x, track_y, 20, 100))
        
        # Car
        self.car.draw(self.screen)
        
        # Current word
        if self.current_word:
            # Word panel
            panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 100, 400, 60)
            self.draw_rounded_rect(self.screen, COLORS['white'], panel_rect)
            
            # Typed portion (green)
            if self.typed_text:
                typed_surface = self.font_medium.render(self.typed_text, True, COLORS['correct'])
                word_width = self.font_medium.size(self.current_word)[0]
                typed_x = SCREEN_WIDTH // 2 - word_width // 2
                self.screen.blit(typed_surface, (typed_x, 115))
                
            # Remaining portion (gray)
            remaining = self.current_word[len(self.typed_text):]
            if remaining:
                remaining_surface = self.font_medium.render(remaining, True, COLORS['text_light'])
                typed_width = self.font_medium.size(self.typed_text)[0] if self.typed_text else 0
                word_width = self.font_medium.size(self.current_word)[0]
                remaining_x = SCREEN_WIDTH // 2 - word_width // 2 + typed_width
                self.screen.blit(remaining_surface, (remaining_x, 115))
                
        # HUD
        hud_rect = pygame.Rect(20, 20, 200, 100)
        self.draw_rounded_rect(self.screen, COLORS['white'], hud_rect)
        
        hud_text = [
            f"Score: {self.score}",
            f"WPM: {self.wpm:.1f}",
            f"Accuracy: {self.accuracy:.1f}%"
        ]
        
        for i, text in enumerate(hud_text):
            self.draw_text_centered(text, pygame.font.Font(None, 20),
                                   COLORS['text'], 120, 50 + i * 25)
                                   
        # Time remaining
        elapsed = time.time() - self.start_time
        remaining = max(0, self.game_time - elapsed)
        self.draw_text_centered(f"Time: {remaining:.0f}s", self.font_small,
                               COLORS['text'], SCREEN_WIDTH // 2, 50)
                               
        # Progress bar
        progress = self.car.position
        bar_width = 400
        bar_rect = pygame.Rect(SCREEN_WIDTH // 2 - bar_width // 2, 20, bar_width, 20)
        self.draw_rounded_rect(self.screen, COLORS['bg_light'], bar_rect, 10)
        
        if progress > 0:
            fill_rect = pygame.Rect(SCREEN_WIDTH // 2 - bar_width // 2, 20, 
                                  int(bar_width * progress), 20)
            self.draw_rounded_rect(self.screen, COLORS['accent_blue'], fill_rect, 10)
            
    def draw_game_over(self):
        """Draw game over screen."""
        # Background overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Results panel
        panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)
        self.draw_rounded_rect(self.screen, COLORS['white'], panel_rect)
        
        # Results
        self.draw_text_centered("RACE FINISHED!", self.font_large,
                               COLORS['text'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)
        
        results = [
            f"Final Score: {self.score:,}",
            f"WPM: {self.wpm:.1f}",
            f"Accuracy: {self.accuracy:.1f}%"
        ]
        
        for i, result in enumerate(results):
            self.draw_text_centered(result, self.font_small, COLORS['text'],
                                   SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20 + i * 40)
                                   
        self.draw_text_centered("Press SPACE to return to menu", pygame.font.Font(None, 20),
                               COLORS['text_light'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

def main():
    """Main entry point for the single file demo."""
    print("🏁 Starting Typing Racer Single File Demo...")
    
    try:
        game = SimpleTypingGame()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()