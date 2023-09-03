from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message
from llm_models.core import run_llm

load_dotenv()
st.header("ChatWithGPT")
option = st.selectbox(
    'Select Subject',
    ('Current affairs', 'Bill passed'))
SUBJECT = option.replace(' ', '_')
print(f'Select option: {option} and subject: {SUBJECT}')

prompt = st.text_input("Prompt", placeholder="Enter your query here...")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


if prompt:
    with st.spinner('Processing query...'):
        generated_response = run_llm(QUERY=prompt, CHAT_HISTORY=st.session_state['chat_history'])

        st.session_state["chat_answers_history"].append(generated_response)
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_history"].append((prompt, generated_response["answer"]))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"], 
        st.session_state["user_prompt_history"]):
        message(user_query, is_user=True)
        message(generated_response)

        