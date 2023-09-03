import os
from dotenv import load_dotenv

load_dotenv()

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Weaviate
from doc_ingestion.ingestion import ingest_doc
from utils.vdb_connections import get_client


def run_llm(QUERY: str, SUBJECT: str, CHAT_HISTORY: list((str, any)) = []) -> any:
    # Ingest docuements
    PATH = (
        r"E:\Langchain Tutorial\local-vector-store\current_affairs_iasbaba.pdf"
        if SUBJECT == "Current_affairs"
        else r"C:\Users\LENOVO\Downloads\bill_passed.pdf"
    )
    ingest_doc(PATH=PATH, SUBJECT=SUBJECT)

    # Retriving the vector store
    client = get_client()
    embeddings = OpenAIEmbeddings()
    vector_store = Weaviate(client, SUBJECT, "content", embedding=embeddings)

    llm = ChatOpenAI(temperature=0.2, verbose=True)
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vector_store.as_retriever(), return_source_documents=True
    )

    return qa({"question": QUERY, "chat_history": CHAT_HISTORY})


if __name__ == "__main__":
    print("Initiating llm config...")
