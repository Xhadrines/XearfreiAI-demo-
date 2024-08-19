import ollama
import requests
import re
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def clean_text(text):
    """Elimina referintele de tip [numar] din text"""
    pattern = re.compile(r'\[\d+\]')
    return pattern.sub('', text)

def wikipedia_search(query):
    """Cautare pe Wikipedia si returnarea continutului"""
    # URL-ul pe care vrei sa il deschizi
    search_url = f"https://ro.wikipedia.org/wiki/{query.replace(' ', '_')}"
    
    # Deschide cu metoda GET 
    resp = requests.get(search_url)
    
    # Daca raspunsul HTTP este 200, inseamna ca statusul este OK 
    if resp.status_code == 200:
        print("S-a deschis cu succes pagina web.")
        # print("Pagina contine:\n")
     
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Gaseste toate elementele <p>
        paragraphs = soup.find_all("p")
        
        # Filtrarea paragrafelor goale si pastrarea celor non-goale
        non_empty_paragraphs = [p for p in paragraphs if p.get_text(strip=True)]
        
        # Verifica daca exista paragrafe non-goale
        if non_empty_paragraphs:
            # Concatenate all cleaned text from paragraphs
            full_text = "\n".join(clean_text(p.get_text()) for p in non_empty_paragraphs)
            return full_text
        else:
            print("Nu s-au gasit elemente de paragraf nevide")
            return ""
    else:
        print("Error")
        return ""

# Fetch and process Wikipedia content
content = wikipedia_search("Stefan cel Mare")

if content:
    # Create a document object
    docs = [Document(metadata={'source': "https://ro.wikipedia.org/wiki/Stefan cel Mare"}, page_content=content)]

    # Debug: Print loaded document content
    print(f"Loaded document content: {docs[0].page_content[:1000]}")  # Print first 1000 characters for inspection

    # Split the documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Debug: Print document splits
    print(f"Document splits: {splits}")

    # Check if splits is not empty
    if not splits:
        raise ValueError("No document splits found. Please check the document loader and text splitter.")

    # Create Ollama embeddings and vector store
    embeddings = OllamaEmbeddings(model="llama3")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

    # Call Ollama Llama3 model
    def ollama_llm(question, context):
        formatted_prompt = f"Question: {question}\n\nContext: {context}"
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': formatted_prompt}])
        return response['message']['content']

    # RAG Setup
    retriever = vectorstore.as_retriever()
    def combine_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    def rag_chain(question):
        retriever_docs = retriever.invoke(question)
        formatted_context = combine_docs(retriever_docs)
        return ollama_llm(question, formatted_context)

    # Use the RAG App
    result = rag_chain("Cine a fost Stefan cel Mare?")
    print(result)
else:
    print("Failed to fetch or process Wikipedia content.")
