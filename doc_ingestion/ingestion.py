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

# weaviate client
client = get_client()


def ingest_doc(PATH: str, SUBJECT: str) -> None:
    loader = PyPDFLoader(PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    texts = text_splitter.split_documents(documents=documents)
    print(f"Splitted into {len(texts)} chunks.")

    class_obj = get_schema(class_name=SUBJECT)
    embedding = OpenAIEmbeddings()
    # client.schema.delete_all()

    if client.schema.exists(SUBJECT):
        print(f"Data for class {SUBJECT} already exists")
        # print(f"Class {SUBJECT} already exists")
        print(client.schema.get())
        # vector_store = Weaviate(client, SUBJECT, 'content', embedding=embedding)

    else:
        print(f"Class object {SUBJECT} does not exist.\n Creating {SUBJECT}...")
        client.schema.create_class(class_obj)
        print(client.schema.get())

        print("Inititing document insert...")
        text_meta_pair = [(doc.page_content, doc.metadata) for doc in texts]
        texts, meta = list(zip(*text_meta_pair))
        Weaviate.from_texts(
            texts, embedding, metadatas=meta, client=client, by_text=False
        )
        print(f"Inserted {len(texts)} documents into db.")


if __name__ == "__main__":
    print("Initiating doc insertion...")
