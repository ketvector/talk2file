from langchain_chroma import Chroma
from .chroma_store import ChromaStore
from .utils import get_embedding_function
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI


class LangchainAgent():
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    def query(self, questions, store_ids):
        persistent_client = ChromaStore(host="localhost", port=8001, id = store_ids[0])
        langchain_chroma = Chroma(
                client=persistent_client.store,
                collection_name=store_ids[0],
                embedding_function=get_embedding_function(),
            )
        retriever = langchain_chroma.as_retriever()
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", system_prompt),
                        ("human", "{input}"),
                    ]
                )
        print("XXXXXXXXXXXXXXXX")
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        results = rag_chain.invoke({"input": questions[0]})
        return results