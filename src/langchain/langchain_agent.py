from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import os

from .chroma_store import ChromaStore
from .utils import get_embedding_function, format_docs



class LangchainAgent():
    def __init__(self):
        LANGCHAIN_OPEN_AI_MODEL = os.environ["LANGCHAIN_OPEN_AI_MODEL"]
        self.llm = ChatOpenAI(model=LANGCHAIN_OPEN_AI_MODEL)

    
    def query(self, questions, store_ids):
        persistent_client = ChromaStore.get_from_id(store_ids[0])
        langchain_chroma = Chroma(
                client=persistent_client.store,
                collection_name=store_ids[0],
                embedding_function=get_embedding_function(),
            )
        
        retriever = langchain_chroma.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        
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
        
        rag_chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        results = []
        for question in questions:
            result = rag_chain.invoke(question)
            print(result)
            results.append(
                {
                    "question" : question,
                    "answer": result
                }
            )
        return {
            "responses" : results
        }