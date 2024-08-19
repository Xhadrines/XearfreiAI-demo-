# main.py
# File description: This file is the main application, from here the application starts

import os

# Importa modulele din directorul utils
from utils.ui_utils import Window

def list_files_and_directories(root_dir, blacklist):
    dir_structure = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude directoarele din lista neagra
        dirnames[:] = [d for d in dirnames if d not in blacklist]

        # Calea relativa a directorului curent fata de directorul de baza
        rel_dirpath = os.path.relpath(dirpath, root_dir)
        abs_dirpath = dirpath  # Calea completa a directorului curent

        if rel_dirpath == '.':
            current_level = dir_structure
        else:
            parts = rel_dirpath.split(os.sep)
            current_level = dir_structure
            for part in parts:
                current_level = current_level.setdefault(part, {})

        # Adaugati fisierele in dictionar cu calea completa
        for filename in filenames:
            full_path = os.path.join(abs_dirpath, filename)
            current_level[filename] = full_path

    return dir_structure

def print_structure(d, indent=0):
    for key, value in d.items():
        if isinstance(value, dict):
            if value:  # Daca dictionary-ul nu este gol
                print_structure(value, indent + 2)
        else:
            print(' ' * indent + f"{key} - {value}")

def main():
    # Definitia listei negre a directoare
    blacklist = [
        'venv',
        '__pycache__',
        'unused',
    ]

    # Obtine calea absoluta a directorului de baza
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Listeaza fisierele si directoarele, excluzand directoarele din lista neagra
    dir_structure = list_files_and_directories(base_dir, blacklist)

    # print_structure(dir_structure)

    # Creeaza si ruleaza fereastra GUI
    window = Window(dir_structure)
    window.run()

if __name__ == "__main__":
    main()
