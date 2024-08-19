import os
import sys
import time
from gtts import gTTS

# Specifica directorul de baza si directorul de module utils
base_dir = os.path.dirname(os.path.abspath(__file__)) # Calea catre directorul XearfreiAI
utils_dir = os.path.join(base_dir, "utils")
sys.path.append(utils_dir)

# Importa modulele din directorul utils
from file_utils import delete_file
from audio_utils import play_beep, record_audio, play_audio
from speech_utils import transcribe_audio_to_text, listen_for_keyword
from chat_utils import get_chat_response
from search_utils import google_search, open_search, open_wikipedia, wikipedia_search

# Defineste directorul principal pentru salvarea fisierelor audio
audio_dir = "audio"

# Defineste subdirectoarele pentru salvarea fisierelor audioS
user_audio_dir = os.path.join(audio_dir, "user_audio")
ai_audio_dir = os.path.join(audio_dir, "ai_audio")

# Creeaza directoarele daca nu exista
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(user_audio_dir, exist_ok=True)
os.makedirs(ai_audio_dir, exist_ok=True)

# Defineste fisierele audio
ai_audio_file = os.path.join(ai_audio_dir, "response.mp3")
user_audio_file = os.path.join(user_audio_dir, "question.mp3")

# Defineste modul de utilizare
keyboard_only = True

# pygame.mixer.init()

messages = [
    {
        'role': 'system',
        # 'content': 'you limit your responses to 20 words and you only speak Romanian'
        'content': 'you only talk like khajiit girl name xearfrei from the elder scrolls, and you limit your responses to 20 words'
    }
]

def main():
    print("Bine ai venit! Spune 'Xhadrines', 'Alexa' sau 'AI' pentru a incepe o intrebare vocala. Scrie 'bye' sau 'goodbye' pentru a iesi.")

    while True:
        delete_file(ai_audio_file)
        delete_file(user_audio_file)

        if keyboard_only:
            user_message = input("Tu: ")
        else:
            keyword_detected = False
            while not keyword_detected:
                keyword = listen_for_keyword()

                if keyword in ['xhadrines', 'alexa', 'ai']:
                    keyword_detected = True
                    play_beep()
                    record_audio(user_audio_file, duration=5)

                    if os.path.isfile(user_audio_file):
                        print(f"Debug: Fisierul {user_audio_file} a fost creat cu succes.")
                    else:
                        print(f"Debug: Fisierul {user_audio_file} nu a fost creat.")

                    user_message = transcribe_audio_to_text(user_audio_file)
                    print(f"Tu: {user_message}")

        if user_message.lower() in ['bye', 'goodbye']:
            reply = "See you later."

            print("AI: " + reply)

            tts = gTTS(text=reply, lang='en')
            tts.save(ai_audio_file)
            play_audio(ai_audio_file)
            delete_file(ai_audio_file)

            time.sleep(0.5)
            break
        
        words = user_message.lower().split()

        # Procesarea comenzilor speciale
        if words[0] == "search":
            if words[1] == "wikipedia":
                query = user_message[len("search wikipedia"):].strip()
                results = wikipedia_search(query)
                reply = "Here are the top results: " # + ", ".join(results)
            else:
                query = user_message[len("search"):].strip()
                results = google_search(query)
                reply = "Here are the top results: " + ", ".join(results)
        elif words[0] == "open":
            if words[1] == "search":
                search_query = user_message[len("open search "):]
                open_search(search_query)
                reply = "I opened the page."
            elif words[1] == "wikipedia":
                wiki_query = user_message[len("open wikipedia "):]
                open_wikipedia(wiki_query)
                reply = "I opened the page."
        else:
            messages.append({
                'role': 'user',
                'content': user_message
            })

            reply = get_chat_response(messages)

        print("AI: " + reply)

        tts = gTTS(text=reply, lang='en')
        tts.save(ai_audio_file)
        play_audio(ai_audio_file)

        time.sleep(0.5)

        messages.append({
            'role': 'assistant',
            'content': reply
        })

if __name__ == "__main__":
    main()