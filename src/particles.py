"""
Typing Racer Game - Particle Effects System
Handles confetti, sparkles, and other visual effects.
"""

import pygame
import math
import random
from typing import List, Tuple

class Particle:
    """Individual particle with physics."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 color: Tuple[int, int, int], size: float, lifetime: float):
        """Initialize particle with position, velocity, color, size and lifetime."""
        self.x = x
        self.y = y
        self.vx = vx  # Velocity X
        self.vy = vy  # Velocity Y
        self.color = color
        self.size = size
        self.max_size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = 200  # Pixels per second squared
        
    def update(self, dt: float) -> bool:
        """Update particle physics. Returns False when particle should be removed."""
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Apply gravity
        self.vy += self.gravity * dt
        
        # Update lifetime
        self.lifetime -= dt
        
        # Fade size based on lifetime
        life_ratio = self.lifetime / self.max_lifetime
        self.size = self.max_size * life_ratio
        
        return self.lifetime > 0 and self.size > 0.1
        
    def draw(self, screen: pygame.Surface):
        """Draw the particle."""
        if self.size <= 0:
            return
            
        # Calculate alpha based on lifetime
        life_ratio = self.lifetime / self.max_lifetime
        alpha = int(255 * life_ratio)
        
        # Create surface with per-pixel alpha
        particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        
        # Draw particle with alpha
        color_with_alpha = (*self.color, alpha)
        pygame.draw.circle(particle_surface, color_with_alpha, 
                          (int(self.size), int(self.size)), int(self.size))
        
        # Blit to screen
        screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))

class Sparkle:
    """Sparkly star-shaped particle."""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], lifetime: float):
        """Initialize sparkle at position with color and lifetime."""
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-180, 180)  # degrees per second
        self.scale = random.uniform(0.5, 1.5)
        
    def update(self, dt: float) -> bool:
        """Update sparkle animation."""
        self.lifetime -= dt
        self.rotation += self.rotation_speed * dt
        
        return self.lifetime > 0
        
    def draw(self, screen: pygame.Surface):
        """Draw sparkle as animated star."""
        if self.lifetime <= 0:
            return
            
        # Calculate alpha and size based on lifetime
        life_ratio = self.lifetime / self.max_lifetime
        alpha = int(255 * life_ratio)
        size = int(8 * self.scale * life_ratio)
        
        if size < 1:
            return
            
        # Create star points
        points = []
        for i in range(8):  # 8-pointed star
            angle = math.radians(self.rotation + i * 45)
            if i % 2 == 0:  # Outer points
                radius = size
            else:  # Inner points  
                radius = size * 0.5
                
            point_x = self.x + math.cos(angle) * radius
            point_y = self.y + math.sin(angle) * radius
            points.append((point_x, point_y))
            
        # Draw star with alpha
        if len(points) >= 3:
            star_surface = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            
            # Offset points for surface coordinates
            surface_points = [(p[0] - self.x + size * 1.5, p[1] - self.y + size * 1.5) for p in points]
            
            try:
                pygame.draw.polygon(star_surface, color_with_alpha, surface_points)
                screen.blit(star_surface, (int(self.x - size * 1.5), int(self.y - size * 1.5)))
            except ValueError:
                # Fallback to circle if polygon fails
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class ParticleSystem:
    """Manages all particle effects in the game."""
    
    def __init__(self):
        """Initialize empty particle system."""
        self.particles: List[Particle] = []
        self.sparkles: List[Sparkle] = []
        
        # Preset colors (pastel palette)
        self.colors = {
            'confetti': [
                (255, 182, 193),  # Light pink
                (189, 224, 254),  # Light blue
                (144, 238, 144),  # Light green
                (255, 255, 224),  # Light yellow
                (221, 160, 221),  # Plum
                (255, 218, 185),  # Peach
            ],
            'sparkle': [
                (255, 255, 255),  # White
                (255, 255, 224),  # Light yellow
                (224, 255, 255),  # Light cyan
            ],
            'boost': [
                (144, 238, 144),  # Light green
                (255, 255, 224),  # Light yellow
            ]
        }
        
    def clear(self):
        """Clear all particles."""
        self.particles.clear()
        self.sparkles.clear()
        
    def add_word_completion_effect(self, x: float, y: float):
        """Add particles for word completion at car position."""
        # Add small burst of confetti
        for _ in range(8):
            # Random velocity in cone above car
            angle = random.uniform(-math.pi/3, math.pi/3)  # 60 degree cone upward
            speed = random.uniform(100, 200)
            vx = math.cos(angle + math.pi/2) * speed  # Add pi/2 to point upward
            vy = math.sin(angle + math.pi/2) * speed
            
            color = random.choice(self.colors['confetti'])
            size = random.uniform(3, 6)
            lifetime = random.uniform(1.0, 2.0)
            
            particle = Particle(x, y, vx, vy, color, size, lifetime)
            self.particles.append(particle)
            
        # Add sparkles
        for _ in range(3):
            sparkle_x = x + random.uniform(-20, 20)
            sparkle_y = y + random.uniform(-15, 15)
            color = random.choice(self.colors['sparkle'])
            lifetime = random.uniform(0.5, 1.0)
            
            sparkle = Sparkle(sparkle_x, sparkle_y, color, lifetime)
            self.sparkles.append(sparkle)
            
    def add_celebration_effect(self, x: float, y: float):
        """Add big celebration effect for winning."""
        # Large confetti burst
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(150, 300)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 100  # Bias upward
            
            color = random.choice(self.colors['confetti'])
            size = random.uniform(4, 8)
            lifetime = random.uniform(2.0, 4.0)
            
            particle = Particle(x, y, vx, vy, color, size, lifetime)
            self.particles.append(particle)
            
        # Many sparkles
        for _ in range(10):
            sparkle_x = x + random.uniform(-50, 50)
            sparkle_y = y + random.uniform(-30, 30)
            color = random.choice(self.colors['sparkle'])
            lifetime = random.uniform(1.0, 2.5)
            
            sparkle = Sparkle(sparkle_x, sparkle_y, color, lifetime)
            self.sparkles.append(sparkle)
            
    def add_boost_effect(self, x: float, y: float):
        """Add speed boost particles."""
        for _ in range(5):
            # Horizontal trail behind car
            offset_x = random.uniform(-30, -10)
            offset_y = random.uniform(-10, 10)
            
            vx = random.uniform(-50, 0)  # Move backward relative to car
            vy = random.uniform(-20, 20)
            
            color = random.choice(self.colors['boost'])
            size = random.uniform(2, 4)
            lifetime = random.uniform(0.5, 1.0)
            
            particle = Particle(x + offset_x, y + offset_y, vx, vy, color, size, lifetime)
            self.particles.append(particle)
            
    def add_error_effect(self, x: float, y: float):
        """Add error/mistake particles."""
        # Red puff particles
        for _ in range(6):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 100)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = (255, 182, 193)  # Light pink/red
            size = random.uniform(2, 4)
            lifetime = random.uniform(0.3, 0.8)
            
            particle = Particle(x, y, vx, vy, color, size, lifetime)
            self.particles.append(particle)
            
    def update(self, dt: float):
        """Update all particles."""
        # Update and filter particles
        self.particles = [p for p in self.particles if p.update(dt)]
        self.sparkles = [s for s in self.sparkles if s.update(dt)]
        
    def draw(self, screen: pygame.Surface):
        """Draw all particles."""
        # Draw particles first (behind sparkles)
        for particle in self.particles:
            particle.draw(screen)
            
        # Draw sparkles on top
        for sparkle in self.sparkles:
            sparkle.draw(screen)
            
    def get_particle_count(self) -> int:
        """Get total number of active particles."""
        return len(self.particles) + len(self.sparkles)