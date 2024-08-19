# chat_utils.py
# File description: In this file the link is made with llama3. Create and receive the response corresponding to the received message

import ollama

def get_chat_response(messages, model='llama3'):
    """Primeste raspuns-ul de la chat bot"""
    try:
        # Apelam API-ul pentru a primi raspunsul
        response = ollama.chat(model=model, messages=messages)

        # Verificarea raspunsului pentru a se asigura ca contine datele asteptate
        if 'message' in response and 'content' in response['message']:
            reply = response['message']['content']
        else:
            reply = "A aparut o eroare la formarea raspunsului."

    except Exception as e:
        print(f"Debug: A aparut o eroare la primirea raspunsului: {e}")
        reply = "A aparut o eroare la primirea raspunsului."

    return reply
