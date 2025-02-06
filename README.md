# Triluxo-Technologies-Task


This project implements a chatbot that extracts and processes course data from Brainlox using LangChain, Flask, and Streamlit.

## Features
- **Data Extraction**: Uses LangChain's `WebBaseLoader` to scrape course data from Brainlox.
- **Embedding & Vector Store**: Converts scraped text into vector embeddings using `OllamaEmbeddings` and stores them in `FAISS`.
- **Flask API**: Hosts a RESTful API to retrieve chatbot responses.
- **Streamlit UI**: Provides an interactive chat interface for users.

## Tech Stack
- **Python**
- **LangChain** (FAISS, ChatGroq, WebBaseLoader, OllamaEmbeddings)
- **Flask** (REST API)
- **Streamlit** (Frontend Chat UI)
- **FAISS** (Vector Database)
- **Requests** (API Communication)

## Installation
### Prerequisites
Ensure you have Python installed.

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Running the Application
### 1. Start the Flask Backend
```sh
python app.py
```
This will start the API on `http://127.0.0.1:5000/`.

### 2. Start the Streamlit Frontend
```sh
streamlit run chatbot.py
```
This will launch the chatbot UI in your browser.

## Usage
- Type a message in the Streamlit chatbot interface.
- The message is sent to the Flask API, which retrieves the response from FAISS.
- The response is displayed in the chat interface.

## API Endpoint
### `GET /`
**Parameters:**
- `input`: User query.

**Example Request:**
```sh
curl "http://127.0.0.1:5000/?input=Tell me about Java courses"
```

**Example Response:**
```json
{
    "code": "The Java course covers core programming concepts..."
}
```

## Future Improvements
- Deploy the Flask API and Streamlit UI online.
- Add authentication for secure access.
- Integrate more AI models for advanced responses.

## Author
Developed as part of an AI chatbot task using LangChain and Flask. 🚀

