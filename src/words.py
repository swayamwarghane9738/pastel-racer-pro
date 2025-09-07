"""
Typing Racer Game - Word Management System
Handles word generation, movement, and difficulty scaling.
"""

import random
import pygame
from typing import List, Tuple, Optional

class MovingWord:
    """A word that moves across the screen for the player to type."""
    
    def __init__(self, text: str, start_pos: Tuple[int, int], 
                 end_pos: Tuple[int, int], speed: float):
        """Initialize a moving word with start/end positions and speed."""
        self.text = text
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.current_pos = list(start_pos)  # Current position [x, y]
        self.speed = speed  # pixels per second
        
        # Calculate movement vector
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        if distance > 0:
            self.velocity = [dx / distance * speed, dy / distance * speed]
        else:
            self.velocity = [0, 0]
            
        self.active = True
        
    def update(self, dt: float) -> bool:
        """Update word position. Returns True if word is still active."""
        if not self.active:
            return False
            
        # Move towards target
        self.current_pos[0] += self.velocity[0] * dt
        self.current_pos[1] += self.velocity[1] * dt
        
        # Check if reached destination
        dx = self.end_pos[0] - self.current_pos[0]
        dy = self.end_pos[1] - self.current_pos[1]
        distance_remaining = (dx ** 2 + dy ** 2) ** 0.5
        
        if distance_remaining < 10:  # Close enough to destination
            self.active = False
            return False
            
        return True
    
    def get_position(self) -> Tuple[int, int]:
        """Get current position as tuple."""
        return (int(self.current_pos[0]), int(self.current_pos[1]))
    
    def is_expired(self) -> bool:
        """Check if word has expired (reached destination)."""
        return not self.active

class WordManager:
    """Manages word generation, movement, and difficulty progression."""
    
    def __init__(self, screen_width: int, screen_height: int, settings):
        """Initialize word manager with screen dimensions and settings."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.settings = settings
        
        # Word lists by difficulty
        self.easy_words = [
            "cat", "dog", "sun", "run", "fun", "car", "big", "red", "hot", "cold",
            "yes", "no", "go", "up", "down", "happy", "fast", "slow", "good", "bad",
            "help", "jump", "play", "read", "sing", "walk", "talk", "look", "find", "make"
        ]
        
        self.normal_words = [
            "house", "water", "computer", "keyboard", "mouse", "typing", "racing", "speed",
            "challenge", "victory", "practice", "improve", "accuracy", "champion", "winner",
            "puzzle", "adventure", "journey", "explore", "discover", "create", "design",
            "develop", "progress", "achieve", "succeed", "complete", "master", "expert"
        ]
        
        self.hard_words = [
            "extraordinary", "magnificent", "programming", "development", "architecture",
            "infrastructure", "optimization", "performance", "complexity", "algorithm", 
            "implementation", "visualization", "transformation", "revolutionary", 
            "technological", "sophisticated", "comprehensive", "extraordinary",
            "professional", "responsibility", "concentration", "determination",
            "perseverance", "accomplishment", "achievement", "excellence"
        ]
        
        # Current settings
        self.word_speed = 100  # pixels per second
        self.max_word_length = 6
        self.spawn_delay = 100  # frames between spawns
        
        # Movement patterns
        self.movement_patterns = [
            "top_right_to_bottom_left",
            "left_to_right", 
            "top_to_bottom",
            "random_corners"
        ]
        self.current_pattern = "top_right_to_bottom_left"
        
        # State
        self.active_words = []
        self.current_word_index = 0
        self.spawn_timer = 0
        
    def set_difficulty(self, speed_multiplier: float, max_length: int, spawn_rate: int):
        """Set difficulty parameters."""
        self.word_speed = int(100 * speed_multiplier)
        self.max_word_length = max_length
        self.spawn_delay = spawn_rate
        
    def get_word_list(self) -> List[str]:
        """Get appropriate word list based on difficulty."""
        # Mix word lists based on max length
        if self.max_word_length <= 4:
            return self.easy_words
        elif self.max_word_length <= 7:
            return self.easy_words + self.normal_words
        else:
            return self.easy_words + self.normal_words + self.hard_words
            
    def get_next_word(self) -> str:
        """Get the next word for the player to type."""
        word_list = self.get_word_list()
        
        # Filter by max length
        valid_words = [w for w in word_list if len(w) <= self.max_word_length]
        
        if not valid_words:
            valid_words = self.easy_words
            
        return random.choice(valid_words)
    
    def get_spawn_position(self, pattern: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Get start and end positions based on movement pattern."""
        margin = 50
        
        if pattern == "top_right_to_bottom_left":
            start = (self.screen_width - margin, margin)
            end = (margin, self.screen_height - margin)
            
        elif pattern == "left_to_right":
            y = self.screen_height // 2 + random.randint(-100, 100)
            start = (margin, y)
            end = (self.screen_width - margin, y)
            
        elif pattern == "top_to_bottom":
            x = self.screen_width // 2 + random.randint(-200, 200)
            start = (x, margin)
            end = (x, self.screen_height - margin - 150)  # Above track area
            
        elif pattern == "random_corners":
            corners = [
                (margin, margin),                                    # top-left
                (self.screen_width - margin, margin),                # top-right
                (margin, self.screen_height - margin),              # bottom-left  
                (self.screen_width - margin, self.screen_height - margin)  # bottom-right
            ]
            start = random.choice(corners)
            end = random.choice([c for c in corners if c != start])
            
        else:
            # Default to top-right to bottom-left
            start = (self.screen_width - margin, margin)
            end = (margin, self.screen_height - margin)
            
        return start, end
    
    def spawn_word(self, text: str):
        """Spawn a new moving word."""
        start_pos, end_pos = self.get_spawn_position(self.current_pattern)
        
        word = MovingWord(text, start_pos, end_pos, self.word_speed)
        self.active_words.append(word)
        
    def update(self, dt: float):
        """Update all active words."""
        # Update existing words
        self.active_words = [word for word in self.active_words if word.update(dt)]
        
        # Spawn timer
        self.spawn_timer += 1
        
    def clear_words(self):
        """Clear all active words."""
        self.active_words.clear()
        self.current_word_index = 0
        self.spawn_timer = 0
        
    def current_word_expired(self) -> bool:
        """Check if the current word has expired."""
        # For this simple implementation, we don't track moving words separately
        # The main game manages the current typing word
        return False
        
    def draw_moving_words(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw all moving words on screen."""
        for word in self.active_words:
            if word.active:
                pos = word.get_position()
                
                # Create text surface with background
                text_surface = font.render(word.text, True, (60, 60, 60))
                text_rect = text_surface.get_rect(center=pos)
                
                # Background rectangle
                bg_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=8)
                pygame.draw.rect(screen, (200, 200, 200), bg_rect, 2, border_radius=8)
                
                # Draw text
                screen.blit(text_surface, text_rect)
                
    def get_movement_pattern_name(self) -> str:
        """Get human-readable name of current movement pattern.""" 
        pattern_names = {
            "top_right_to_bottom_left": "Corner to Corner",
            "left_to_right": "Left to Right",
            "top_to_bottom": "Top to Bottom", 
            "random_corners": "Random Corners"
        }
        return pattern_names.get(self.current_pattern, "Unknown")
        
    def cycle_movement_pattern(self):
        """Cycle to next movement pattern."""
        current_index = self.movement_patterns.index(self.current_pattern)
        next_index = (current_index + 1) % len(self.movement_patterns)
        self.current_pattern = self.movement_patterns[next_index]