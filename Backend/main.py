from ChatBot import ChatBot
from VectorStore import VectorStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv, find_dotenv
from DataFactory import DataFactory

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

pdf_base_directory = './docs/droits/'
DB_directory = './chroma_db'
pdfpaths = DataFactory.get_all_pdf_paths(pdf_base_directory)

vector_store = VectorStore(
    embeddingModel=OpenAIEmbeddings(),
    persist_directory= DB_directory,
    reset_db=True,pdfpaths= pdfpaths
)

vector_store.initializeVectorDB()

print(vector_store.vectorDB._collection.count())

chatbot = ChatBot(
 vector_store=vector_store,
    api_key= OPENAI_API_KEY
)

while True:
    question = input("Your question: ")
    if question.lower() == 'exit':
        print("Exiting the program. Goodbye!")
        break

    #Generate response
    try:
        result = chatbot.generate_response(question)
        print(f"Answer: {result}\n")
        title = chatbot.summarize_question(question)
        print(f"Title : {title}")
        # Optional: Print source documents for debugging
    except Exception as e:
        print(f"Error: {e}\n")



