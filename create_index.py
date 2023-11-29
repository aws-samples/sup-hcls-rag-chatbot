__import__('pysqlite3')
import os
import json
from langchain.embeddings import BedrockEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import JSONLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.llms.bedrock import Bedrock
from langchain.vectorstores import Chroma
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from chromadb.config import Settings

CHROMA_SETTINGS = Settings(
    chroma_db_impl='duckdb+parquet',
    persist_directory="./db",
    anonymized_telemetry=False
)

def get_index(): #creates and returns an in-memory vector store to be used in the application
    
    credentials_profile_name = "ENTER CREDENTIAL PROFILE, if not the default" #sets the profile name to use for AWS credentials (if not the default)
    region_name = "ENTER REGION" #sets the region name (if not the default)
    endpoint_url = "https://bedrock-runtime.us-west-2.amazonaws.com" #sets the Bedrock endpoint.  If not using us-west-2 region, adjust this to the correct region

    embeddings = BedrockEmbeddings(
        credentials_profile_name=credentials_profile_name,
        region_name=region_name, 
        endpoint_url=endpoint_url,
        model_id="amazon.titan-embed-text-v1"
    ) #create a Titan Embeddings client
    
    text_splitter = RecursiveCharacterTextSplitter( #create a text splitter
        separators=["\n\n", "\n", ".", " "], #split chunks at (1) paragraph, (2) line, (3) sentence, or (4) word, in that order
        chunk_size=1000, #divide into 1000-character chunks using the separators above
        chunk_overlap=100 #number of characters that can overlap with previous chunk
    )

    ### Load multiple documents within a directory
    documents = []
    for file in os.listdir('./docs/'):
        if file.endswith('.pdf'):
            pdf_path = './docs/' + file
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
            print("Loaded document " + str(file) + " into list.")
        elif file.endswith('.docx') or file.endswith('.doc'):
            doc_path = './docs/' + file
            loader = Docx2txtLoader(doc_path)
            documents.extend(loader.load())
            print("Loaded document " + str(file) + " into list.")
        elif file.endswith('.txt'):
            text_path = './docs/' + file
            loader = TextLoader(text_path)
            documents.extend(loader.load())
            print("Loaded document " + str(file) + " into list.")
        elif file.endswith('.json'):
            text_path = './docs/' + file
            loader = JSONLoader(file_path=text_path, jq_schema='.[]', text_content=False)
            documents.extend(loader.load())
            print("Loaded document " + str(file) + " into list.")
        elif file.endswith('.csv'):
            text_path = './docs/' + file
            loader = CSVLoader(text_path)
            documents.extend(loader.load())
            print("Loaded document " + str(file) + " into list.")

    documents = text_splitter.split_documents(documents)
    
    vectordb = Chroma.from_documents(documents, embedding=embeddings, persist_directory="./db")
    vectordb.persist()

    vectordb = VectorStoreIndexWrapper(vectorstore=vectordb)
    return vectordb
    
get_index()
print("Indexing complete.  Vectordb is available in the ./db directory.")