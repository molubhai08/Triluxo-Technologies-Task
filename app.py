import os
from dotenv import load_dotenv  # Load environment variables from a .env file
load_dotenv()
USER_AGENT = os.getenv("USER_AGENT")

# Import necessary libraries from LangChain and Flask
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from flask import Flask, request, jsonify
from langchain_core.output_parsers import StrOutputParser
import json

# Set environment variable manually (optional, can also use .env file)
os.environ['USER_AGENT'] = 'myagent'

# Initialize Flask application
app = Flask(__name__)

# Define the URLs to extract course data from Brainlox
page_urls = [
    "https://brainlox.com/courses/category/technical/",
    "https://brainlox.com/courses/4f629d96-5ed9-4302-ae0e-3479c543a49e",
    "https://brainlox.com/courses/872d1cb6-8469-4797-b267-8c41837b10e2",
    "https://brainlox.com/courses/be32e068-edca-4b41-96ee-4839de6aaebb",
    "https://brainlox.com/courses/fe8f5696-eb0e-48a0-a505-147e9c502b65"
]

# Load data from the URLs using WebBaseLoader
loader = WebBaseLoader(web_paths=page_urls)
text = loader.load()

# Initialize Language Model (LLM) with Groq API
llm = ChatGroq(
    groq_api_key="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",
    model="llama3-70b-8192"
)

# Split the extracted text into smaller chunks for better retrieval
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
final = splitter.split_documents(text)

# Generate embeddings for the text using Ollama Embeddings
embedder = OllamaEmbeddings(model="nomic-embed-text")

# Store embeddings in FAISS vector database
db = FAISS.from_documents(final, embedder)

# Define chatbot prompt with structured instructions for generating responses
prompt = ChatPromptTemplate.from_template(
    """You are an intelligent and interactive assistant designed to help users with technical courses. 
    Your role is to **guide, explain, and assist** users with their queries using ONLY the provided context. 

    Instructions:
    - Use the provided context to answer questions.
    - If a user asks about learning a topic, provide an overview and suggest a structured approach based on the available courses.
    - If a course is mentioned (e.g., "LEARN CORE JAVA PROGRAMMING ONLINE"), offer insights into its content and how it can benefit learners.
    - If the answer is not found within this context, respond with:  
      **"I cannot find the answer in the provided document, but I can still help you understand related concepts!"**  
    - **Do NOT include information about Python courses.** If the user specifically asks about Python courses, respond with:  
      **"I am unable to provide information about Python courses at the moment."**

    Context:
    {context}

    Question: {input}
    """
)

# Create a retriever from the FAISS database
retriever = db.as_retriever()

# Create document chain using the chatbot model and prompt
document_chain = create_stuff_documents_chain(llm, prompt)

# Create retrieval chain to fetch relevant data
chain = create_retrieval_chain(retriever, document_chain)

# Initialize output parser to format chatbot responses
parser = StrOutputParser()

# Define a Flask API endpoint to handle chatbot queries
@app.route('/', methods=['GET', 'POST'])
def handle_request():
    # Get user input from request
    text = request.args.get('input')

    # Return error if no input is provided
    if not text:
        return jsonify({"error": "No input provided"}), 400
    
    # Generate response using the chatbot chain
    response = chain.invoke({"input": text})
    a = response['answer']

    # Return response in JSON format
    dataset = {'code': a}
    return json.dumps(dataset)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
