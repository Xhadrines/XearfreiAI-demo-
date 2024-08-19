# file_utils.py
# File description: In this file are all the functions that are used for file manipulation

import os
import time

def delete_file(filename):
    """Sterge fisierul daca exista"""
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"Debug: Fisierul {filename} a fost sters cu succes.")
        except PermissionError:
            print(f"Debug: Nu am permisiunea de a sterge fisierul {filename}. Voi incerca din nou.")
            time.sleep(0.5)
            delete_file(filename)
        except Exception as e:
            print(f"Debug: A aparut o eroare la stergerea fisierului {filename}: {e}")
    else:
        print(f"Debug: Fisierul {filename} nu exista.")

def read_file(filename):
    """Citeste din fisier"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Debug: A aparut o eroare la citirea fisierului {filename}: {e}"
    else:
        return f"Debug: Fisierul {filename} nu exista."

def write_to_file(filename, content):
    """Scriere in fisier"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Debug: Continutul a fost scris in fisierul {filename}.")
    except Exception as e:
        print(f"Debug: A aparut o eroare la scrierea in fisierul {filename}: {e}")

def append_to_file(filename, content):
    """Suprascrierea fisierelor"""
    try:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(content + '\n')
        print(f"Debug: Continutul a fost suprascris in fisierul {filename}.")
    except Exception as e:
        print(f"Debug: A aparut o eroare la suprascrierea fisierului {filename}: {e}")

def extract_python_files(data, py_files=[]):
    """Extrage toate caile fisierelor .py dintr-un dictionar"""
    for key, value in data.items():
        if isinstance(value, dict):
            extract_python_files(value, py_files)
        elif isinstance(value, str) and value.endswith('.py'):
            py_files.append(value)
    return py_files

def read_python_files_from_dict(data):
    """Citeste continutul fisierelor .py dintr-un dictionar"""
    python_files = extract_python_files(data)
    file_contents = ""

    for file_path in python_files:
        try:
            print(f"Debug: Deschid fisierul: {file_path}")  # Debugging
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # print(f"Continutul citit din {file_path}: {content[:100]}...")
                file_contents += f"\nAnother file from {file_path}\n" + content
        except Exception as e:
            print(f"Debug: Nu am putut citi fisierul {file_path}: {e}")

    return file_contents
