import os

# Dictionarul dat
data = {
    'cod.txt': 'D:\\Documents\\Practica\\XearfreiAI\\cod.txt',
    'main.py': 'D:\\Documents\\Practica\\XearfreiAI\\main.py',
    'requirements.txt': 'D:\\Documents\\Practica\\XearfreiAI\\requirements.txt',
    'audio': {
        'ai_audio': {},
        'other': {
            'beep.mp3': 'D:\\Documents\\Practica\\XearfreiAI\\audio\\other\\beep.mp3'
        },
        'user_audio': {}
    },
    'images': {
        'background.png': 'D:\\Documents\\Practica\\XearfreiAI\\images\\background.png',
        'close.png': 'D:\\Documents\\Practica\\XearfreiAI\\images\\close.png',
        'mic_off.png': 'D:\\Documents\\Practica\\XearfreiAI\\images\\mic_off.png',
        'mic_on.png': 'D:\\Documents\\Practica\\XearfreiAI\\images\\mic_on.png',
        'options.png': 'D:\\Documents\\Practica\\XearfreiAI\\images\\options.png',
        'return.png': 'D:\\Documents\\Practica\\XearfreiAI\\images\\return.png',
        'send.png': 'D:\\Documents\\Practica\\XearfreiAI\\images\\send.png',
        'sound_off.png': 'D:\\Documents\\Practica\\XearfreiAI\\images\\sound_off.png',
        'sound_on.png': 'D:\\Documents\\Practica\\XearfreiAI\\images\\sound_on.png'
    },
    'utils': {
        'audio_utils.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\audio_utils.py',
        'chat_utils.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\chat_utils.py',
        'file_utils.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\file_utils.py',
        'search_utils.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\search_utils.py',
        'speech_utils.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\speech_utils.py',
        'ui_utils.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\ui_utils.py',
        'other': {
            'cod.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\other\\cod.py',
            'main(old)-v1.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\other\\main(old)-v1.py',
            'main(old)-v2.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\other\\main(old)-v2.py',
            'rag-local.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\other\\rag-local.py',
            'rag-online.py': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\other\\rag-online.py',
            'requirements(old).txt': 'D:\\Documents\\Practica\\XearfreiAI\\utils\\other\\requirements(old).txt'
        }
    }
}

# Functie recursiva pentru a gasi toate caile fisierelor .py
def extract_python_files(data, py_files=[]):
    for key, value in data.items():
        if isinstance(value, dict):
            extract_python_files(value, py_files)
        elif isinstance(value, str) and value.endswith('.py'):
            py_files.append(value)
    return py_files

# Extragem caile fisierelor .py
python_files = extract_python_files(data)

# Initializam o variabila pentru a stoca continutul fisierelor
file_contents = ""

# Citim continutul fisierelor si il adaugam la variabila
for file_path in python_files:
    try:
        print(f"Deschid fisierul: {file_path}")  # Debugging
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"Continutul citit din {file_path}: {content[:100]}...")  # Afisam primele 100 de caractere pentru debugging
            file_contents += content + "\n"  # Adaugam un nou rand pentru a separa continutul fisierelor
    except Exception as e:
        print(f"Nu am putut citi fisierul {file_path}: {e}")

# Acum, file_contents contine tot continutul fisierelor .py
print("Tot continutul fisierelor a fost citit.")
print(f"Primele 500 de caractere din file_contents: {file_contents[:500]}...")
