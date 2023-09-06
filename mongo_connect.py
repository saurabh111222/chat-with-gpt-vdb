from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import streamlit as st
from utils.vdb_connections import generate_unique_uuid
from dotenv import load_dotenv
load_dotenv()

def get_mongo_client():
    uri = f"mongodb+srv://saurabhkumariitism:{os.environ.get('MONGO_PASSWORD')}@clusterchatwithgpt.zdnep97.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    return MongoClient(uri, server_api=ServerApi('1'))


def load_customer_chat_history_on_UI():
    client = get_mongo_client()
    test_db = client.data
    collection = test_db.test_coll
    found_docs = collection.find({'user_id': 123})
    for doc in found_docs:
        st.session_state["chat_answers_history"].append(doc['query'])
        st.session_state["user_prompt_history"].append(doc['response'])
    # Send a ping to confirm a successful connection
    # try:
    #     client.admin.command('ping')
    #     test_db = client.data
    #     collection = test_db.test_coll
    #     test_dic = {'uuid': f'{generate_unique_uuid()}', 'query': f'{query}','response': f'{response}'}
    #     inserted = collection.insert_one(test_dic)
    #     print("Pinged your deployment. You successfully connected to MongoDB!")
    # except Exception as e:
    #     print(e)