import os
import streamlit as st
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA

location = './sample_data'
persist_directory = "chroma_db"

#list all files in the sample directory
files = [f for f in os.listdir(location)]
st.write(files)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/jayeshvpatil/langchain-demo/blob/main/pages/01_langchain.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


def load_and_split_docs(directory, chunk_size=250):
    loader = DirectoryLoader(directory)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
    docs = loader.load_and_split(text_splitter)
    # st.write(len(docs))
    return docs

def create_vector_db(docs, openai_api_key):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)  
    db =   Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    db.persist()
    return db

docs = load_and_split_docs(location)
db = create_vector_db(docs, openai_api_key)

st.write("Do a similarity search ")
with st.echo():
    query = "Can you tell me 2 CDP use cases?"
    st.write(query)
    matching_docs = db.similarity_search(query)
    st.write(matching_docs[0])

st.write('Run Q&A chain to use the matching docs with LLM')
with st.echo():
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    qa_chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
    answer =  qa_chain.run(input_documents=matching_docs, question=query)
    st.write(answer)

st.write('Run Retriever chain to use the matching docs with LLM')
with st.echo():
    retrieval_chain = RetrievalQA.from_chain_type(llm,chain_type="stuff", retriever = db.as_retriever())
    answer = retrieval_chain.run(query)
    st.write(answer)