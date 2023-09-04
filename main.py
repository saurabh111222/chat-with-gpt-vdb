from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message
from llm_models.core import run_llm
import uuid


load_dotenv()
st.header("ChatWithGPT")
option = st.selectbox(
    'Select Subject',
    ('Current affairs', 'Bill passed'))

def generate_unique_uuid():
    return str(uuid.uuid4())

prompt = st.text_input("Prompt", placeholder="Enter your query here...",  key='widget')



if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


if prompt:
    with st.spinner('Processing query...'):
        SUBJECT = option.replace(' ', '_')
        print(f'Select option: {option} and subject: {SUBJECT}')
        generated_response, similarity_score = run_llm(QUERY=prompt, SUBJECT=SUBJECT, CHAT_HISTORY=st.session_state['chat_history'])
        # print(generated_response)
        formated_response = F"{generated_response['answer']} \n\n Similarity score: {similarity_score}"

        # print(st.session_state)
        # print(st.session_state['chat_history'])
        st.session_state["chat_answers_history"].append(formated_response)
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_history"].append((prompt, generated_response["answer"]))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"], 
        st.session_state["user_prompt_history"]):
        # message(user_query, is_user=True)
        message(generated_response, key=f'{generate_unique_uuid()}')

