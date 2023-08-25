""" 
 Basic PDF Document search using

"""
from langchain.document_loaders import PyPDFLoader
import streamlit as st
import langchain
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


st.title("Using Faiss Index for similarity search through medical database schema and generate sql")
langchain.verbose = False
loader = TextLoader("sample_data/metadata.txt")
pages = loader.load_and_split()

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="langchain_api_key_openai", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/jayeshvpatil/langchain-demo/blob/main/pages/03_docsearch.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    with open("sample_data/metadata.txt","r") as f:
        tables = f.read()
        st.code(tables)

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

question_list=[ "write a SQL query to Obtain the names of all physicians that have performed a medical procedure they have never been certified to perform.",
"Write a SQL query to Obtain the names of all physicians that have performed a medical procedure that they are certified to perform, but such that the procedure was done at a date (Undergoes.Date) after the physician's certification expired (Trained_In.CertificationExpires).",
"Write a SQL query. Here's some information: The hospital has several examination rooms where appointments take place. Obtain the number of appointments that have taken place in each examination room.",
"Write a SQL query with Physician name, name of procedure, date when the procedure was carried out, name of the patient the procedure was carried out on, and date when the certification expired.",
"Write a SQL query to Obtain the names of all the nurses who have ever been on call for room 123."
]
st.write(question_list)

question = st.text_input("Ask questions to generate sql. Choose one from above if you need examples")

if question:
    faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings(openai_api_key=openai_api_key))
    docs = faiss_index.similarity_search(question, k=2)

    # completion llm
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=faiss_index.as_retriever()
    )

    result = qa.run(question)
    st.write(result)