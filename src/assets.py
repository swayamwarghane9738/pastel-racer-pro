"""
Typing Racer Game - Asset Management
Handles creation of embedded assets and graphics.
"""

import pygame
import os
import base64
from typing import Dict, Any

class AssetManager:
    """Manages embedded assets and procedural graphics generation."""
    
    def __init__(self):
        """Initialize asset manager."""
        self.assets_created = False
        
    def initialize(self):
        """Initialize and create all embedded assets."""
        if self.assets_created:
            return
            
        # Create data directory for persistent files
        self.ensure_data_directory()
        
        # Create any embedded font files if needed
        # (For this implementation, we'll use system fonts)
        
        self.assets_created = True
        
    def ensure_data_directory(self):
        """Create data directory for saving game files."""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
    def draw_rounded_rect(self, surface: pygame.Surface, color: tuple, rect: pygame.Rect, 
                         radius: int = 10):
        """Draw a rounded rectangle on the given surface."""
        # Draw main rectangle
        main_rect = pygame.Rect(rect.x + radius, rect.y, 
                               rect.width - 2 * radius, rect.height)
        pygame.draw.rect(surface, color, main_rect)
        
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
        
    def create_button_surface(self, width: int, height: int, text: str, 
                             font: pygame.font.Font, bg_color: tuple, 
                             text_color: tuple, border_radius: int = 15) -> pygame.Surface:
        """Create a button surface with rounded corners and text."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw button background
        button_rect = pygame.Rect(0, 0, width, height)
        self.draw_rounded_rect(surface, bg_color, button_rect, border_radius)
        
        # Draw text centered
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        surface.blit(text_surface, text_rect)
        
        return surface
        
    def create_progress_bar(self, width: int, height: int, progress: float, 
                           bg_color: tuple, fill_color: tuple, 
                           border_radius: int = 10) -> pygame.Surface:
        """Create a progress bar surface."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Background
        bg_rect = pygame.Rect(0, 0, width, height)
        self.draw_rounded_rect(surface, bg_color, bg_rect, border_radius)
        
        # Fill
        fill_width = int(width * progress)
        if fill_width > 0:
            fill_rect = pygame.Rect(0, 0, fill_width, height)
            self.draw_rounded_rect(surface, fill_color, fill_rect, border_radius)
            
        return surface
        
    def create_panel_surface(self, width: int, height: int, bg_color: tuple,
                            border_color: tuple = None, border_width: int = 2,
                            border_radius: int = 15, shadow: bool = True) -> pygame.Surface:
        """Create a panel surface with optional border and shadow."""
        # Create larger surface to accommodate shadow
        shadow_offset = 3 if shadow else 0
        surface = pygame.Surface((width + shadow_offset, height + shadow_offset), pygame.SRCALPHA)
        
        # Draw shadow
        if shadow:
            shadow_rect = pygame.Rect(shadow_offset, shadow_offset, width, height)
            self.draw_rounded_rect(surface, (0, 0, 0, 50), shadow_rect, border_radius)
            
        # Draw main panel
        panel_rect = pygame.Rect(0, 0, width, height)
        self.draw_rounded_rect(surface, bg_color, panel_rect, border_radius)
        
        # Draw border
        if border_color:
            # Create border by drawing a slightly larger rectangle behind
            border_rect = pygame.Rect(-border_width, -border_width, 
                                     width + 2 * border_width, height + 2 * border_width)
            border_surface = pygame.Surface((width + 2 * border_width, height + 2 * border_width), pygame.SRCALPHA)
            self.draw_rounded_rect(border_surface, border_color, 
                                 pygame.Rect(0, 0, width + 2 * border_width, height + 2 * border_width), 
                                 border_radius + border_width)
            
            # Blit border surface first, then panel on top
            temp_surface = pygame.Surface((width + shadow_offset + 2 * border_width, 
                                         height + shadow_offset + 2 * border_width), pygame.SRCALPHA)
            temp_surface.blit(border_surface, (0, 0))
            temp_surface.blit(surface, (border_width, border_width))
            return temp_surface
            
        return surface
        
    def create_gradient_surface(self, width: int, height: int, 
                               start_color: tuple, end_color: tuple,
                               vertical: bool = True) -> pygame.Surface:
        """Create a gradient surface."""
        surface = pygame.Surface((width, height))
        
        if vertical:
            for y in range(height):
                ratio = y / height
                color = [
                    int(start_color[i] + (end_color[i] - start_color[i]) * ratio)
                    for i in range(3)
                ]
                pygame.draw.line(surface, color, (0, y), (width, y))
        else:
            for x in range(width):
                ratio = x / width
                color = [
                    int(start_color[i] + (end_color[i] - start_color[i]) * ratio)
                    for i in range(3)
                ]
                pygame.draw.line(surface, color, (x, 0), (x, height))
                
        return surface
        
    def create_car_icon(self, size: int = 32, color: tuple = (189, 224, 254)) -> pygame.Surface:
        """Create a small car icon surface."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Car body
        car_width = int(size * 0.8)
        car_height = int(size * 0.5)
        car_x = (size - car_width) // 2
        car_y = (size - car_height) // 2
        
        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        pygame.draw.rect(surface, color, car_rect, border_radius=car_height // 3)
        
        # Wheels
        wheel_radius = max(3, size // 8)
        wheel_color = (60, 60, 60)
        
        left_wheel_pos = (car_x + wheel_radius, car_y + car_height)
        right_wheel_pos = (car_x + car_width - wheel_radius, car_y + car_height)
        
        pygame.draw.circle(surface, wheel_color, left_wheel_pos, wheel_radius)
        pygame.draw.circle(surface, wheel_color, right_wheel_pos, wheel_radius)
        
        return surface
        
    def get_color_palette(self) -> Dict[str, tuple]:
        """Get the game's color palette."""
        return {
            'bg': (253, 221, 210),       # Warm peach
            'bg_light': (248, 237, 235),  # Light pink
            'accent': (216, 226, 220),    # Mint green
            'accent_blue': (189, 224, 254), # Light blue
            'text': (60, 60, 60),        # Dark gray
            'text_light': (120, 120, 120), # Medium gray
            'correct': (144, 238, 144),   # Light green
            'error': (255, 182, 193),     # Light pink (error)
            'white': (255, 255, 255),
            'shadow': (200, 200, 200),    # Light shadow
        }

# Example of how to embed a small font file as base64 (if needed)
# This would be a very small, permissively licensed font
EMBEDDED_FONT_DATA = ""  # Would contain base64 encoded font data

def create_embedded_font(size: int) -> pygame.font.Font:
    """Create font from embedded data (placeholder implementation)."""
    # For this demo, we'll use system fonts
    # In a full implementation, this could decode base64 font data
    try:
        return pygame.font.SysFont('Arial', size)
    except:
        return pygame.font.Font(None, size)