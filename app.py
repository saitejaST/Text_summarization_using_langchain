# app.py

import streamlit as st
from summarization import summarize_text, summarize_pdf 

st.title("Text Summarization App")

# Option to summarize direct text input
st.header("Summarize Text Input")
input_text = st.text_area("Enter text to summarize")

language = st.selectbox("Select language for summary", ["English", "Hindi"])

if st.button("Summarize Text"):
    if input_text:
        summary = summarize_text(input_text, language)
        st.subheader("Summary")
        st.write(summary)
    else:
        st.write("Please enter some text to summarize.")

# Option to summarize text from an uploaded PDF file
st.header("Summarize PDF File")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if st.button("Summarize PDF"):
    if uploaded_file:
        summary = summarize_pdf(uploaded_file)
        st.subheader("Summary")
        st.write(summary)
    else:
        st.write("Please upload a PDF file to summarize.")
