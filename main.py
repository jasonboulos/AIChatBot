from ChatBot import ChatBot
from VectorStore import VectorStore
from DataFactory import DataFactory

pdf_base_directory = './docs/pdfData/HAS/'
DB_directory = './chroma_db'
pdfpaths = DataFactory.get_all_pdf_paths(pdf_base_directory)

vector_store = VectorStore(
    embeddingModelName="distiluse-base-multilingual-cased-v1",
    persist_directory= DB_directory,
    pdfpaths=["./docs/pdfData/HAS/Insuffisance_Cardiaque_Has.pdf","./docs/pdfData/HAS/insufcard.pdf"],
    reset_db=True
)

vector_store.initializeVectorDB()


print(vector_store.vectorDB._collection.count())

chatbot = ChatBot(
    vectorStore=vector_store,
    model_name="bigscience/bloom-560m",
    tokenizerName="bigscience/bloom-560m",
    search_kwargs=2
)
while True:
        question = input("Your question: ")
        
        if question.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break

        # Process the question (you can replace this with actual logic to handle questions)
        response = chatbot.generate_response(question)
        print(f"Answer: {response}\n")




