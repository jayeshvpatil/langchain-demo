import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory


# From here down is all the StreamLit UI.
st.set_page_config(page_title="Chat Demo", page_icon=":robot:")
st.header("Hey, I'm your Chat GPT")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="langchain_api_key_openai", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/jayeshvpatil/langchain-demo/blob/main/pages/04_Conversation_Chat.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.chat_message("user"):
    st.write("Hello 👋")


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



response_container = st.container()
# Here we will have a container for user input text box
container = st.container()
with container:
    # React to user input
    if prompt := st.chat_input("Say something"):
        # Display user message in chat message container
        st.chat_message("user").write(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        llm = OpenAI(
            temperature=0,
            openai_api_key=openai_api_key,
            model_name='text-davinci-003'  #we can also use 'gpt-3.5-turbo'
        )
        conversion = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationBufferWindowMemory(k=2)
        )
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = conversion.predict(input=prompt)
                st.write(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})

