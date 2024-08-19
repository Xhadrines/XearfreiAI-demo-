# ui_utils.py
# File description: In this file is everything that means the interface, and which links all the other files and puts them inside the single interface to work

import tkinter as tk
from gtts import gTTS
import os

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Importa functiile din modulele existente
from utils.file_utils import delete_file, read_python_files_from_dict, write_to_file, read_file
from utils.audio_utils import play_beep, record_audio, play_audio
from utils.speech_utils import transcribe_audio_to_text, listen_for_keyword
from utils.chat_utils import get_chat_response
from utils.search_utils import google_search, open_search, open_wikipedia, wikipedia_search

class Window:
    def __init__(self, dir_structure, width=800, height=450):
        # Creeaza instanta ferestrei principale
        self.root = tk.Tk()
        self.root.title("XearfreiAI")
        self.root.attributes('-topmost', True)  # Fereastra principala deasupra altor aplicatii

        # Variabila pentru a stoca referinta la fereastra de optiuni
        self.options_window = None

        # Elimina bara de titlu si butoanele de control
        self.root.overrideredirect(True)

        # Seteaza dimensiunea ferestrei
        self.width = width
        self.height = height
        self.root.geometry(f"{self.width}x{self.height}")

        # Seteaza culoarea de fundal pentru intreaga fereastra
        self.bg_color = "#EAEAEA"
        self.root.configure(bg=self.bg_color)

        # Centreaza fereastra pe ecran
        self.center_window()

        # Creeaza frame-uri pentru organizare
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(self.root, bg=self.bg_color)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Defineste directorul cu imagini
        self.images_dir = os.path.join(os.path.dirname(__file__), '..', 'images')

        # Adauga elemente in fereastra
        self.add_widgets()

        # Defineste directoarele pentru salvarea fisierelor audio
        self.audio_dir = "audio"
        self.user_audio_dir = os.path.join(self.audio_dir, "user_audio")
        self.ai_audio_dir = os.path.join(self.audio_dir, "ai_audio")
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.user_audio_dir, exist_ok=True)
        os.makedirs(self.ai_audio_dir, exist_ok=True)
        self.ai_audio_file = os.path.join(self.ai_audio_dir, "response.mp3")
        self.user_audio_file = os.path.join(self.user_audio_dir, "question.mp3")

        # Defineste directoarele pentru salvarea fisierelor temp
        self.temp_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')
        os.makedirs(self.temp_dir, exist_ok=True)

        self.messages = [
            {
                'role': 'system',
                'content': ''
            }
        ]

        # Initializeaza variabila de stare pentru sunet si mic
        self.sound_enabled = False
        self.mic_enabled = False

        self.keyword_detected = False

        self.dir_structure = dir_structure

        # print(dir_structure)

    def center_window(self):
        # Obtine dimensiunea ecranului
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculeaza coordonatele pentru a centra fereastra
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        # Seteaza pozitia ferestrei
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def add_widgets(self):
        # Creeaza un frame pentru partea de sus
        top_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Creeaza un frame pentru stanga si dreapta partii de sus
        left_frame = tk.Frame(top_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        right_frame = tk.Frame(top_frame, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Creeaza un Label pentru textul "XearfreiAI"
        title_label = tk.Label(top_frame, text="XearfreiAI", font=("Arial", 30, "bold"), bg=self.bg_color, fg="#000000")
        title_label.pack(side=tk.LEFT, expand=True)  # Expandeaza label-ul pentru a fi centrat intre frame-urile stang si drept

        # Asociaza evenimentele de mouse pentru mutarea ferestrei
        title_label.bind("<Button-1>", self.start_move)
        title_label.bind("<B1-Motion>", self.do_move)

        # Incarca imaginea pentru butonul de optiuni
        options_image_path = os.path.join(self.images_dir, "options.png")  # Asigura-te ca ai o imagine "options.png" in directorul "images"
        options_image = tk.PhotoImage(file=options_image_path)

        # Creeaza un buton de optiuni cu imagine
        options_button = tk.Button(left_frame, image=options_image, command=self.open_options_window, bg=self.bg_color, bd=0, highlightthickness=0)
        options_button.image = options_image  # Salveaza referinta pentru a preveni colectarea gunoiului
        options_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Incarca imaginea pentru butonul de inchidere
        close_image_path = os.path.join(self.images_dir, "close.png")
        close_image = tk.PhotoImage(file=close_image_path)

        # Creeaza un buton de inchidere cu imagine
        close_button = tk.Button(right_frame, image=close_image, command=self.root.destroy, bg=self.bg_color, bd=0, highlightthickness=0)
        close_button.image = close_image  # Salveaza referinta pentru a preveni colectarea gunoiului
        close_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Creeaza un frame pentru zona de mesaj
        message_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        message_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Creeaza un widget Text pentru a afisa mesajele
        self.message_display = tk.Text(message_frame, height=10, font=("Arial", 12), state=tk.DISABLED, bg="#FFFFFF", fg="#000000")
        self.message_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Incarca imaginea pentru butonul Send
        send_image_path = os.path.join(self.images_dir, "send.png")
        send_image = tk.PhotoImage(file=send_image_path)

        # Creeaza un buton "Send" cu imagine
        send_button = tk.Button(self.bottom_frame, image=send_image, command=self.send_action, bg=self.bg_color, bd=0, highlightthickness=0)
        send_button.image = send_image  # Salveaza referinta pentru a preveni colectarea gunoiului
        send_button.grid(row=0, column=1, padx=10, pady=10)

        # Creeaza o caseta de text (Text) si le adauga in bara de jos
        self.text_entry = tk.Text(self.bottom_frame, height=2, font=("Arial", 14), bg="#FFFFFF", fg="#000000")  # Folosind `Text` pentru dimensiune mai mare
        self.text_entry.grid(row=0, column=0, sticky="ew", padx=(10, 0), pady=10)

        self.text_entry.bind("<Return>", lambda event: self.send_action())

        # Configureaza coloana pentru a se extinde
        self.bottom_frame.grid_columnconfigure(0, weight=1)

    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self.start_x
        y = self.root.winfo_y() + event.y - self.start_y
        self.root.geometry(f"+{x}+{y}")

    def open_options_window(self):
        if hasattr(self, 'options_window') and self.options_window is not None and self.options_window.winfo_exists():
            self.options_window.destroy()
            self.options_window = None
            return

        self.options_window = tk.Toplevel(self.root)
        self.options_window.attributes('-topmost', True)
        self.options_window.title("Options")

        # Elimina bara de titlu si butoanele de control
        self.options_window.overrideredirect(True)

        # Seteaza dimensiunea ferestrei de optiuni
        window_width = 200
        window_height = 70
        self.options_window.geometry(f"{window_width}x{window_height}")

        # Seteaza culoarea de fundal
        self.options_window.configure(bg=self.bg_color)

        # Centreaza fereastra de optiuni pe fereastra principala
        main_x = self.root.winfo_rootx()
        main_y = self.root.winfo_rooty()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        x = main_x + (main_width - window_width) // 2
        y = main_y + (main_height - window_height) // 2
        self.options_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Creeaza un frame pentru butoane
        button_frame = tk.Frame(self.options_window, bg=self.bg_color)
        button_frame.pack(pady=10, padx=10, fill=tk.X)

        # Incarca imaginile pentru butoane
        sound_on_image = tk.PhotoImage(file=os.path.join(self.images_dir, "sound_on.png"))
        sound_off_image = tk.PhotoImage(file=os.path.join(self.images_dir, "sound_off.png"))
        mic_on_image = tk.PhotoImage(file=os.path.join(self.images_dir, "mic_on.png"))
        mic_off_image = tk.PhotoImage(file=os.path.join(self.images_dir, "mic_off.png"))
        return_image = tk.PhotoImage(file=os.path.join(self.images_dir, "return.png"))

        # Creeaza butonul de sunet
        sound_button = tk.Button(button_frame, image=sound_on_image if self.sound_enabled else sound_off_image, bg=self.bg_color, bd=0, highlightthickness=0,
                                 command=lambda: self.toggle_sound(sound_button, sound_on_image, sound_off_image))
        sound_button.pack(side=tk.LEFT, padx=(0, 10))

        # Creeaza butonul de microfon
        mic_button = tk.Button(button_frame, image=mic_on_image if self.mic_enabled else mic_off_image, bg=self.bg_color, bd=0, highlightthickness=0,
                               command=lambda: self.toggle_mic(mic_button, mic_on_image, mic_off_image))
        mic_button.pack(side=tk.LEFT, padx=(0, 10))

        # Creeaza butonul de inchidere
        return_button = tk.Button(button_frame, image=return_image, bg=self.bg_color, bd=0, highlightthickness=0,
                                  command=self.close_options_window)
        return_button.pack(side=tk.LEFT)

        sound_button.image = sound_on_image if self.sound_enabled else sound_off_image
        mic_button.image = mic_on_image if self.mic_enabled else mic_off_image
        return_button.image = return_image

    def toggle_button_image(self, button, img_on, img_off, state_var):
        current_image = button.cget("image")
        if current_image == str(img_on):
            button.config(image=img_off)
            button.image = img_off
            state_var.set(False)
        else:
            button.config(image=img_on)
            button.image = img_on
            state_var.set(True)

    def toggle_sound(self, button, img_on, img_off):
        self.toggle_button_image(button, img_on, img_off, tk.BooleanVar(value=self.sound_enabled))
        self.sound_enabled = not self.sound_enabled

    def toggle_mic(self, button, img_on, img_off):
        self.toggle_button_image(button, img_on, img_off, tk.BooleanVar(value=self.mic_enabled))
        self.mic_enabled = not self.mic_enabled

        if self.mic_enabled:
            self.text_entry.config(state=tk.DISABLED)
            self.start_keyword_detection()
        else:
            self.text_entry.config(state=tk.NORMAL)
            self.keyword_detected = True

    def start_keyword_detection(self):
        self.keyword_detected = False
        self.root.after(100, self.detect_keyword)

    def detect_keyword(self):
        if not self.keyword_detected:
            keyword = listen_for_keyword()
            
            if keyword in ['xhadrines', 'alexa', 'ai']:
                self.keyword_detected = True
                play_beep()
                record_audio(self.user_audio_file, duration=5)

                if os.path.isfile(self.user_audio_file):
                    print(f"Debug: Fisierul {self.user_audio_file} a fost creat cu succes.")
                else:
                    print(f"Debug: Fisierul {self.user_audio_file} nu a fost creat.")

                user_message = transcribe_audio_to_text(self.user_audio_file)
                # print(f"Tu: {user_message}")
                self.display_message("Tu", user_message)
                delete_file(self.user_audio_file)
                self.generate_reply(user_message)
            else:
                self.root.after(100, self.detect_keyword)  # Verifica din nou dupa 100ms
    
    def display_message(self, sender, message):
        self.message_display.config(state=tk.NORMAL)  # Permite editarea temporara pentru a adauga text
        self.message_display.insert(tk.END, f"{sender}: {message}\n")  # Afiseaza mesajul
        self.message_display.config(state=tk.DISABLED)  # Revine la starea de citire
        self.message_display.yview(tk.END)  # Deruleaza la sfarsit pentru a afisa mesajul nou

    def close_options_window(self):
        self.options_window.destroy()
        self.options_window = None

    def send_action(self):
        user_message = self.text_entry.get("1.0", tk.END).strip()  # Obtine textul din caseta de text
        if user_message:
            self.display_message("Tu", user_message)  # Afiseaza mesajul in widgetul de mesaje
            self.text_entry.delete("1.0", tk.END)  # Sterge textul din caseta de text
            self.root.after(100, self.generate_reply, user_message)  # Genereaza raspunsul dupa o scurta intarziere

    def generate_reply(self, user_message):
        # Functie pentru a genera raspunsul AI si a afisa mesajul
        reply = self.process_message(user_message)

        # Afiseaza raspunsul in caseta de mesaje
        self.message_display.config(state=tk.NORMAL)
        self.message_display.insert(tk.END, "AI: " + reply + "\n")
        self.message_display.config(state=tk.DISABLED)
        self.message_display.yview(tk.END)  # Deruleaza la sfarsit pentru a afisa mesajul nou

        # Salveaza raspunsul ca fisier audio si reda-l dupa ce mesajul este afisat
        self.root.after(500, self.save_and_play_audio, reply)  # Introduce o intarziere de 500 ms inainte de a reda audio-ul

    def process_message(self, message):
        words = message.lower().split()

        # Procesarea comenzilor speciale
        if words[0] == "search":
            if words[1] == "wikipedia":
                query = message[len("search wikipedia"):].strip()
                results = wikipedia_search(query)
                reply = "Here are the top results: " # + ", ".join(results)
            else:
                query = message[len("search"):].strip()
                results = google_search(query)
                reply = "Here are the top results: " + ", ".join(results)
        elif words[0] == "open":
            if words[1] == "search":
                search_query = message[len("open search "):]
                open_search(search_query)
                reply = "I opened the page."
            elif words[1] == "wikipedia":
                wiki_query = message[len("open wikipedia "):]
                open_wikipedia(wiki_query)
                reply = "I opened the page."
        elif words[0] == "update":
            # Path-ul catre fisierul de text
            file_path = os.path.join(self.temp_dir, 'ia_cod.txt')

            # Citim continutul fisierelor .py din structura dir_structure
            content = read_python_files_from_dict(self.dir_structure)
            
            # Scriem continutul in fisierul ia_cod.txt
            write_to_file(file_path, content)
            
            print(f"Debug: Continutul fisierelor .py a fost actualizat in {file_path}")

            def load_text_from_file(file_path):
                """Incarca textul dintr-un fisier si returneaza continutul curat"""
                return read_file(file_path)

            # Incarca si proceseaza continutul din fisier
            content = load_text_from_file(file_path)

            if content:
                # Creaza un obiect document
                docs = [Document(metadata={'source': file_path}, page_content=content)]

                # Debug: Afiseaza continutul documentului incarcat
                # print(f"Loaded document content: {docs[0].page_content}")

                # Imparte documentele
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                splits = text_splitter.split_documents(docs)

                # Debug: Afiseaza impartirile documentului
                # print(f"Document splits: {splits}")

                # Verifica daca splits nu este gol
                if not splits:
                    raise ValueError("Debug: Documentul este gol, nu sa putut da splits")

                # Creaza embeddings Ollama si vector store
                embeddings = OllamaEmbeddings(model="llama3")
                vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

                # Functie pentru apelarea modelului Ollama Llama3
                def ollama_llm(question, context):
                    formatted_prompt = f"Question: {question}\n\nContext: {context}"
                    response = get_chat_response(messages=[{'role': 'user', 'content': formatted_prompt}], model='llama3')
                    return response

                # Configurare RAG
                retriever = vectorstore.as_retriever()
                def combine_docs(docs):
                    return "\n\n".join(doc.page_content for doc in docs)
                def rag_chain(question):
                    retriever_docs = retriever.invoke(question)
                    formatted_context = combine_docs(retriever_docs)
                    return ollama_llm(question, formatted_context)

                # Foloseste aplicatia RAG
                reply = rag_chain("I want you to come up with new features based on my code")

                self.messages.append({
                    'role': 'assistant',
                    'content': reply
                })
                delete_file(file_path)
            else:
                print("Debug: Nu sa putut incarca si procesa documentul")
        else:
            self.messages.append({
                'role': 'user',
                'content': message
            })

            reply = get_chat_response(self.messages)

            self.messages.append({
                'role': 'assistant',
                'content': reply
            })

        return reply

    def save_and_play_audio(self, reply):
        if not self.sound_enabled:
            return  # Nu reda audio daca sunetul este dezactivat
        
        tts = gTTS(text=reply, lang='en')
        tts.save(self.ai_audio_file)
        play_audio(self.ai_audio_file)
        delete_file(self.ai_audio_file)

    def run(self):
        # Ruleaza bucla principala a ferestrei
        self.root.mainloop()
