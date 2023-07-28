import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

st.header('Simple Langchain demo - Product generator')
st.text('Using langchain and open ai to generate product names')

prompt = st.text_input("plug in a product idea here")
name_template = PromptTemplate(input_variables=['product_idea'],
    template = 'Generate a product name for the {product_idea}'
)

desc_template = PromptTemplate(input_variables = ['product_name'],
    template = 'Generate a product description for the {product_name}'
)

#memory 
memory = ConversationBufferMemory(input_key='product_idea', memory_key='chat_history')


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="langchain_api_key_openai", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/jayeshvpatil/langchain-demo/blob/main/pages/01_langchain.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

if prompt:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    #llm chain
    llm = OpenAI(temperature=0.9, openai_api_key=openai_api_key)
    name_chain = LLMChain(llm=llm, prompt=name_template, verbose=True, output_key='product_name', memory=memory)
    desc_chain = LLMChain(llm=llm,prompt=desc_template, verbose=True, output_key='product_desc', memory=memory)
    seq_chain = SequentialChain(chains=[name_chain,desc_chain],input_variables=['product_idea'], 
                                output_variables=['product_name','product_desc'])    
    response = seq_chain({'product_idea':prompt})
    st.write(response['product_name'])
    st.write(response['product_desc'])

    with st.expander('Chat History'):
        st.info(memory.buffer)