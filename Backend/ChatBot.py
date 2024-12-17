import logging
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
import openai
class ChatBot:
    logging.basicConfig(level=logging.INFO)
    DEFAULT_PROMPT = """
    En utilisant le contexte ci-dessous, réponds à la question suivante. Si tu ne connais pas la réponse, dis-le clairement et évite d'inventer des informations.Ajoute a la fin de la reponse "Merci pour votre question !"
    Contexte : {context} 
    Question : {question}
    Réponse :
"""


    def __init__(self, vector_store,api_key, search_kwargs = 3, temperature=0,promptTemplate = None, model_name = "gpt-3.5-turbo"):
        self.model_name = model_name
        self.vectorStore = vector_store
        self.api_key = api_key
        self.temperature = temperature
        self.search_kwargs = search_kwargs
        self.retriever = self.vectorStore.vectorDB.as_retriever(search_type="similarity", search_kwargs={"k": search_kwargs})
        self.promptTemplate = promptTemplate or self.DEFAULT_PROMPT
        self.logger = logging.getLogger("ChatBot")
        self.chat_history = []
        custom_prompt = PromptTemplate(
            input_variables=["context", "question"],  # Variables to populate in the prompt
            template=self.DEFAULT_PROMPT)
        try:
            openai.api_key = self.api_key
            self.llm = ChatOpenAI(model_name = self.model_name, temperature= self.temperature)
            self.logger.info(f"LLM Model '{self.model_name}' successfully loaded.")
            self.memory = ConversationBufferMemory(memory_key = "Chat_history",return_messages = True)
            # Ce que lui il a fait au debut, il faut changer aussi le self.chain dans generate response (enleve self.chat_history)
            # self.chain = ConversationalRetrievalChain.from_llm(self.llm, retriever = self.retriever, memory = self.memory)
            self.chain = ConversationalRetrievalChain.from_llm(self.llm, retriever = self.retriever, combine_docs_chain_kwargs = {"prompt" : custom_prompt})
            self.logger.info("chain creaeted successfully.")    
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM Model '{self.model_name}': {e}")

    def generate_response(self, question):
        if question:
            try:
                self.logger.info(f"Chat history before chain: {self.chat_history}")
                result = self.chain({"question": question, "chat_history": self.chat_history})
                self.chat_history.extend([(question, result["answer"])])
                self.logger.info("Result generated successfully")
                return result["answer"]
            except Exception as e:
                self.logger.error(f"Error processing question '{question}': {e}")
                return "An error occurred while processing your question. Please try again later."
        else:
            return "Please provide your question."
    
    def clear_history(self):
        self.chat_history.clear()
        return
       
