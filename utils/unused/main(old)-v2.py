import os

# Importa modulele din directorul utils
from utils.ui_utils import Window

def list_files_and_directories(root_dir, blacklist):
    # Creati un dictionar pentru a stoca ierarhia directoarelor si fisierelor
    dir_structure = {}

    # Populati dictionarul cu ierarhia directoarelor si fisierelor
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude directoarele din lista neagra pe baza numelui
        dirnames[:] = [d for d in dirnames if d not in blacklist]

        # Calea relativa a directorului curent fata de directorul de baza
        rel_dirpath = os.path.relpath(dirpath, root_dir)

        # Adaugati directoare si fisiere in dictionar
        if rel_dirpath == '.':
            current_level = dir_structure
        else:
            # Navigati la nivelul corespunzator din dictionar
            parts = rel_dirpath.split(os.sep)
            current_level = dir_structure
            for part in parts:
                current_level = current_level.setdefault(part, {})

        # Adaugati fisierele in dictionar
        for filename in filenames:
            current_level[filename] = None

    # Functie pentru a afisa ierarhia
    def print_structure(d, indent=0):
        for key, value in d.items():
            if isinstance(value, dict):
                print(' ' * indent + f"Director: {key}")
                print_structure(value, indent + 2)
            else:
                print(' ' * indent + f"Fisier: {key}")

    # Afisati structura, incepand de la directorul de baza
    print(f"Director: {os.path.basename(root_dir)}")
    print_structure(dir_structure, indent=2)

def main():
    # Definitia listei negre a directoare
    blacklist = [
        'venv',
        '__pycache__',
    ]

    # Obtine calea absoluta a directorului de baza
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Listeaza fisierele si directoarele, excluzand directoarele din lista neagra
    list_files_and_directories(base_dir, blacklist)

    # Creeaza si ruleaza fereastra GUI
    window = Window()
    window.run()

if __name__ == "__main__":
    main()