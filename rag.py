import requests
from pinecone import Pinecone, ServerlessSpec
from embeddings import get_huggingface_embeddings
from keys import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME, PINECONE_NAMESPACE,GROQ_MODEL, GROQ_API_KEY

# Initialize Pinecone
pc = Pinecone(
    api_key= PINECONE_API_KEY,
    spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
)

pinecone_index = pc.Index(PINECONE_INDEX_NAME)
index_description = pc.describe_index(PINECONE_INDEX_NAME)
print(index_description)
def perform_rag(query):
    """
    Perform Retrieval-Augmented Generation (RAG) to answer a query.

    Args:
        query (str): User query.

    Returns:
        str: LLM-generated response.
    """
    # Step 1: Generate embeddings for the query
    raw_query_embedding = get_huggingface_embeddings(query)
    raw_query_embedding_list = raw_query_embedding.tolist()

    # Step 2: Query Pinecone for relevant contexts
    top_matches = pinecone_index.query(
        vector=raw_query_embedding_list,
        top_k=5,
        include_metadata=True,
        namespace=PINECONE_NAMESPACE
    )

    # Extract contexts from matches
    contexts = [item['metadata']['text'] for item in top_matches['matches']]

    # Step 3: Construct an augmented query
    augmented_query = (
        "<CONTEXT>\n"
        + "\n\n-------\n\n".join(contexts[:10])  # Use top 10 results
        + "\n-------\n</CONTEXT>\n\n\n\nMY QUESTION:\n" + query
    )

    # Step 4: Define the system prompt
    system_prompt = (
        "You are a Senior Software Engineer specializing in Python and JavaScript. "
        "You are an expert in the Django framework.\n\n"
        "Answer the following question about the codebase using the context provided. "
        "Always explain your reasoning step by step."
    )

    # Step 5: Query the Llama 3.1 API
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
         "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": augmented_query}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    # Debugging Groq response

    if response.status_code == 200:
        response_json = response.json()
        try:
            return response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return "No response text found in the Groq API response."
    else:
        raise ValueError(f"Error from Llama API: {response.status_code} - {response.text}")
