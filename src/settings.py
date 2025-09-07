"""
Typing Racer Game - Settings Management
Handles game configuration and user preferences.
"""

import json
import os
from typing import Dict, Any, Optional

class SettingsManager:
    """Manages game settings with JSON persistence."""
    
    def __init__(self):
        """Initialize settings manager with default values."""
        self.settings_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                         'data', 'settings.json')
        
        # Default settings
        self.default_settings = {
            'audio': {
                'master_volume': 0.7,
                'sfx_volume': 1.0,
                'mute': False
            },
            'gameplay': {
                'difficulty': 'normal',  # easy, normal, hard, endless
                'movement_pattern': 'top_right_to_bottom_left',
                'time_limit': 60,
                'auto_advance': True
            },
            'display': {
                'font_size': 'normal',  # small, normal, large
                'high_contrast': False,
                'colorblind_mode': False,
                'show_fps': False,
                'fullscreen': False
            },
            'controls': {
                'backspace_key': 'backspace',
                'pause_key': 'escape', 
                'confirm_key': 'return'
            },
            'accessibility': {
                'slow_animations': False,
                'reduce_particles': False,
                'large_text': False,
                'high_contrast': False
            },
            'stats': {
                'games_played': 0,
                'total_words_typed': 0,
                'best_wpm': 0.0,
                'best_accuracy': 0.0,
                'total_time_played': 0.0
            }
        }
        
        # Current settings (loaded from file or defaults)
        self.current_settings = {}
        
        # Load settings from file
        self.load_settings()
        
    def load_settings(self):
        """Load settings from JSON file, creating defaults if file doesn't exist."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    
                # Merge with defaults to ensure all keys exist
                self.current_settings = self._merge_settings(self.default_settings, loaded_settings)
            else:
                # Use defaults if no settings file exists
                self.current_settings = self.default_settings.copy()
                self.save_settings()  # Create the file
                
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading settings: {e}")
            # Fall back to defaults
            self.current_settings = self.default_settings.copy()
            
    def _merge_settings(self, defaults: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge loaded settings with defaults."""
        result = defaults.copy()
        
        for key, value in loaded.items():
            if key in result:
                if isinstance(value, dict) and isinstance(result[key], dict):
                    result[key] = self._merge_settings(result[key], value)
                else:
                    result[key] = value
            else:
                result[key] = value
                
        return result
        
    def save_settings(self):
        """Save current settings to JSON file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            with open(self.settings_file, 'w') as f:
                json.dump(self.current_settings, f, indent=2)
                
        except IOError as e:
            print(f"Error saving settings: {e}")
            
    def get(self, category: str, key: str, default=None) -> Any:
        """Get a setting value by category and key."""
        try:
            return self.current_settings.get(category, {}).get(key, default)
        except (KeyError, TypeError):
            return default
            
    def set(self, category: str, key: str, value: Any):
        """Set a setting value by category and key."""
        if category not in self.current_settings:
            self.current_settings[category] = {}
            
        self.current_settings[category][key] = value
        
    def get_all(self, category: str) -> Dict[str, Any]:
        """Get all settings in a category."""
        return self.current_settings.get(category, {})
        
    def set_all(self, category: str, settings: Dict[str, Any]):
        """Set all settings in a category."""
        self.current_settings[category] = settings
        
    def reset_category(self, category: str):
        """Reset a category to defaults."""
        if category in self.default_settings:
            self.current_settings[category] = self.default_settings[category].copy()
            
    def reset_all(self):
        """Reset all settings to defaults."""
        self.current_settings = self.default_settings.copy()
        
    # Convenience methods for common settings
    def get_master_volume(self) -> float:
        """Get master audio volume (0.0 to 1.0)."""
        return self.get('audio', 'master_volume', 0.7)
        
    def set_master_volume(self, volume: float):
        """Set master audio volume (0.0 to 1.0)."""
        self.set('audio', 'master_volume', max(0.0, min(1.0, volume)))
        
    def get_sfx_volume(self) -> float:
        """Get sound effects volume (0.0 to 1.0)."""
        return self.get('audio', 'sfx_volume', 1.0)
        
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)."""
        self.set('audio', 'sfx_volume', max(0.0, min(1.0, volume)))
        
    def is_muted(self) -> bool:
        """Check if audio is muted."""
        return self.get('audio', 'mute', False)
        
    def set_muted(self, muted: bool):
        """Set audio mute state."""
        self.set('audio', 'mute', muted)
        
    def get_difficulty(self) -> str:
        """Get current difficulty setting."""
        return self.get('gameplay', 'difficulty', 'normal')
        
    def set_difficulty(self, difficulty: str):
        """Set difficulty (easy, normal, hard, endless)."""
        if difficulty in ['easy', 'normal', 'hard', 'endless']:
            self.set('gameplay', 'difficulty', difficulty)
            
    def get_font_size(self) -> str:
        """Get font size setting."""
        return self.get('display', 'font_size', 'normal')
        
    def set_font_size(self, size: str):
        """Set font size (small, normal, large)."""
        if size in ['small', 'normal', 'large']:
            self.set('display', 'font_size', size)
            
    def is_high_contrast(self) -> bool:
        """Check if high contrast mode is enabled."""
        return self.get('accessibility', 'high_contrast', False)
        
    def set_high_contrast(self, enabled: bool):
        """Set high contrast mode."""
        self.set('accessibility', 'high_contrast', enabled)
        
    def is_colorblind_mode(self) -> bool:
        """Check if colorblind mode is enabled."""
        return self.get('display', 'colorblind_mode', False)
        
    def set_colorblind_mode(self, enabled: bool):
        """Set colorblind mode."""
        self.set('display', 'colorblind_mode', enabled)
        
    def get_movement_pattern(self) -> str:
        """Get word movement pattern."""
        return self.get('gameplay', 'movement_pattern', 'top_right_to_bottom_left')
        
    def set_movement_pattern(self, pattern: str):
        """Set word movement pattern."""
        valid_patterns = [
            'top_right_to_bottom_left',
            'left_to_right',
            'top_to_bottom',
            'random_corners'
        ]
        if pattern in valid_patterns:
            self.set('gameplay', 'movement_pattern', pattern)
            
    # Statistics methods
    def increment_games_played(self):
        """Increment games played counter."""
        current = self.get('stats', 'games_played', 0)
        self.set('stats', 'games_played', current + 1)
        
    def add_words_typed(self, count: int):
        """Add to total words typed."""
        current = self.get('stats', 'total_words_typed', 0)
        self.set('stats', 'total_words_typed', current + count)
        
    def update_best_wpm(self, wpm: float):
        """Update best WPM if new record."""
        current_best = self.get('stats', 'best_wpm', 0.0)
        if wpm > current_best:
            self.set('stats', 'best_wpm', wpm)
            
    def update_best_accuracy(self, accuracy: float):
        """Update best accuracy if new record."""
        current_best = self.get('stats', 'best_accuracy', 0.0)
        if accuracy > current_best:
            self.set('stats', 'best_accuracy', accuracy)
            
    def add_play_time(self, seconds: float):
        """Add to total play time."""
        current = self.get('stats', 'total_time_played', 0.0)
        self.set('stats', 'total_time_played', current + seconds)
        
    def get_stats_summary(self) -> Dict[str, Any]:
        """Get a summary of all statistics."""
        return self.get_all('stats')
        
    def export_settings(self) -> str:
        """Export settings as JSON string."""
        return json.dumps(self.current_settings, indent=2)
        
    def import_settings(self, json_string: str) -> bool:
        """Import settings from JSON string. Returns True if successful."""
        try:
            imported = json.loads(json_string)
            self.current_settings = self._merge_settings(self.default_settings, imported)
            self.save_settings()
            return True
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error importing settings: {e}")
            return False