import wave
import struct
import math
import os

def generate_ding(filename):
    try:
        sample_rate = 44100
        duration = 0.5
        frequency = 880.0
        with wave.open(filename, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            for i in range(int(duration * sample_rate)):
                volume = 0.5 * (1.0 - i / (duration * sample_rate))
                value = int(volume * 32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
                data = struct.pack('<h', value)
                f.writeframesraw(data)
        print(f"File {filename} created successfully.")
    except Exception as e:
        print(f"Error creating {filename}: {e}")

BASE_DIR = r'c:\Users\User\OneDrive\Documents\Smoky Bites'
audio_dir = os.path.join(BASE_DIR, 'static', 'audio')
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir, exist_ok=True)
    print(f"Created directory: {audio_dir}")
else:
    print(f"Directory already exists: {audio_dir}")

generate_ding(os.path.join(audio_dir, 'notify.wav'))
# Also create a .mp3 named copy just in case, even if it's wav content
generate_ding(os.path.join(audio_dir, 'notify.mp3'))
