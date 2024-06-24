# summarization.py

import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
# Set your OpenAI API key
open_api_key = "sk-smwm1RBSXekyqdUplCkFJRdSSbKPJJgiqBx3JZZve"
os.environ["OPENAI_API_KEY"] = open_api_key

# Initialize the OpenAI LLM
llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)

# Summarize a given speech
def summarize_text(text, language='English'):
    generic_template = '''
    Write a summary of the following speech:
    Speech : `{speech}`
    Translate the precise summary to {language}.
    '''
    prompt = PromptTemplate(
        input_variables=['speech', 'language'],
        template=generic_template
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    summary = llm_chain.run({'speech': text, 'language': language})
    return summary

# Summarize text extracted from a PDF file
def summarize_pdf(pdf_file, chain_type='map_reduce'):
    pdfreader = PdfReader(pdf_file)
    text = ''
    for page in pdfreader.pages:
        content = page.extract_text()
        if content:
            text += content

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
    chunks = text_splitter.create_documents([text])

    chunks_prompt = """
    Please summarize the below speech:
    Speech:`{text}`
    Summary:
    """
    map_prompt_template = PromptTemplate(input_variables=['text'], template=chunks_prompt)
    
    final_combine_prompt = '''
    Provide a final summary of the entire speech with these important points.
    Add a Generic Motivational Title,
    Start the precise summary with an introduction and provide the
    summary in number points for the speech.
    Speech: `{text}`
    '''
    final_combine_prompt_template = PromptTemplate(input_variables=['text'], template=final_combine_prompt)

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type=chain_type,
        map_prompt=map_prompt_template,
        combine_prompt=final_combine_prompt_template,
        verbose=False
    )
    summary = summary_chain.run(chunks)
    return summary

