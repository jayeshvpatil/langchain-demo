import streamlit as st


st.title('LLM Demo Apps Home')


# Sidebar
st.sidebar.header("About")
st.sidebar.markdown(
    "LLM Demo app is collection of generative ai demo apps built using python, streamlit,langchain and other libraries"
)

st.sidebar.header("Resources")
st.sidebar.markdown("""
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
- [Langchain Documentation](https://docs.langchain.com/docs/)                    
"""
)

with open(f"README.md", "r") as f:
    st.markdown(f.read())