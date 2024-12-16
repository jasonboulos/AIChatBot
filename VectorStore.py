import os
import shutil
from langchain_community.llms import HuggingFacePipeline
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import logging
from DataFactory import DataFactory

class VectorStore:
    logging.basicConfig(level=logging.INFO)

    def __init__(self, embeddingModel, persist_directory, urls=None, pdfpaths=None, chunk_size = 500,chunk_overlap = 75,reset_db=False):
        self.docs = []
        self.newDocs = []
        self.embeddingModel = embeddingModel
        self.persist_directory = persist_directory
        self.splits = None
        self.logger = logging.getLogger("VectorStore")
        self.vectorDB = None
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if reset_db:
            self.resetDatabase()

        if urls or pdfpaths:
            self.collectData(urls, pdfpaths)

        

    def resetDatabase(self):
        """
        Deletes the existing Chroma database directory.
        """
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            self.logger.info(f"Resetting Chroma database by deleting directory: {self.persist_directory}")

    def collectData(self, urls=None, pdfpaths=None):
        """
        Collect data from URLs and PDF paths and store it in self.docs and self.newDocs.
        """
        if urls:
            valid_urls = [url for url in urls if url.strip()]
            webdocsdata = DataFactory.collectDataFromWeb(valid_urls)
            self.docs.extend(webdocsdata)
            self.newDocs.extend(webdocsdata)

        if pdfpaths:
            valid_pdfPaths = [path for path in pdfpaths if path.strip()]
            pdfdocsdata = DataFactory.collectDataFromPdf(valid_pdfPaths)
            self.docs.extend(pdfdocsdata)
            if not self.docs:
                raise ValueError("No docs generated from the documents.")
            self.newDocs.extend(pdfdocsdata)

    def initializeVectorDB(self):
        """
        Initialize the vector database. Load the existing database if it exists,
        otherwise create a new one with current documents.
        """
        # Check if the Chroma database already exists
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            self.logger.info("Loading existing Chroma database...")
            self.vectorDB = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddingModel)
            if self.newDocs:
                self.saveData()
        else:
            self.logger.info("Creating a new Chroma database...")
            self.splits = DataFactory.splitDocuments(self.docs, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            if not self.splits:
                raise ValueError("No splits generated from the documents.")          
            self.vectorDB = Chroma.from_documents(self.splits, self.embeddingModel, persist_directory=self.persist_directory)
            self.newDocs = []

    def saveData(self):
        """
        Add new documents to the vector database.
        """
        new_splits = DataFactory.splitDocuments(self.newDocs, chunk_size=800, chunk_overlap=150)
        self.splits.extend(new_splits)
        if self.vectorDB:
            self.vectorDB.add_documents(new_splits)
        else:
            self.vectorDB = Chroma.from_documents(new_splits, self.embeddingModel, persist_directory=self.persist_directory)
        self.newDocs = []

    def getCurrentDocuments(self):
        return self.docs


