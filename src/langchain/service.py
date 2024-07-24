from .chroma_store import ChromaStore
from .langchain_agent import LangchainAgent

def add_file_to_store(store_id, file_path):
    store = ChromaStore.get_from_id(store_id)
    store.add([file_path])

def query(store_ids, questions):
    agent = LangchainAgent()
    return agent.query(questions , store_ids)