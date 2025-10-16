import pygame
import os
from settings import *

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        
        # Volume settings
        self.master_volume = MASTER_VOLUME
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME
        
        # Sound effects dictionary
        self.sounds = {}
        self.music = {}
        
        # Load sounds
        self.load_sounds()
        
        # Current playing music
        self.current_music = None
        
    def load_sounds(self):
        """Load all sound effects and music"""
        sounds_path = "assets/Sounds"
        
        # Create sounds directory if it doesn't exist
        if not os.path.exists(sounds_path):
            os.makedirs(sounds_path)
            
        # Define sound files to load
        sound_files = {
            'button_click': 'button_click.wav',
            'enemy_death': 'enemy_death.wav',
            'player_hit': 'player_hit.wav',
            'hunt_mode_start': 'hunt_mode_start.wav',
            'hunt_mode_end': 'hunt_mode_start.wav',  # Reuse existing sound
            'level_complete': 'level_complete.wav',
            'game_over': 'boss_spawn.wav',  # Reuse existing sound
            'boss_spawn': 'boss_spawn.wav',
            'power_up': 'button_click.wav',  # Reuse existing sound
            'footstep': 'button_click.wav'  # Reuse existing sound
        }
        
        # Load sound effects
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(sounds_path, filename)
            if os.path.exists(filepath):
                self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                self.sounds[sound_name].set_volume(self.sfx_volume * self.master_volume)
            else:
                # Create placeholder sound if file doesn't exist
                self.sounds[sound_name] = self.create_placeholder_sound()
                
        # Define music files to load
        music_files = {
            'lobby_music': 'lobby_music.wav',
            'level_music': 'level_music.wav',
            'hunt_music': 'hunt_music.wav',
            'boss_music': 'boss_music.wav'
        }
        
        # Load music
        for music_name, filename in music_files.items():
            filepath = os.path.join(sounds_path, filename)
            if os.path.exists(filepath):
                self.music[music_name] = filepath
            else:
                # Create placeholder music if file doesn't exist
                self.music[music_name] = None
                
    def create_placeholder_sound(self):
        """Create a simple placeholder sound"""
        # Create a very short, quiet sound as placeholder
        try:
            import numpy as np
            # Create a 2D array for stereo sound
            sound_data = np.zeros((1000, 2), dtype=np.int16)
            sound_array = pygame.sndarray.make_sound(sound_data)
            return sound_array
        except (ImportError, NotImplementedError):
            # Fallback: create a silent sound using pygame's built-in functionality
            silent_sound = pygame.mixer.Sound(buffer=bytes([0] * 4000))  # 1000 samples * 2 channels * 2 bytes per sample
            return silent_sound
        
    def play_sound(self, sound_name, volume=1.0):
        """Play a sound effect"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(self.sfx_volume * self.master_volume * volume)
            sound.play()
            
    def play_music(self, music_name, loops=-1, volume=1.0):
        """Play background music"""
        if music_name in self.music and self.music[music_name]:
            pygame.mixer.music.load(self.music[music_name])
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume * volume)
            pygame.mixer.music.play(loops)
            self.current_music = music_name
            
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.current_music = None
        
    def fade_out_music(self, duration=1000):
        """Fade out background music"""
        pygame.mixer.music.fadeout(duration)
        
    def set_master_volume(self, volume):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        self.update_all_volumes()
        
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.current_music:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume * self.master_volume)
            
    def update_all_volumes(self):
        """Update all sound and music volumes"""
        # Update sound effects
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume * self.master_volume)
            
        # Update music
        if self.current_music:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            
    def get_volume_settings(self):
        """Get current volume settings"""
        return {
            'master': self.master_volume,
            'music': self.music_volume,
            'sfx': self.sfx_volume
        }
        
    def set_volume_settings(self, settings):
        """Set volume settings from dictionary"""
        if 'master' in settings:
            self.set_master_volume(settings['master'])
        if 'music' in settings:
            self.set_music_volume(settings['music'])
        if 'sfx' in settings:
            self.set_sfx_volume(settings['sfx'])

# Global audio manager instance
audio_manager = AudioManager()
