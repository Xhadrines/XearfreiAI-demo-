from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

from chat_utils import get_chat_response
from file_utils import read_file

def load_text_from_file(file_path):
    """Incarca textul dintr-un fisier si returneaza continutul curat"""
    return read_file(file_path)

def main():
    # Path-ul catre fisierul de text
    file_path = 'cod.txt'  # Inlocuieste cu calea reala catre fisierul tau

    # Incarca si proceseaza continutul din fisier
    content = load_text_from_file(file_path)

    if content:
        # Creaza un obiect document
        docs = [Document(metadata={'source': file_path}, page_content=content)]

        # Debug: Afiseaza continutul documentului incarcat
        print(f"Loaded document content: {docs[0].page_content}")

        # Imparte documentele
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # Debug: Afiseaza impartirile documentului
        print(f"Document splits: {splits}")

        # Verifica daca splits nu este gol
        if not splits:
            raise ValueError("No document splits found. Please check the document loader and text splitter.")

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
        result = rag_chain("I want you to come up with new features and implement them in the provided code.")
        print("\n\nAI:\n\n")
        print(result)
    else:
        print("Failed to load or process file content.")

if __name__ == "__main__":
    main()
