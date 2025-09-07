"""
Typing Racer Game - Car Animation and Movement
Handles the cute chibi-style car that moves based on typing progress.
"""

import pygame
import math
from typing import Tuple

class Car:
    """Chibi-style car that moves along the race track."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize car with screen dimensions."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Track settings
        self.track_y = screen_height - 200  # Y position of track center
        self.track_start_x = 50
        self.track_end_x = screen_width - 150  # Leave space for finish line
        self.track_length = self.track_end_x - self.track_start_x
        
        # Car properties
        self.position = 0.0  # Progress from 0.0 to 1.0
        self.x = self.track_start_x
        self.y = self.track_y
        
        # Animation state
        self.bounce = 0.0
        self.wheel_rotation = 0.0
        self.speed = 0.0  # Current speed for animations
        self.boost_timer = 0.0
        self.penalty_timer = 0.0
        
        # Colors (pastel palette)
        self.car_body_color = (189, 224, 254)      # Light blue
        self.car_accent_color = (144, 238, 144)    # Light green
        self.wheel_color = (60, 60, 60)            # Dark gray
        self.eye_color = (255, 255, 255)           # White
        self.pupil_color = (60, 60, 60)            # Dark gray
        
    def reset(self):
        """Reset car to starting position."""
        self.position = 0.0
        self.x = self.track_start_x
        self.y = self.track_y
        self.bounce = 0.0
        self.wheel_rotation = 0.0
        self.speed = 0.0
        self.boost_timer = 0.0
        self.penalty_timer = 0.0
        
    def move_by_progress(self, progress_increment: float):
        """Move car forward by a progress amount (0.0 to 1.0)."""
        old_position = self.position
        self.position = min(1.0, self.position + progress_increment)
        
        # Update screen position
        self.x = self.track_start_x + (self.position * self.track_length)
        
        # Calculate speed for animations
        self.speed = (self.position - old_position) * 100
        
        # Add bounce when moving
        if progress_increment > 0:
            self.bounce = min(self.bounce + 0.5, 2.0)
            
    def apply_boost(self):
        """Apply speed boost effect when completing a word."""
        self.move_by_progress(0.05)  # 5% boost
        self.boost_timer = 1.0  # 1 second boost effect
        
    def apply_penalty(self):
        """Apply penalty effect for mistakes."""
        self.penalty_timer = 0.5  # 0.5 second penalty effect
        
    def get_position(self) -> Tuple[int, int]:
        """Get current screen position of the car."""
        # Add bounce effect
        bounce_offset = math.sin(self.bounce) * 3
        return (int(self.x), int(self.y + bounce_offset))
        
    def get_progress(self) -> float:
        """Get progress from 0.0 to 1.0."""
        return self.position
        
    def has_finished(self) -> bool:
        """Check if car has reached the finish line."""
        return self.position >= 1.0
        
    def update(self, dt: float):
        """Update car animations.""" 
        # Update bounce animation
        if self.bounce > 0:
            self.bounce = max(0, self.bounce - dt * 3)
            
        # Update wheel rotation based on speed
        if self.speed > 0:
            self.wheel_rotation += self.speed * dt * 5
            if self.wheel_rotation >= 360:
                self.wheel_rotation -= 360
                
        # Update effect timers
        if self.boost_timer > 0:
            self.boost_timer = max(0, self.boost_timer - dt)
            
        if self.penalty_timer > 0:
            self.penalty_timer = max(0, self.penalty_timer - dt)
            
        # Decay speed
        self.speed *= 0.95
        
    def draw(self, screen: pygame.Surface):
        """Draw the cute chibi car with animations."""
        car_pos = self.get_position()
        x, y = car_pos
        
        # Car dimensions
        car_width = 60
        car_height = 35
        wheel_radius = 8
        
        # Effects
        if self.boost_timer > 0:
            # Boost glow effect
            glow_radius = int(40 + math.sin(pygame.time.get_ticks() * 0.01) * 5)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 255, 0, 50), (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, (x - glow_radius, y - glow_radius))
            
        if self.penalty_timer > 0:
            # Red flash effect for penalty
            flash_surface = pygame.Surface((car_width + 20, car_height + 20), pygame.SRCALPHA)
            flash_surface.fill((255, 0, 0, 100))
            screen.blit(flash_surface, (x - car_width//2 - 10, y - car_height//2 - 10))
            
        # Car shadow
        shadow_offset = 3
        shadow_rect = pygame.Rect(x - car_width//2 + shadow_offset, y - car_height//2 + shadow_offset, 
                                 car_width, car_height)
        pygame.draw.ellipse(screen, (200, 200, 200), shadow_rect)
        
        # Car body (main rounded rectangle)
        car_rect = pygame.Rect(x - car_width//2, y - car_height//2, car_width, car_height)
        pygame.draw.rect(screen, self.car_body_color, car_rect, border_radius=15)
        
        # Car roof (smaller rounded rectangle on top)
        roof_width = car_width - 16
        roof_height = car_height - 16
        roof_rect = pygame.Rect(x - roof_width//2, y - roof_height//2 - 3, roof_width, roof_height)
        pygame.draw.rect(screen, self.car_accent_color, roof_rect, border_radius=10)
        
        # Wheels with rotation
        wheel_offset_x = car_width//2 - 8
        wheel_y_offset = car_height//2 - 3
        
        # Left wheel
        left_wheel_pos = (x - wheel_offset_x, y + wheel_y_offset)
        pygame.draw.circle(screen, self.wheel_color, left_wheel_pos, wheel_radius)
        
        # Wheel spokes (rotating)
        spoke_angle = math.radians(self.wheel_rotation)
        for i in range(4):
            angle = spoke_angle + (i * math.pi / 2)
            spoke_end_x = left_wheel_pos[0] + math.cos(angle) * (wheel_radius - 2)
            spoke_end_y = left_wheel_pos[1] + math.sin(angle) * (wheel_radius - 2)
            pygame.draw.line(screen, (200, 200, 200), left_wheel_pos, 
                           (spoke_end_x, spoke_end_y), 2)
        
        # Right wheel  
        right_wheel_pos = (x + wheel_offset_x, y + wheel_y_offset)
        pygame.draw.circle(screen, self.wheel_color, right_wheel_pos, wheel_radius)
        
        # Right wheel spokes
        for i in range(4):
            angle = spoke_angle + (i * math.pi / 2)
            spoke_end_x = right_wheel_pos[0] + math.cos(angle) * (wheel_radius - 2)
            spoke_end_y = right_wheel_pos[1] + math.sin(angle) * (wheel_radius - 2)
            pygame.draw.line(screen, (200, 200, 200), right_wheel_pos,
                           (spoke_end_x, spoke_end_y), 2)
        
        # Cute eyes on the windshield
        eye_radius = 4
        left_eye_pos = (x - 8, y - 8)
        right_eye_pos = (x + 8, y - 8)
        
        # Eye whites
        pygame.draw.circle(screen, self.eye_color, left_eye_pos, eye_radius)
        pygame.draw.circle(screen, self.eye_color, right_eye_pos, eye_radius)
        
        # Pupils (look in direction of movement)
        pupil_radius = 2
        look_offset = 1 if self.speed > 0 else 0
        
        pygame.draw.circle(screen, self.pupil_color, 
                          (left_eye_pos[0] + look_offset, left_eye_pos[1]), pupil_radius)
        pygame.draw.circle(screen, self.pupil_color,
                          (right_eye_pos[0] + look_offset, right_eye_pos[1]), pupil_radius)
        
        # Cute mouth (small line or curve)
        mouth_width = 8
        mouth_y = y + 4
        if self.boost_timer > 0:
            # Happy mouth when boosting
            pygame.draw.arc(screen, self.pupil_color,
                          pygame.Rect(x - mouth_width//2, mouth_y - 2, mouth_width, 6),
                          0, math.pi, 2)
        elif self.penalty_timer > 0:
            # Sad mouth when penalized  
            pygame.draw.arc(screen, self.pupil_color,
                          pygame.Rect(x - mouth_width//2, mouth_y + 2, mouth_width, 6),
                          math.pi, 2 * math.pi, 2)
        else:
            # Neutral mouth
            pygame.draw.line(screen, self.pupil_color,
                           (x - mouth_width//2, mouth_y), (x + mouth_width//2, mouth_y), 2)
        
        # Speed trail particles when moving fast
        if self.speed > 10:
            for i in range(3):
                trail_x = x - car_width//2 - (i * 15) - random.randint(0, 5)
                trail_y = y + random.randint(-10, 10)
                trail_size = 3 - i
                if trail_size > 0:
                    pygame.draw.circle(screen, (200, 200, 255, 150), 
                                     (trail_x, trail_y), trail_size)

# Import random for trail particles
import random