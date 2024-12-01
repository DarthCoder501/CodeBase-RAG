import os

# Set up API keys and configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = 'us-east-1'
PINECONE_INDEX_NAME = 'codebase-rag'
PINECONE_NAMESPACE = 'https://github.com/CoderAgent/SecureAgent'
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-70b-versatile"
