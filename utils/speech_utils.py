# speech_utils.py
# File description: This file deals with the transformation of speech into words

import os
import whisper
import speech_recognition as sr

# Incarcarea modelului Whisper o singura data
whisper_model = whisper.load_model("base")

def transcribe_audio_to_text(audio_file):
    """Transcrie fisierul audio la text"""
    absolute_path = os.path.abspath(audio_file)
    print(f"Debug: Calea fisierului este {absolute_path}")

    if not os.path.isfile(audio_file):
        print(f"Debug: Fisierul {audio_file} nu exista.")
        return "Debug: Fisierul specificat nu a fost gasit."

    # Verifica permisiunile fisierului
    if not os.access(audio_file, os.R_OK):
        print(f"Debug: Fisierul {audio_file} nu poate fi citit.")
        return "Debug: Fisierul nu poate fi citit."

    # Verifica dimensiunea fisierului
    file_size = os.path.getsize(audio_file)
    print(f"Debug: Dimensiunea fisierului este {file_size} bytes")

    # Verifica daca fisierul poate fi deschis si citit manual
    try:
        with open(audio_file, 'rb') as f:
            audio_data = f.read()
        print("Debug: Fisierul audio a fost citit cu succes")
    except Exception as e:
        print(f"Debug: A aparut o eroare la citirea fisierului audio: {e}")
        return "Debug: Eroare la citirea fisierului audio."

    try:
        # Transcriere folosind optiunile de decodare
        audio = whisper.load_audio(audio_file)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)
        options = whisper.DecodingOptions(language='en', fp16=False)
        result = whisper.decode(whisper_model, mel, options)
        return result.text
    except Exception as e:
        print(f"Debug: A aparut o eroare la transcriere: {e}")
        return "Debug: Transcriere esuata."

def listen_for_keyword(timeout=5):
    """Asculta cuvintele cheie"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Debug: Ascult cuvantul cheie...")
        try:
            audio = recognizer.listen(source, timeout=timeout)
            keyword = recognizer.recognize_google(audio, language='en-EN').lower()
            return keyword
        except sr.UnknownValueError:
            print("Debug: Nu am inteles cuvantul.")
            return ""
        except sr.RequestError as e:
            print(f"Debug: Nu am putut cere rezultatele: {e}")
            return ""
        except Exception as e:
            print(f"Debug: A aparut o eroare: {e}")
            return ""
