import os
from dotenv import load_dotenv
load_dotenv()

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.vectorstores import Weaviate
from doc_ingestion.ingestion import ingest_doc
from utils.vdb_connections import get_client
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback



def run_llm(QUERY: str, SUBJECT: str, CHAT_HISTORY: list((str, any)) = []) -> any:
    #insert documents
    # ingest_doc(QUERY=QUERY, SUBJECT=SUBJECT)

    client = get_client()
    #Calculating similarity score
    vectorstore = Weaviate(client, f"{SUBJECT}", "content", attributes=["source"], embedding=OpenAIEmbeddings())
    doc = vectorstore.similarity_search_with_score(query=QUERY, by_text=False)
    similarity_score = doc[0][1]
    print("page_content", dict(doc[0][0])['page_content'])

    # Retriving the vector store
    embeddings = OpenAIEmbeddings()
    vector_store = Weaviate(client, SUBJECT, "content", embedding=embeddings)

    llm = OpenAI(temperature=0.5, verbose=True)
    # qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever(), return_source_documents=True)
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vector_store.as_retriever(), return_source_documents=True
    )
    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    #calculate the token spent and cost
    with get_openai_callback() as cb:
        result = qa({"question": QUERY, "chat_history": CHAT_HISTORY})
        print(f'{cb}')

    return result, similarity_score, cb

if __name__ == "__main__":
    print("Initiating llm config...")
    run_llm(QUERY='Explain me about THE CENTRAL GOODS AND SERVICES TAX Bill in gaming industry.', SUBJECT = "Current_affairs")
