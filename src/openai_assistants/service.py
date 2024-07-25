from openai import OpenAI

from .openai_assistants_agent import OpenAIAssistantsAgent
from .openai_assistants_store import OpenAIAssistantsStore


client = OpenAI()

def get_agent(id):
    return OpenAIAssistantsAgent(client, id)

def create_agent(name):
    return OpenAIAssistantsAgent(client, None, name)

def get_store(id):
    return OpenAIAssistantsStore(client, id)

def create_store(name):
    return OpenAIAssistantsStore(client, None, name)

def query(agent_id, store_ids, questions):
    agent = OpenAIAssistantsAgent(client=client, id=agent_id)
    return agent.query(questions , store_ids)

def add_file_to_store(store_id, file_path):
    store = get_store(store_id)
    store.add(file_paths=[file_path])