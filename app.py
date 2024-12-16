from ChatBot import ChatBot
from VectorStore import VectorStore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question:str
    answer: str

app = FastAPI()
DB_directory = './docs/chroma_db/'

vector_store = VectorStore(embeddingModel=OpenAIEmbeddings(),persist_directory=DB_directory)
vector_store.initializeVectorDB()
chatbot = ChatBot(vector_store = vector_store,api_key= OPENAI_API_KEY)

app.get("/")
def health_check():
    try:
        if chatbot:
            return {"status": "ok"}
        else:
            return {"status": "bot is not alive"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

app.post("/ask",response_model=AnswerResponse)
def ask_question(request : QuestionRequest):
    try:

        answer = chatbot.generate_response(request.question)
        return AnswerResponse(question= request.question, answer=answer)
    except Exception as e:    
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

