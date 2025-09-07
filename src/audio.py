"""
Typing Racer Game - Audio System
Handles sound effects with procedurally generated audio.
"""

import pygame
import numpy as np
import math
import io
from typing import Dict, Optional

class AudioManager:
    """Manages all game audio including procedurally generated sound effects."""
    
    def __init__(self, settings):
        """Initialize audio system with settings reference."""
        self.settings = settings
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        
        # Audio settings
        self.master_volume = 0.7
        self.sfx_volume = 1.0
        
        # Initialize pygame mixer if not already done
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except pygame.error:
            print("Warning: Could not initialize audio")
            
        # Generate all sound effects
        self.generate_sounds()
        
    def generate_sounds(self):
        """Generate all sound effects procedurally."""
        sample_rate = 22050
        
        # Generate correct typing sound (pleasant beep)
        self.sounds['correct'] = self.generate_beep(440, 0.1, sample_rate, fade_out=True)
        
        # Generate error sound (lower, harsher tone)
        self.sounds['error'] = self.generate_buzz(220, 0.15, sample_rate)
        
        # Generate word completion sound (ascending notes)
        self.sounds['word_complete'] = self.generate_chord([440, 554, 659], 0.3, sample_rate)
        
        # Generate backspace sound (soft click)
        self.sounds['backspace'] = self.generate_click(0.05, sample_rate)
        
        # Generate menu selection sound
        self.sounds['menu_select'] = self.generate_beep(660, 0.1, sample_rate, fade_out=True)
        
        # Generate game win sound (victory fanfare)
        self.sounds['game_win'] = self.generate_victory_fanfare(sample_rate)
        
    def generate_beep(self, frequency: float, duration: float, sample_rate: int, 
                     fade_out: bool = False) -> pygame.mixer.Sound:
        """Generate a clean beep tone."""
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))  # Stereo
        
        for i in range(frames):
            # Generate sine wave
            sample = math.sin(2 * math.pi * frequency * i / sample_rate)
            
            # Apply envelope (fade in/out)
            if fade_out:
                # Fade out envelope
                envelope = max(0, 1 - (i / frames))
            else:
                # Simple attack/decay envelope
                if i < frames * 0.1:  # Attack (10%)
                    envelope = i / (frames * 0.1)
                elif i > frames * 0.7:  # Decay (30%)
                    envelope = 1 - (i - frames * 0.7) / (frames * 0.3)
                else:  # Sustain
                    envelope = 1
                    
            sample *= envelope * 0.3  # Reduce volume
            arr[i] = [sample, sample]  # Stereo
            
        return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))
    
    def generate_buzz(self, frequency: float, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a buzz/harsh sound for errors."""
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            # Mix sine wave with some harmonics for harsh sound
            sample = (
                math.sin(2 * math.pi * frequency * i / sample_rate) * 0.5 +
                math.sin(2 * math.pi * frequency * 1.5 * i / sample_rate) * 0.3 +
                math.sin(2 * math.pi * frequency * 2 * i / sample_rate) * 0.2
            )
            
            # Envelope with quick decay
            envelope = max(0, 1 - (i / frames) ** 0.5)  # Square root decay
            sample *= envelope * 0.2
            
            arr[i] = [sample, sample]
            
        return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))
    
    def generate_chord(self, frequencies: list, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a chord from multiple frequencies."""
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            sample = 0
            for freq in frequencies:
                sample += math.sin(2 * math.pi * freq * i / sample_rate)
                
            sample /= len(frequencies)  # Normalize
            
            # Envelope 
            if i < frames * 0.1:  # Attack
                envelope = i / (frames * 0.1)
            elif i > frames * 0.6:  # Decay
                envelope = 1 - (i - frames * 0.6) / (frames * 0.4)
            else:  # Sustain
                envelope = 1
                
            sample *= envelope * 0.25
            arr[i] = [sample, sample]
            
        return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))
    
    def generate_click(self, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a soft click sound."""
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            # High frequency with rapid decay for click effect
            sample = math.sin(2 * math.pi * 2000 * i / sample_rate)
            
            # Very fast exponential decay
            envelope = math.exp(-i / (frames * 0.1))
            sample *= envelope * 0.15
            
            arr[i] = [sample, sample]
            
        return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))
    
    def generate_victory_fanfare(self, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a victory fanfare sound."""
        duration = 1.0
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        # Ascending melody notes
        melody = [440, 554, 659, 880]  # A, C#, E, A (octave)
        note_duration = frames // len(melody)
        
        for note_idx, freq in enumerate(melody):
            start_frame = note_idx * note_duration
            end_frame = min((note_idx + 1) * note_duration, frames)
            
            for i in range(start_frame, end_frame):
                local_i = i - start_frame
                local_frames = end_frame - start_frame
                
                # Primary tone
                sample = math.sin(2 * math.pi * freq * i / sample_rate) * 0.4
                
                # Add harmonic for richness
                sample += math.sin(2 * math.pi * freq * 2 * i / sample_rate) * 0.2
                
                # Envelope for each note
                if local_i < local_frames * 0.1:  # Attack
                    envelope = local_i / (local_frames * 0.1)
                elif local_i > local_frames * 0.7:  # Decay
                    envelope = 1 - (local_i - local_frames * 0.7) / (local_frames * 0.3)
                else:  # Sustain
                    envelope = 1
                    
                sample *= envelope
                
                if i < frames:
                    arr[i] = [sample, sample]
                    
        return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))
    
    def play_sound(self, sound_name: str, volume: float = 1.0):
        """Play a sound effect by name."""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(volume * self.sfx_volume * self.master_volume)
            sound.play()
        else:
            print(f"Warning: Sound '{sound_name}' not found")
            
    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)."""
        self.master_volume = max(0.0, min(1.0, volume))
        
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        
    def get_master_volume(self) -> float:
        """Get current master volume."""
        return self.master_volume
        
    def get_sfx_volume(self) -> float:
        """Get current sound effects volume."""
        return self.sfx_volume
        
    def stop_all_sounds(self):
        """Stop all currently playing sounds."""
        pygame.mixer.stop()

# Handle case where numpy is not available
try:
    import numpy as np
except ImportError:
    # Fallback implementation without numpy
    class AudioManager:
        def __init__(self, settings):
            self.settings = settings
            self.sounds = {}
            self.master_volume = 0.7
            self.sfx_volume = 1.0
            print("Warning: numpy not available, audio disabled")
            
        def generate_sounds(self):
            pass
            
        def play_sound(self, sound_name: str, volume: float = 1.0):
            pass
            
        def set_master_volume(self, volume: float):
            self.master_volume = max(0.0, min(1.0, volume))
            
        def set_sfx_volume(self, volume: float):
            self.sfx_volume = max(0.0, min(1.0, volume))
            
        def get_master_volume(self) -> float:
            return self.master_volume
            
        def get_sfx_volume(self) -> float:
            return self.sfx_volume
            
        def stop_all_sounds(self):
            pass