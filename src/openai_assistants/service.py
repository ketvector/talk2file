from openai import OpenAI

from argparse import ArgumentParser
from dotenv import load_dotenv
import json

from .openai_assistants_agent import OpenAIAssistantsAgent
from .openai_assistants_store import OpenAIAssistantsStore

load_dotenv(override=True)
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