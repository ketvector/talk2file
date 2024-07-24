import chromadb
from .utils import load_document, split, get_embedding_function
import os

class ChromaStore():
    @staticmethod
    def get_from_id(id):
        chroma_host = os.environ["LANGCHAIN_CHROMA_HOST"]
        chroma_port = os.environ["LANGCHAIN_CHROMA_PORT"]
        store = ChromaStore(chroma_host, chroma_port, id)
        return store
    
    def __init__(self, host, port, id):
        self.store = chromadb.HttpClient(host=host, port=port)
        self.collection = self.store.get_or_create_collection(name=id, embedding_function=get_embedding_function())
    
    def add(self, file_paths):
        docs = []
        for file_path in file_paths:
            docs = docs + load_document(file_path)
        splits = split(docs)
        cr_docs = [splt.page_content for splt in splits]
        cr_metas = [splt.metadata for splt in splits]
        cr_ids = [str(idx) for idx in range(len(splits))]
        self.collection.add(documents=cr_docs, metadatas=cr_metas, ids=cr_ids)
    
    def peek(self):
        return self.collection.peek()
    
