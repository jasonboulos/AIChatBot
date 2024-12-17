from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer
import logging
<<<<<<< Updated upstream
import os
from dotenv import load_dotenv
from openai import OpenAI
class ChatBot:

    def __init__(self, vectorStore, model_name, tokenizerName,search_kwargs = 3, temperature=0.7, top_p=0.9, max_new_tokens=300):
        self.vectorStore = vectorStore
        self.modelName = model_name
        self.tokenizerName = tokenizerName
=======
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
import openai

<<<<<<< Updated upstream
DEFAULT_PROMPT = """
    En vous basant sur le contexte fourni ci-dessous, répondez à la question suivante avec précision. Si vous ne connaissez pas la réponse, indiquez-le clairement sans inventer d'informations.

    À la fin de votre réponse, ajoutez toujours :  
    "Merci pour votre question !".  

    Important : Ne vous adressez jamais à votre interlocuteur avec "tu", utilisez toujours "vous".  

    Contexte : {context}  
    Question : {question}  
    Réponse :
"""

class ChatBot:

    logging.basicConfig(level=logging.INFO)

    def __init__(self, vector_store, api_key, search_kwargs = 3, temperature=0,promptTemplate = None, model_name = "gpt-3.5-turbo"):
=======
class ChatBot:

    logging.basicConfig(level=logging.INFO)

    DEFAULT_PROMPT = """
        En utilisant le contexte ci-dessous, réponds à la question suivante. Si tu ne connais pas la réponse, dis-le clairement et évite d'inventer des informations. Ajoute à la fin de la rèponse et dans un nouvel paragraphe en sautant deux lignes "Merci pour votre question !".
        Contexte : {context} 
        Question : {question}
        Réponse :
    """

    def __init__(self, vector_store,api_key, search_kwargs = 3, temperature=0, promptTemplate = None, model_name = "gpt-3.5-turbo"):
>>>>>>> Stashed changes
        self.model_name = model_name
        self.vectorStore = vector_store
        self.api_key = api_key
>>>>>>> Stashed changes
        self.temperature = temperature
        self.top_p = top_p
        self.max_new_tokens = max_new_tokens
        self.search_kwargs = search_kwargs
        self.retriever = self.vectorStore.vectorDB.as_retriever(search_type="similarity", search_kwargs={"k": search_kwargs})
<<<<<<< Updated upstream
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("ChatBot")

        try:
            # Initialize LLM and tokenizer
            self.hf_pipeline = pipeline(
                "text-generation",
                model=self.modelName,
                tokenizer=self.tokenizerName,
                temperature=self.temperature,
                top_p=self.top_p,
                repetition_penalty=1.2,
                max_new_tokens=self.max_new_tokens,
                do_sample=True,
                device=0
            )
            self.llm = HuggingFacePipeline(pipeline=self.hf_pipeline)
         
            self.logger.info(f"LLM Model '{self.modelName}' successfully loaded.")
=======
        self.promptTemplate = promptTemplate or DEFAULT_PROMPT
        self.logger = logging.getLogger("ChatBot")
        self.chat_history = []
        custom_prompt = PromptTemplate(
            input_variables=["context", "question"],  # Variables to populate in the prompt
            template=DEFAULT_PROMPT
        )
        try:
            openai.api_key = self.api_key

            self.llm = ChatOpenAI(
                model_name = self.model_name, 
                temperature = self.temperature
            )

            self.logger.info(f"LLM Model '{self.model_name}' successfully loaded.")
<<<<<<< Updated upstream
            # self.memory = ConversationBufferMemory(memory_key = "Chat_history",return_messages = True)
            self.chain = ConversationalRetrievalChain.from_llm(self.llm, chain_type = "stuff", retriever = self.retriever, combine_docs_chain_kwargs = {"prompt" : custom_prompt})
            self.logger.info("chain creaeted successfully.")    
>>>>>>> Stashed changes
=======
            
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )

            # Ce que lui il a fait au debut, il faut changer aussi le self.chain dans generate response (enleve self.chat_history)
            self.chain = ConversationalRetrievalChain.from_llm(
                self.llm, 
                retriever = self.retriever, 
                memory = self.memory,
                combine_docs_chain_kwargs = {"prompt" : custom_prompt}
            )

            #self.chain = ConversationalRetrievalChain.from_llm(self.llm, retriever = self.retriever, combine_docs_chain_kwargs = {"prompt" : custom_prompt})
            self.logger.info("chain creaeted successfully.")  

>>>>>>> Stashed changes
        except Exception as e:
            self.logger.error(f"Failed to load LLM Model '{self.modelName}': {e}")

    def generate_response(self, question):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        try:
            # Retrieve relevant documents
            retrieved_docs = self.retriever.invoke(question)
            if not retrieved_docs:
                self.logger.info(f"No relevant documents found for question: {question}")
                return "I'm sorry, I couldn't find relevant information for your question."

            # Combine context
            context = "\n\n".join([doc.page_content.strip() for doc in retrieved_docs])
            self.logger.info(f"Retrieved documents: {len(retrieved_docs)}")

            # Format input text
            input_text = f"""
            Context: {context}

            Task: En se basant sur le context fourni, repond la question si dessous.
            

            Question: {question}

            Answer:
            """
            self.logger.info(f"Question: {question}")
            tokens = self.hf_pipeline.tokenizer(input_text, return_tensors="pt")["input_ids"]
            self.logger.info(f"Token count: {len(tokens[0])}")

            response = self.llm.invoke(input_text)
            if response:
                self.logger.info(f"Generated response successfully")
                return response
            else:
                self.logger.warning("Generated an empty response.")
                return "I'm sorry, I couldn't generate a response for your question."

        except Exception as e:
            self.logger.error(f"Error processing question '{question}': {e}")
            return "An error occurred while processing your question. Please try again later."
=======
        if question:
            try:
                result = self.chain({"question": question, "chat_history": self.chat_history})
                self.chat_history.extend([(question, result["answer"])])
                self.logger.info(self.chat_history)
=======
        if question != '':
            try:
                if ("précédente" or "precedente" or "précèdente") in question.lower():
                    chat_history = self.memory.chat_memory.messages
                    last_question = None
                    for message in reversed(chat_history):
                        if message.type == "human":
                            last_question = message.content
                            break
                    if last_question != None:
                        response = {"answer": f"Votre question précédente était : '{last_question}'"}
                    else:
                        response = {"answer": "Je suis désolé mais vous ne m'avez posé aucune question précédemment. Merci pour votre question !"}
                else:
                    # Sinon, traiter normalement avec chain.invoke
                    result = self.chain.invoke({"question": question})
                    response = result
                self.logger.info(f"Chat history before chain: {self.chat_history}")
                #result = self.chain({"question": question, "chat_history": self.chat_history})
                #result = self.chain({"question": question})
                #self.chat_history.extend([(question, result["answer"])])
>>>>>>> Stashed changes
                self.logger.info("Result generated successfully")
                return response["answer"]
            except Exception as e:
                self.logger.error(f"Error processing question '{question}': {e}")
                return "An error occurred while processing your question. Please try again later."
        else:
<<<<<<< Updated upstream
            return "Please provide your question."
    
    def clear_history(self):
        self.chat_history.clear()
        return
>>>>>>> Stashed changes
=======
            return "Veuillez poser une question s'il vous plaît. Merci !"
       
>>>>>>> Stashed changes
