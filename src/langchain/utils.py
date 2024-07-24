from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb.utils.embedding_functions as embedding_functions
import os
from langchain_openai import OpenAIEmbeddings


def load_document(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return docs

def split(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits

def get_embedding_function():
    return embedding_functions.create_langchain_embedding(OpenAIEmbeddings())
    
