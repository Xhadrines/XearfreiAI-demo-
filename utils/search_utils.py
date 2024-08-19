# search_utils.py
# File description: This file contains all the functions for searching/opening a page on the Internet

import requests
import webbrowser
import re
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

# Configurare API Key si Custom Search Engine ID
API_KEY = 'AIzaSyBOBnEb1CtwI3LzPOzKwWRLyWQungB0yhE'
SEARCH_ENGINE_ID = 'd59a9390bdc894819'

def google_search(query):
    """Cautare pe Google si returnarea rezumat"""
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()
    results = []
    for item in res.get('items', []):
        title = item.get('title')
        snippet = item.get('snippet')
        results.append(f"{title}: {snippet}")

    return results

def open_search(query):
    """Deschide browser-ul cu cautarea specifica"""
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)

def open_wikipedia(query):
    """Deschide browser-ul cu cautarea specifica pe Wikipedia"""
    search_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    webbrowser.open(search_url)

def clean_text(text):
    """Elimina referintele de tip [numar] din text"""
    pattern = re.compile(r'\[\d+\]')
    return pattern.sub('', text)

def wikipedia_search(query):
    """Cautare pe Wikipedia si returnarea continutului"""
    # URL-ul pe care vrei sa il deschizi
    search_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    
    # Deschide cu metoda GET 
    resp = requests.get(search_url)

    # Daca raspunsul HTTP este 200, inseamna ca statusul este OK 
    if resp.status_code == 200:
        print("S-a deschis cu succes pagina web.")
        print("Pagina contine:\n")

        soup = BeautifulSoup(resp.text, 'html.parser')

        # Gaseste toate elementele <p>
        paragraphs = soup.find_all("p")

        # Filtrarea paragrafelor goale si pastrarea celor non-goale
        non_empty_paragraphs = [p for p in paragraphs if p.get_text(strip=True)]

        # Verifica daca exista paragrafe non-goale
        if non_empty_paragraphs:
            # Parcurge toate elementele <p> si afiseaza textul curatat al fiecaruia
            for p in non_empty_paragraphs:
                # Curata textul de referinte
                cleaned_text = clean_text(p.get_text())
                print(cleaned_text)
        else:
            print("Nu sau gasit elemente de paragraf nevide")
    else:
        print("Error")
