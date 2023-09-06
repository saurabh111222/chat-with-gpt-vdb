from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message
from llm_models.core import run_llm
from utils.vdb_connections import generate_unique_uuid
from mongo_connect import get_mongo_client, load_customer_chat_history_on_UI
load_dotenv()
import time

client = get_mongo_client()
#Setting header
st.header("ChatWithGPT")

#Taking subject
option = st.selectbox(
    'Select Subject',
    ('Current affairs', 'Bill passed'))

#Taking prompt query
with st.form(key='my_form'):
	prompt = st.text_input("Prompt", placeholder="Enter your query here...",  key='widget')
	submit_button = st.form_submit_button(label='Submit')
     
# prompt = st.text_input("Prompt", placeholder="Enter your query here...",  key='widget')


if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

load_customer_chat_history_on_UI()


if prompt:
    with st.spinner('Processing query...'):        
        SUBJECT = option.replace(' ', '_')
        print(f'Select option: {option} and subject: {SUBJECT}')
        generated_response, similarity_score, cb = run_llm(QUERY=prompt, SUBJECT=SUBJECT, CHAT_HISTORY=st.session_state['chat_history'])
        if "don't know" not in generated_response['answer']:
           formated_response = F"{generated_response['answer']} \n\n Similarity score: {similarity_score} \n\n Total token: {cb.total_tokens} \n Total cost (USD): ${cb.total_cost}"
        else:
            formated_response=generated_response['answer']
        st.session_state["chat_answers_history"].append(formated_response)
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_history"].append((prompt, generated_response["answer"]))
        try:
            client.admin.command('ping')
            print("You successfully connected to MongoDB!")
            test_db = client.data
            collection = test_db.test_coll
            test_dic = {'uuid': f'{generate_unique_uuid()}', 'user_id': 123, 'query': f'{prompt}','response': f'{generated_response["answer"]}'}
            inserted = collection.insert_one(test_dic)
            print('Inserted the data into mongo', inserted)
        except Exception as e:
          print(e)

if st.session_state["chat_answers_history"]:
    for gen_response, user_query in zip(
        st.session_state["chat_answers_history"], 
        st.session_state["user_prompt_history"]):
        message(user_query, key=f'{generate_unique_uuid()}', is_user=True)
        message(gen_response, key=f'{generate_unique_uuid()}')

