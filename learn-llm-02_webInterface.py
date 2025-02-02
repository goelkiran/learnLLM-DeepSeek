"""
This script provides a web interface for interacting with PDF documents using a language model.
It includes functions for loading and processing PDFs, generating responses from a language model,
and performing retrieval augmented generation (RAG).
Functions:
    load_and_process_pdf(pdf_file_bytes):
        Load and process a PDF file, returning text splitter, vector store, and document retriever.
        Args:
            pdf_file_bytes (bytes): The PDF file in bytes.
        Returns:
            tuple: A tuple containing document chunks, vector store, and document retriever.
    generate_llm_response(question, context):
        Generate a response from the language model based on a question and context.
        Args:
            question (str): The question to ask the language model.
            context (str): The context to provide to the language model.
        Returns:
            str: The generated response from the language model.
    perform_RAG(question, retriever):
        Perform retrieval augmented generation by retrieving relevant documents and generating a response.
        Args:
            question (str): The question to ask the language model.
            retriever: The document retriever to use for retrieving relevant documents.
        Returns:
            str: The generated response from the language model.
    handle_question(pdf_file_bytes, question):
        Handle a question by processing a PDF and generating a response.
        Args:
            pdf_file_bytes (bytes): The PDF file in bytes.
            question (str): The question to ask the language model.
        Returns:
            str: The generated response from the language model or None if no PDF is uploaded.
Gradio Interface:
    A Gradio interface is created for uploading a PDF and asking questions.
    The interface includes:
        - A file upload component for uploading PDF documents.
        - A textbox for entering the prompt/question.
        - A text output for displaying the generated response.
"""
import ollama
import gradio as gr
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

import re
import time

model_name = "deepseek-r1:8b"

def load_and_process_pdf(pdf_file_bytes):
    """Load and process PDF, returning text splitter, vector store, and document retriever."""
    if pdf_file_bytes is None:
        return None, None, None

    start_time = time.time()
    document_data = PyMuPDFLoader(pdf_file_bytes).load()
    print(f"{time.time() - start_time:09.3f} seconds taken by load_and_process_pdf:PDF Loading.")
    
    start_time = time.time()
    document_chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(document_data)
    print(f"{time.time() - start_time:09.3f} seconds taken by load_and_process_pdf:Text splitting.")
    
    start_time = time.time()
    embeddings_model = OllamaEmbeddings(model=model_name)
    print(f"{time.time() - start_time:09.3f} seconds taken by load_and_process_pdf:Embeddings model creation.")
    
    start_time = time.time()
    vector_store = Chroma.from_documents(documents=document_chunks, embedding=embeddings_model)
    print(f"{time.time() - start_time:09.3f} seconds taken by load_and_process_pdf:Vector store creation.")
    
    start_time = time.time()
    document_retriever = vector_store.as_retriever()
    print(f"{time.time() - start_time:09.3f} seconds taken by load_and_process_pdf:Document retriever creation.")
    
    return document_chunks, vector_store, document_retriever

def generate_llm_response(question, context):
    """Generate LLM response based on question and context."""
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    start_time = time.time()
    response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': formatted_prompt}])
    print(f"{time.time() - start_time:09.3f} seconds taken by generate_llm_response:Response generation.")
    
    response_content = response['message']['content']
    
    # Remove content between <think> and </think> tags to remove thinking output
    final_answer = re.sub(r'<think>.*?</think>', '', response_content, flags=re.DOTALL).strip()
    return final_answer

def perform_RAG(question, retriever):
    """Perform retrieval augmented generation."""
    start_time = time.time()
    retrieved_documents = retriever.invoke(question)
    print(f"{time.time() - start_time:09.3f} seconds taken by perform_RAG:Document retrieval.")
    
    combined_content = "\n\n".join(doc.page_content for doc in retrieved_documents)
    return generate_llm_response(question, combined_content)

def handle_question(pdf_file_bytes, question):
    """Handle question by processing PDF and generating response."""
    document_chunks, vector_store, retriever = load_and_process_pdf(pdf_file_bytes)
    if document_chunks is None:
        return None  # No PDF uploaded
    return perform_RAG(question, retriever)

# Create a Gradio interface for uploading a PDF and asking questions
interface = gr.Interface(
    fn=handle_question,
    inputs=[gr.File(label="Upload Your PDF Documents (optional)"), gr.Textbox(label="Your Prompt")],
    outputs="text",
    title="LLM Democratization",
    description="Using DeepSeek-R1 interact with the uploaded PDFs.",
)
interface.launch()
