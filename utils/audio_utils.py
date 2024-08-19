# audio_utils.py
# File description: In this file it deals with the sounds used start/audio recording

import os
import pygame
import pyaudio
import wave

def play_beep():
    """Scoate un sunet beep"""
    # Defineste directorul principal pentru salvarea fisierelor audio
    audio_dir = "audio"

    # Defineste subdirectoarele pentru salvarea fisierelor audio
    other = os.path.join(audio_dir, "other")

    # Defineste fisierele audio
    beep_file = os.path.join(other, "beep.mp3")

    # Initializeaza pygame mixer and si porneste sunetul
    pygame.mixer.init()
    pygame.mixer.music.load(beep_file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

def record_audio(filename, duration=5):
    """Inregistreaza sunetul de la microfon si salveaza"""
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    p = pyaudio.PyAudio()

    try:
        # Deschide audio stream
        stream = p.open(format=sample_format, channels=channels, rate=rate, 
                        frames_per_buffer=chunk, input=True)
        frames = []

        print("Debug: Se inregistreaza...")
        for _ in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)
        print("Debug: Sa terminat de inregistrat.")

    except Exception as e:
        print(f"Debug: A aparut o eroare in timpul inregistrarii: {e}")

    finally:
        # Opreste si inchide stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Salveaza inregostrarea ca fisier
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(p.get_sample_size(sample_format))
                wf.setframerate(rate)
                wf.writeframes(b''.join(frames))
        except Exception as e:
            print(f"Debug: A aparut o eroare in timp ce se salva inregistrarea: {e}")

def play_audio(filename):
    """Porneste sunetul"""
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Debug: A aparut o eroare in timp ce pornea sunetul: {e}")
