from openai_assistants_agent import OpenAIAssistantsAgent
from openai_assistants_store import OpenAIAssistantsStore


def get_agent(client, id):
    return OpenAIAssistantsAgent(client, id)

def create_agent(client, name):
    return OpenAIAssistantsAgent(client, None, name)

def get_store(client, id):
    return OpenAIAssistantsStore(client, id)

def create_store(client, name):
    return OpenAIAssistantsStore(client, None, name)

def query(agent, stores, questions):
    return agent.query(questions , [store.get_id() for store in stores])