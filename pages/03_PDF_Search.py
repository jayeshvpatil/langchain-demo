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

langchain.verbose = False
loader = PyPDFLoader("sample_data/cdp-ebook.pdf")
pages = loader.load_and_split()

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="langchain_api_key_openai", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/jayeshvpatil/langchain-demo/blob/main/pages/03_docsearch.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()


st.title("📝 Q&A PDF document")
uploaded_file = st.file_uploader("Upload a pdf", type=("pdf"))
question = st.text_input(
    "Ask something about the pdf",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)
st.write(pages[0])

query= 'Can you summarize this document for me?'
faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings(openai_api_key=openai_api_key))
docs = faiss_index.similarity_search(query, k=2)
for doc in docs:
    st.write(str(doc.metadata["page"]) + ":", doc.page_content[:300])

combined_text = ''
for i, page in enumerate(docs):
    text = page.extr 

llm = OpenAI(model="text-davinci-003", openai_api_key=openai_api_key)
pdf_search = FAISS.from_texts(pages, OpenAIEmbeddings(openai_api_key=openai_api_key))
qa_chain = load_qa_chain(llm=llm,chain_type='stuff')
pdfs = pdf_search.similarity_search(query,k=3)
qa_chain.run(input_documents=pdfs, question=query)