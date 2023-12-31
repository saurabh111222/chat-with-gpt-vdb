import os
from dotenv import load_dotenv
load_dotenv()

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TextSplitter,
)
from langchain.embeddings.openai import OpenAIEmbeddings
from utils.vdb_connections import get_client, get_schema
from langchain.vectorstores import Weaviate
import weaviate


# weaviate client
client = get_client()


def ingest_doc(QUERY:str, SUBJECT: str):

    PATH = (
        r"E:\Langchain Tutorial\local-vector-store\current_affairs_iasbaba.pdf"
        if SUBJECT == "Current_affairs"
        else r"C:\Users\LENOVO\Downloads\bill_passed.pdf"
    )

    loader = PyPDFLoader(PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=30, separator="\n")
    texts = text_splitter.split_documents(documents=documents)
    print(f"Splitted into {len(texts)} chunks.")

    class_obj = get_schema(class_name=SUBJECT)
    print(class_obj)
    embedding = OpenAIEmbeddings()

    if client.schema.exists(SUBJECT):
        print(f"Data for class {SUBJECT} already exists")
        # vectorstore = Weaviate(client, f"{SUBJECT}", "content", attributes=["source"], embedding=embedding)

    else:
        print(f"Class object {SUBJECT} does not exist.\n Creating {SUBJECT}...")
        client.schema.create_class(class_obj)

        print("Inititing document insert...")
        text_meta_pair = [(doc.page_content, doc.metadata) for doc in texts]
        texts, meta = list(zip(*text_meta_pair))
        # Weaviate.from_texts(
        #     texts, embedding, metadatas=meta, client=client, by_text=False
        # )
        vectorstore = Weaviate(client, f"{SUBJECT}", "content", attributes=["source"], embedding=embedding)
        vectorstore.add_texts(texts, meta)
        print(f"Inserted {len(texts)} documents into db.")
    
    # doc = vectorstore.similarity_search_with_score(query=QUERY, by_text=False)
    # similarity_score = doc[0][1]
    # print(f"Splitted into {len(texts)} chunks.")
    # return similarity_score

        


if __name__ == "__main__":
    print("Initiating ingestion config...")
    ingest_doc(QUERY="Tell me about Japan-India Maritime Exercise 2023", SUBJECT = "Current_affairs")