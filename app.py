import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

os.environ['OPENAI_API_KEY']= apikey

st.title('Product Creator')
prompt = st.text_input("plug in a product idea here")

name_template = PromptTemplate(input_variables=['product_idea'],
    template = 'Generate a product name for the {product_idea}'
)

desc_template = PromptTemplate(input_variables = ['product_name'],
    template = 'Generate a product description for the {product_name}'
)

#memory 
memory = ConversationBufferMemory(input_key='product_idea', memory_key='chat_history')

#llm chain
llm = OpenAI(temperature=0.9)
name_chain = LLMChain(llm=llm, prompt=name_template, verbose=True, output_key='product_name', memory=memory)
desc_chain = LLMChain(llm=llm,prompt=desc_template, verbose=True, output_key='product_desc', memory=memory)
seq_chain = SequentialChain(chains=[name_chain,desc_chain],input_variables=['product_idea'], 
                            output_variables=['product_name','product_desc'])


if prompt:
    response = seq_chain({'product_idea':prompt})
    st.write(response['product_name'])
    st.write(response['product_desc'])

    with st.expander('Chat History'):
        st.info(memory.buffer)