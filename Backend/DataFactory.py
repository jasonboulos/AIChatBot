from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
import whisper
from bs4 import BeautifulSoup
from langchain.schema import Document
import requests
import re
import os
import unicodedata


class DataFactory:

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("DataFactory")
    
    @staticmethod
    def collectDataFromWeb(urls):
        """
        Collects documents from a list of web URLs.
        :param urls: List of web page URLs.
        :return: List of documents.
        """
        documents = []

        for url in urls:
            try:
                loader = WebBaseLoader(url)
                docs = loader.load()
                documents.extend(docs)
                DataFactory.logger.info(f"Successfully loaded data from {url}")
            except Exception as e:
                DataFactory.logger.error(f"Error loading data from {url}: {e}")

        return documents
    
    @staticmethod
    def normalize_text(text):
        return unicodedata.normalize("NFKC", text)
    @staticmethod
    def clean_text(text):
        text = re.sub(r"´ e", "é", text)
        text = re.sub(r"` a", "à", text)
        text = re.sub(r"´ ee", "ée", text)
        text = re.sub(r"\s+", " ", text)  # Remove extra spaces
        return text
    @staticmethod
    def collectDataFromPdf(paths):
        """
        Collects documents from a list of PDF file paths.
        :param paths: List of paths to PDF files.
        :return: List of documents.
        """
        documents = []

        for path in paths:
            try:
                loader = PyPDFLoader(path)
                docs = loader.load()
                print(f"docs: {len(docs)}")
                normalized_docs = [
                    Document(
                        page_content=DataFactory.normalize_text(doc.page_content),
                        metadata=doc.metadata  # Preserve metadata
                    ) for doc in docs
                ]

                cleaned_docs = [
                    Document(
                        page_content=DataFactory.clean_text(doc.page_content),
                        metadata=doc.metadata  # Preserve metadata
                    ) for doc in normalized_docs
                ]
                documents.extend(cleaned_docs)
                DataFactory.logger.info(f"Successfully loaded data from {path}")
            except Exception as e:
                DataFactory.logger.error(f"Error loading data from {path}: {e}")

        return documents
    
    @staticmethod
    def collectDataFromYoutube(urls):
        model = whisper.load_model("base")
        save_dir = "videos"
        documents = []

        audio_loader = YoutubeAudioLoader(urls, save_dir)
        for blob in audio_loader.yield_blobs():
            try:
                DataFactory.logger.info(f"Transcription for {blob.path}")
                transcription = model.transcribe(str(blob.path))
                documents.extend(transcription["text"])
            except Exception as e:
                DataFactory.logger.error(f"Error loading data from {blob.path}: {e}")

        return documents
        


    @staticmethod
    def splitDocuments(docs, chunk_size, chunk_overlap):
        splits = []

        if(len(docs) > 0 and chunk_size > 0 and chunk_overlap >=0):
            text_splitter = RecursiveCharacterTextSplitter()
            splits = text_splitter.split_documents(docs)
            DataFactory.logger.info(f"Splits = {len(splits)}")
            
        return splits
      
    @staticmethod
    def get_all_pdf_paths(base_directory):
        """
        Retrieves all PDF file paths from a given base directory.
        :param base_directory: Base directory to search for PDFs.
        :return: List of all PDF file paths.
        """
        pdf_paths = []
        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if file.endswith(".pdf"):
                    pdf_paths.append(os.path.join(root, file))
        return pdf_paths
