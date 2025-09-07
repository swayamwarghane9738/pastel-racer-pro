"""
Typing Racer Game - User Interface Components
Handles all UI rendering, menus, HUD, and visual elements.
"""

import pygame
import math
from typing import List, Tuple, Optional, Dict, Any

class UI:
    """User interface manager for all game screens and overlays."""
    
    def __init__(self, screen: pygame.Surface, settings, audio):
        """Initialize UI with screen reference and managers."""
        self.screen = screen
        self.settings = settings
        self.audio = audio
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Colors (pastel palette)
        self.colors = {
            'bg': (253, 221, 210),      # Warm peach
            'bg_light': (248, 237, 235), # Light pink  
            'accent': (216, 226, 220),   # Mint green
            'accent_blue': (189, 224, 254), # Light blue
            'text': (60, 60, 60),       # Dark gray
            'text_light': (120, 120, 120), # Medium gray
            'correct': (144, 238, 144),  # Light green
            'error': (255, 182, 193),    # Light pink (error)
            'white': (255, 255, 255),
            'shadow': (200, 200, 200),   # Light shadow
        }
        
        # Fonts
        try:
            self.font_large = pygame.font.SysFont('Comic Sans MS', 48)
            self.font_medium = pygame.font.SysFont('Comic Sans MS', 32) 
            self.font_small = pygame.font.SysFont('Comic Sans MS', 24)
            self.font_tiny = pygame.font.SysFont('Comic Sans MS', 18)
        except:
            # Fallback fonts
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
            self.font_tiny = pygame.font.Font(None, 18)
        
        # Animation state
        self.menu_bounce = 0
        self.hud_pulse = 0
        
    def update(self, dt: float):
        """Update UI animations."""
        self.menu_bounce += dt * 2
        self.hud_pulse += dt * 3
        
    def draw_rounded_rect(self, surface: pygame.Surface, color: Tuple[int, int, int], 
                         rect: pygame.Rect, radius: int = 15, shadow: bool = True):
        """Draw a rounded rectangle with optional shadow."""
        if shadow:
            shadow_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width, rect.height)
            self._draw_rounded_rect_shape(surface, self.colors['shadow'], shadow_rect, radius)
            
        self._draw_rounded_rect_shape(surface, color, rect, radius)
        
    def _draw_rounded_rect_shape(self, surface: pygame.Surface, color: Tuple[int, int, int],
                                rect: pygame.Rect, radius: int):
        """Helper to draw the actual rounded rectangle shape."""
        # Draw center rectangle
        center_rect = pygame.Rect(rect.x + radius, rect.y, 
                                 rect.width - 2 * radius, rect.height)
        pygame.draw.rect(surface, color, center_rect)
        
        # Draw side rectangles
        left_rect = pygame.Rect(rect.x, rect.y + radius,
                               radius, rect.height - 2 * radius) 
        right_rect = pygame.Rect(rect.x + rect.width - radius, rect.y + radius,
                                radius, rect.height - 2 * radius)
        pygame.draw.rect(surface, color, left_rect)
        pygame.draw.rect(surface, color, right_rect)
        
        # Draw corner circles
        pygame.draw.circle(surface, color, (rect.x + radius, rect.y + radius), radius)
        pygame.draw.circle(surface, color, (rect.x + rect.width - radius, rect.y + radius), radius)
        pygame.draw.circle(surface, color, (rect.x + radius, rect.y + rect.height - radius), radius)
        pygame.draw.circle(surface, color, (rect.x + rect.width - radius, rect.y + rect.height - radius), radius)
    
    def draw_text_centered(self, text: str, font: pygame.font.Font, color: Tuple[int, int, int],
                          x: int, y: int, shadow: bool = True) -> pygame.Rect:
        """Draw centered text with optional shadow."""
        if shadow:
            shadow_surf = font.render(text, True, self.colors['shadow'])
            shadow_rect = shadow_surf.get_rect(center=(x + 2, y + 2))
            self.screen.blit(shadow_surf, shadow_rect)
            
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.screen.blit(text_surf, text_rect)
        return text_rect
    
    def draw_menu(self):
        """Draw the main menu screen."""
        # Title with bounce animation
        title_y = 150 + math.sin(self.menu_bounce) * 10
        self.draw_text_centered("🏁 TYPING RACER 🏁", self.font_large, 
                               self.colors['text'], self.width // 2, title_y)
        
        # Subtitle
        self.draw_text_centered("Cute Cars & Fast Typing!", self.font_medium,
                               self.colors['text_light'], self.width // 2, title_y + 60)
        
        # Menu options
        menu_items = [
            ("1. Play Game", "P"),
            ("2. Settings", "S"), 
            ("3. Leaderboard", "L"),
            ("4. Tutorial", "T"),
            ("5. Quit", "Q")
        ]
        
        start_y = 320
        for i, (item, key) in enumerate(menu_items):
            y = start_y + i * 60
            
            # Button background
            button_rect = pygame.Rect(self.width // 2 - 150, y - 20, 300, 50)
            self.draw_rounded_rect(self.screen, self.colors['white'], button_rect)
            
            # Button text
            self.draw_text_centered(item, self.font_small, self.colors['text'], 
                                   self.width // 2, y)
            
            # Key hint
            self.draw_text_centered(f"({key})", self.font_tiny, self.colors['text_light'],
                                   self.width // 2 + 200, y)
    
    def draw_typing_area(self, current_word: str, typed_text: str):
        """Draw the word typing area with visual feedback."""
        if not current_word:
            return
            
        # Background panel
        panel_rect = pygame.Rect(self.width // 2 - 200, 100, 400, 80)
        self.draw_rounded_rect(self.screen, self.colors['white'], panel_rect)
        
        # Calculate text positions
        word_x = self.width // 2
        word_y = 140
        
        # Draw typed portion (green)
        if typed_text:
            typed_surface = self.font_medium.render(typed_text, True, self.colors['correct'])
            typed_width = typed_surface.get_width()
            typed_x = word_x - (self.font_medium.size(current_word)[0] // 2)
            self.screen.blit(typed_surface, (typed_x, word_y - 15))
            
        # Draw remaining portion (gray)
        remaining = current_word[len(typed_text):]
        if remaining:
            remaining_surface = self.font_medium.render(remaining, True, self.colors['text_light'])
            remaining_x = word_x - (self.font_medium.size(current_word)[0] // 2) + self.font_medium.size(typed_text)[0]
            self.screen.blit(remaining_surface, (remaining_x, word_y - 15))
            
        # Cursor blink
        if int(pygame.time.get_ticks() / 500) % 2:  # Blink every 500ms
            cursor_x = word_x - (self.font_medium.size(current_word)[0] // 2) + self.font_medium.size(typed_text)[0]
            pygame.draw.line(self.screen, self.colors['text'], 
                           (cursor_x, word_y - 10), (cursor_x, word_y + 20), 2)
    
    def draw_hud(self, wpm: float, accuracy: float, score: int, 
                time_remaining: float, progress: float):
        """Draw the heads-up display during gameplay."""
        # Stats panel (top-left)
        stats_rect = pygame.Rect(20, 20, 200, 120)
        self.draw_rounded_rect(self.screen, self.colors['white'], stats_rect)
        
        stats_text = [
            f"WPM: {wpm:.1f}",
            f"Accuracy: {accuracy:.1f}%", 
            f"Score: {score:,}",
            f"Time: {time_remaining:.0f}s"
        ]
        
        for i, text in enumerate(stats_text):
            self.draw_text_centered(text, self.font_tiny, self.colors['text'],
                                   120, 50 + i * 25, shadow=False)
        
        # Progress bar (top)
        bar_width = 400
        bar_height = 20
        bar_x = self.width // 2 - bar_width // 2
        bar_y = 30
        
        # Progress bar background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        self.draw_rounded_rect(self.screen, self.colors['bg_light'], bg_rect, 10, False)
        
        # Progress bar fill
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            fill_color = self.colors['accent_blue'] if progress < 0.8 else self.colors['correct']
            self.draw_rounded_rect(self.screen, fill_color, fill_rect, 10, False)
        
        # Progress percentage
        self.draw_text_centered(f"{progress * 100:.1f}%", self.font_tiny, 
                               self.colors['text'], self.width // 2, bar_y + 40, False)
    
    def draw_pause_overlay(self):
        """Draw pause screen overlay.""" 
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Pause panel
        panel_rect = pygame.Rect(self.width // 2 - 200, self.height // 2 - 100, 400, 200)
        self.draw_rounded_rect(self.screen, self.colors['white'], panel_rect)
        
        # Pause text
        self.draw_text_centered("PAUSED", self.font_large, self.colors['text'],
                               self.width // 2, self.height // 2 - 30)
        
        self.draw_text_centered("Press SPACE or ENTER to continue", self.font_small,
                               self.colors['text_light'], self.width // 2, self.height // 2 + 20)
        
        self.draw_text_centered("Press ESC to return to menu", self.font_tiny,
                               self.colors['text_light'], self.width // 2, self.height // 2 + 50)
    
    def draw_game_over(self, score: int, wpm: float, accuracy: float):
        """Draw game over screen with final stats."""
        # Overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Results panel
        panel_rect = pygame.Rect(self.width // 2 - 250, self.height // 2 - 150, 500, 300)
        self.draw_rounded_rect(self.screen, self.colors['white'], panel_rect)
        
        # Title
        self.draw_text_centered("RACE FINISHED!", self.font_large, self.colors['text'],
                               self.width // 2, self.height // 2 - 100)
        
        # Stats
        stats = [
            f"Final Score: {score:,}",
            f"Words Per Minute: {wpm:.1f}",
            f"Accuracy: {accuracy:.1f}%"
        ]
        
        for i, stat in enumerate(stats):
            self.draw_text_centered(stat, self.font_small, self.colors['text'],
                                   self.width // 2, self.height // 2 - 40 + i * 35)
        
        # Continue instruction  
        self.draw_text_centered("Press ENTER to save score and return to menu", 
                               self.font_tiny, self.colors['text_light'],
                               self.width // 2, self.height // 2 + 80)
    
    def draw_settings(self):
        """Draw settings screen."""
        self.draw_text_centered("SETTINGS", self.font_large, self.colors['text'],
                               self.width // 2, 100)
        
        # Settings options
        settings_items = [
            "Sound Volume",
            "Accessibility Mode", 
            "Font Size",
            "Difficulty"
        ]
        
        start_y = 200
        for i, item in enumerate(settings_items):
            y = start_y + i * 80
            
            # Setting label
            self.draw_text_centered(item, self.font_small, self.colors['text'],
                                   self.width // 2 - 100, y)
            
            # Setting value (placeholder)
            value = "Normal"  # This would come from settings manager
            self.draw_text_centered(value, self.font_small, self.colors['accent_blue'],
                                   self.width // 2 + 100, y)
        
        # Instructions
        self.draw_text_centered("Use arrow keys to navigate, ENTER to change", 
                               self.font_tiny, self.colors['text_light'],
                               self.width // 2, self.height - 100)
        
        self.draw_text_centered("Press ESC to return to menu", self.font_tiny,
                               self.colors['text_light'], self.width // 2, self.height - 60)
    
    def draw_leaderboard(self, scores: List[Dict[str, Any]]):
        """Draw leaderboard screen."""
        self.draw_text_centered("🏆 LEADERBOARD 🏆", self.font_large, self.colors['text'],
                               self.width // 2, 80)
        
        if not scores:
            self.draw_text_centered("No scores yet! Be the first to set a record!", 
                                   self.font_small, self.colors['text_light'],
                                   self.width // 2, self.height // 2)
        else:
            # Headers
            header_y = 150
            self.draw_text_centered("Rank", self.font_small, self.colors['text'], 150, header_y)
            self.draw_text_centered("Name", self.font_small, self.colors['text'], 300, header_y)  
            self.draw_text_centered("Score", self.font_small, self.colors['text'], 500, header_y)
            self.draw_text_centered("WPM", self.font_small, self.colors['text'], 650, header_y)
            self.draw_text_centered("Accuracy", self.font_small, self.colors['text'], 800, header_y)
            
            # Scores
            for i, score_data in enumerate(scores[:10]):  # Top 10
                y = 190 + i * 35
                rank_color = self.colors['accent_blue'] if i < 3 else self.colors['text']
                
                self.draw_text_centered(f"{i+1}.", self.font_tiny, rank_color, 150, y, False)
                self.draw_text_centered(score_data['name'], self.font_tiny, self.colors['text'], 300, y, False)
                self.draw_text_centered(f"{score_data['score']:,}", self.font_tiny, self.colors['text'], 500, y, False)
                self.draw_text_centered(f"{score_data['wpm']:.1f}", self.font_tiny, self.colors['text'], 650, y, False)
                self.draw_text_centered(f"{score_data['accuracy']:.1f}%", self.font_tiny, self.colors['text'], 800, y, False)
        
        # Instructions
        self.draw_text_centered("Press C to clear leaderboard", self.font_tiny,
                               self.colors['text_light'], self.width // 2, self.height - 100)
        self.draw_text_centered("Press ESC to return to menu", self.font_tiny,
                               self.colors['text_light'], self.width // 2, self.height - 60)
    
    def draw_tutorial(self):
        """Draw tutorial/help screen."""
        self.draw_text_centered("📚 HOW TO PLAY 📚", self.font_large, self.colors['text'],
                               self.width // 2, 80)
        
        instructions = [
            "🎯 OBJECTIVE: Type words before they disappear!",
            "",
            "🚗 Your cute car moves forward as you type correctly",
            "⚡ Complete words to get speed boosts", 
            "❌ Mistakes slow you down and break your combo",
            "🏁 Reach the finish line before time runs out!",
            "",
            "⌨️ CONTROLS:",
            "• Type letters to match the current word",
            "• BACKSPACE to correct mistakes",
            "• ESC to pause during games",
            "",
            "📊 SCORING:",
            "• Accuracy and speed determine your WPM",
            "• Longer words give more points",
            "• Consecutive correct words build combos!"
        ]
        
        start_y = 150
        for i, line in enumerate(instructions):
            y = start_y + i * 25
            font = self.font_small if line.startswith(('🎯', '⌨️', '📊')) else self.font_tiny
            color = self.colors['text'] if line.strip() else self.colors['text_light']
            
            if line.strip():  # Don't draw empty lines
                self.draw_text_centered(line, font, color, self.width // 2, y, False)
        
        # Back instruction
        self.draw_text_centered("Press ESC to return to menu", self.font_tiny,
                               self.colors['text_light'], self.width // 2, self.height - 60)
    
    def get_player_name_input(self) -> Optional[str]:
        """Get player name input for leaderboard (simplified version)."""
        # For this demo, return a default name
        # In a full implementation, this would show an input dialog
        return "Player"