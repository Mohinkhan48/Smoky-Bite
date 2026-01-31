import wave
import struct
import math

# Simple "Ding" sound generation
def generate_ding(filename):
    sample_rate = 44100
    duration = 0.5  # seconds
    frequency = 880.0  # A5 note
    
    # Create the wave file
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)  # Mono
        f.setsampwidth(2)  # 2 bytes per sample
        f.setframerate(sample_rate)
        
        for i in range(int(duration * sample_rate)):
            # Taper the volume to make it a "ding"
            volume = 0.5 * (1.0 - i / (duration * sample_rate))
            value = int(volume * 32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            data = struct.pack('<h', value)
            f.writeframesraw(data)

import os
os.makedirs('static/audio', exist_ok=True)
generate_ding('static/audio/notify.mp3') # Using .mp3 extension for convenience, though it's technically a pcm wav
print("Generated notify.mp3 (WAV format internally)")
