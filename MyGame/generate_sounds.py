import pygame
import numpy as np
import os
import wave
import struct

def generate_sound(frequency, duration, sample_rate=44100, volume=0.3):
    """Generate a simple sine wave sound"""
    frames = int(duration * sample_rate)
    arr = np.zeros((frames, 2))
    
    for i in range(frames):
        arr[i][0] = volume * np.sin(2 * np.pi * frequency * i / sample_rate)
        arr[i][1] = volume * np.sin(2 * np.pi * frequency * i / sample_rate)
    
    return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))

def save_wav_file(filename, sound_data, sample_rate=44100):
    """Save sound data as WAV file"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        # Convert to bytes
        sound_bytes = b''
        for frame in sound_data:
            left = int(frame[0])
            right = int(frame[1])
            sound_bytes += struct.pack('<hh', left, right)
        
        wav_file.writeframes(sound_bytes)

def generate_button_click():
    """Generate a button click sound"""
    # Short, high-pitched beep
    sound = generate_sound(800, 0.1, volume=0.2)
    return sound

def generate_enemy_death():
    """Generate an enemy death sound"""
    # Lower pitched, longer sound
    sound = generate_sound(200, 0.3, volume=0.4)
    return sound

def generate_hunt_mode_start():
    """Generate hunt mode start sound"""
    # Rising tone
    sound = generate_sound(600, 0.5, volume=0.3)
    return sound

def generate_level_complete():
    """Generate level complete sound"""
    # Upward arpeggio
    sound = generate_sound(400, 0.8, volume=0.5)
    return sound

def generate_boss_spawn():
    """Generate boss spawn sound"""
    # Deep, ominous sound
    sound = generate_sound(150, 1.0, volume=0.6)
    return sound

def main():
    pygame.mixer.init()
    
    # Create sounds directory
    sounds_dir = "assets/Sounds"
    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)
    
    # Generate sounds
    sounds = {
        'button_click.wav': generate_button_click(),
        'enemy_death.wav': generate_enemy_death(),
        'hunt_mode_start.wav': generate_hunt_mode_start(),
        'level_complete.wav': generate_level_complete(),
        'boss_spawn.wav': generate_boss_spawn(),
    }
    
    # Save sounds
    for filename, sound in sounds.items():
        filepath = os.path.join(sounds_dir, filename)
        # Get sound data and save as WAV
        sound_array = pygame.sndarray.array(sound)
        save_wav_file(filepath, sound_array)
        print(f"Generated: {filepath}")
    
    print("All sounds generated successfully!")

if __name__ == "__main__":
    main()
