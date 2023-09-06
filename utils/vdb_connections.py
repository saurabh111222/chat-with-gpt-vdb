import os
from dotenv import load_dotenv
import uuid
load_dotenv()

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, TextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import streamlit as st
from langchain.vectorstores import Weaviate
import weaviate


def generate_unique_uuid():
    return str(uuid.uuid4())

def get_client():
    client = weaviate.Client(url=os.environ.get("WEAVIATE_URL"), 
                         auth_client_secret=weaviate.AuthApiKey(os.environ.get("WEAVIATE_API_KEY")), 
                         additional_headers = {
                                "X-OpenAI-Api-Key": f"{os.environ.get('OPENAI_API_KEY')}"  # Replace with your inference API key
                    }                   
                    )
    return client


def get_schema(class_name:str):
    class_obj = {
            "class": f"{class_name}",
            "description": "An Author class to store the author information",
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "The actual content", 
                },
                {
                    "name": "metadata",
                    "dataType": ["text"],
                    "description": "metadata about the content", 
                }
            ],
            "vectorizer": "text2vec-openai"
        }

    return class_obj

if __name__ == "__main__":
    print('config')