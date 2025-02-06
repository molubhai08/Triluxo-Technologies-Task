import streamlit as st
from streamlit_chat import message as st_message
import requests as rq

# Initialize chat history in session state if not already present
if "history" not in st.session_state:
    st.session_state.history = []

# Set up the Streamlit app title
st.title("Hello Chatbot")

# Function to send user input to backend and receive response
def generate_answer():
    user_message = st.session_state.input_text  # Get user input
    BASE_URL = "http://127.0.0.1:5000/"  # API endpoint
    payload = {'input': user_message}  # Prepare request payload

    # Send GET request to chatbot API
    response = rq.get(BASE_URL, params=payload)
    json_values = response.json()  # Parse JSON response
    rq_input = json_values['code']  # Extract chatbot response

    # Append user input and chatbot response to session history
    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": rq_input, "is_user": False})

# Create a text input box with event trigger for message submission
st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)

# Display chat history using Streamlit message component
for i, chat in enumerate(st.session_state.history):
    st_message(**chat, key=str(i))  # Unpack dictionary values into message component