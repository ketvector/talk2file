from openai import OpenAI

from argparse import ArgumentParser
from dotenv import load_dotenv
import json

from service import get_agent, get_store, query


load_dotenv(override=True)
client = OpenAI()

agent_id = "asst_UqhROUNxEWCZkek8g0X4xzYM"
store_id = "vs_B9g5Lhfiw3oDzck1otR2Whro"
questions = [
    "What is the name of the company?",
    "Who is the CEO of the company?",
    "What is their vacation policy?",
    "What is the termination policy?"
]

if __name__ == "__main__":
    agent = get_agent(client, agent_id)
    store = get_store(client, store_id)
    answer = query(agent, [store], questions)
    print(json.dumps(answer, indent=4))






