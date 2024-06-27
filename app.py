# Import libraries
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import os

# Function to get response from my LLama2 model
@st.cache_resource
def load_model():
    model_path = "models/llama-2-7b-chat.ggmlv3.q8_0.bin"
    if not os.path.exists(model_path):
        st.error(f"Model file not found at {model_path}. Please check the path and try again.")
        return None
    return CTransformers(model=model_path, model_type="llama", config={"max_new_tokens": 256, "temperature": 0.01})

def fetch_response(llm, input_text, no_words, blog_style):
    if llm is None:
        return "Model not loaded. Please check the path and try again."

    # Template for Prompts
    template = """
            Write a blog for {blog_style} job profile for a topic on 
            {input_text} within {no_words} words.
        """
    
    prompt = PromptTemplate(input_variables=["blog_style", "input_text", "no_words"], template=template)

    try:
        # Generate response from LLama2 model
        response = llm.invoke(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
        return response
    except Exception as e:
        return f"An error occurred: {e}"

st.set_page_config(page_title="Generate Blog Posts", page_icon="🤖", layout="centered", initial_sidebar_state="collapsed")

st.header("Generate Blog Posts 🤖")

input_text = st.text_input("Enter the Topic or Title for your Blog")

## Additional fields
col1, col2 = st.columns([5, 5]) # width for columns

with col1:
    no_words = st.text_input("Number of Words")

with col2:
    blog_style = st.selectbox("Writing the blogpost for", ("Researchers", "Data Scientist", "AI Enthusiasts"), index=0)

submit = st.button("Generate Post")

# Load the model once
llm = load_model()

# Response
if submit:
    if not input_text or not no_words:
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Generating your blog post..."):
            response = fetch_response(llm, input_text, no_words, blog_style)
            st.write(response)
