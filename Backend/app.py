from ChatBot import ChatBot
from VectorStore import VectorStore
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]

class TitleResponse(BaseModel):
    question: str
    title: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
DB_directory = './chroma_db/'

vector_store = VectorStore(embeddingModel=OpenAIEmbeddings(),persist_directory=DB_directory)
vector_store.initializeVectorDB()
chatbot = ChatBot(vector_store = vector_store,api_key= OPENAI_API_KEY)

@app.get("/health")
def health_check():
    try:
        if chatbot:
            return {"status": "ok"}
        else:
            return {"status": "bot is not alive"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@app.post("/ask",response_model=AnswerResponse)
def ask_question(request : QuestionRequest):
    try:

        response = chatbot.generate_response(request.question)
        return AnswerResponse(question= request.question, answer=response["answer"],sources= response["sources"])
    except Exception as e:    
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.post("/summarize", response_model= TitleResponse)
def generate_title(request : QuestionRequest):
    try:
        title = chatbot.summarize_question(request.question)
        return TitleResponse(question=request.question, title=title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
