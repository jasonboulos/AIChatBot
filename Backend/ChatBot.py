import logging
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openai

class ChatBot:
    logging.basicConfig(level=logging.INFO)
    DEFAULT_PROMPT = """
        Tu es un chatbot médical spécialisé en insuffisance cardiaque. Ton rôle est d'aider les patients à diagnostiquer leur état, fournir des informations, et donner des conseils personnalisés. 
        Si les informations fournies sont insuffisantes pour établir un diagnostic ou donner un conseil, pose des questions précises au patient pour recueillir plus de données.
        Réponds gentiment aux salutations ou questions simples (par exemple, "Bonjour", "Ça va"), mais ne réponds pas aux questions non liées à l'insuffisance cardiaque ou à son diagnostic. 
        Analyse les informations données pour prendre une décision adaptée et termine chaque réponse par "Merci pour votre question !"


        Contexte : {context} 
        Question : {question}
        Réponse :
    """

    SUMMARIZE_PROMPT = """
    Résume la question ci-dessous en un titre clair et concis de 2 à 3 mots, tout en capturant son essence principale.

    Question : {question}
    Titre : 
"""

    def __init__(self, vector_store, api_key, search_kwargs=3, temperature=0, prompt_template=None, model_name="gpt-3.5-turbo"):
        self.model_name = model_name
        self.vectorStore = vector_store
        self.api_key = api_key
        self.temperature = temperature
        self.search_kwargs = search_kwargs

        # Define retriever
        self.retriever = self.vectorStore.vectorDB.as_retriever(
            search_type="similarity", search_kwargs={"k": search_kwargs}
        )

        # Set up memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Define prompt
        self.prompt_template = prompt_template or self.DEFAULT_PROMPT
        self.logger = logging.getLogger("ChatBot")

        # Set up OpenAI API key
        openai.api_key = self.api_key

        # Initialize LLM and Chain
        try:
            # Initialize LLM
            self.llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)
            self.logger.info(f"LLM Model '{self.model_name}' successfully loaded.")

            # Create the conversational retrieval chain with memory
            custom_prompt = PromptTemplate(
                input_variables=["context", "question"],
                template=self.prompt_template
            )
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.retriever,
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": custom_prompt}
            )
            self.logger.info("Conversation Chain created successfully.")

            summarize_prompt_template = PromptTemplate(
            input_variables=["question"],
            template= self.SUMMARIZE_PROMPT
        )
            self.summarize_chain = LLMChain(llm=self.llm, prompt=summarize_prompt_template)
            self.logger.info("Summarized Chain created successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM Model '{self.model_name}': {e}")
    def summarize_question(self, question):
        try:
            summary = self.summarize_chain.run({"question": question})
            self.logger.info(f"Summarized question: {summary}")
            return summary.strip()
        except Exception as e:
            self.logger.error(f"Error summarizing question: {e}")
            return "Error summarizing question."
    def generate_response(self, question):
        if question:
            try:
                self.logger.info(f"Chat history: {self.memory.chat_memory.messages}")
                result = self.chain({"question": question})
                self.logger.info("Result generated successfully.")
                return result["answer"]
            except Exception as e:
                self.logger.error(f"Error processing question '{question}': {e}")
                return "An error occurred while processing your question. Please try again later."
        else:
            return "Please provide your question."


        
    def clear_history(self):
        self.memory.clear()  # Clears the conversation history
        self.logger.info("Chat history cleared.")
