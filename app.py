import streamlit as st
from rag import perform_rag  # Import the perform_rag function from rag.py file

# Set the Streamlit app configuration
st.set_page_config(page_title="Codebase Chatbot", layout="wide")

# Title and Description
st.title("Codebase Chatbot")
st.write(
    """
    Welcome to your codebase chatbot! Engage in a conversation about your codebase,
    and receive detailed answers based on the embedded context.
    """
)

# Initialize session state for storing chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm here to answer your questions about the codebase. How can I assist you today?"}]  # List to hold chat messages

# Display previous messages in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # `role` can be "user" or "assistant"
        st.markdown(message["content"])  # Render the message content

# Input box for user query
if user_input := st.chat_input("Ask your question about the codebase..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)  # Display user's message

    # Process the query with the RAG function
    with st.chat_message("assistant"):
        with st.spinner("Processing your query..."):
            try:
                # Call perform_rag to generate a response
                response = perform_rag(user_input)
                st.markdown(response)  # Display assistant's response
                # Add assistant's response to session state
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_message = f"An error occurred: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
