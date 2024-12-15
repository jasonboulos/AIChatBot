from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer
import logging
import os
from dotenv import load_dotenv
from openai import OpenAI
class ChatBot:

    def __init__(self, vectorStore, model_name, tokenizerName,search_kwargs = 3, temperature=0.7, top_p=0.9, max_new_tokens=300):
        self.vectorStore = vectorStore
        self.modelName = model_name
        self.tokenizerName = tokenizerName
        self.temperature = temperature
        self.top_p = top_p
        self.max_new_tokens = max_new_tokens
        self.search_kwargs = search_kwargs
        self.retriever = self.vectorStore.vectorDB.as_retriever(search_type="similarity", search_kwargs={"k": search_kwargs})
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
        except Exception as e:
            self.logger.error(f"Failed to load LLM Model '{self.modelName}': {e}")

    def generate_response(self, question):
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
