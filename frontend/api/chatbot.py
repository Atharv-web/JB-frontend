import os, requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from pinecone import Pinecone

HF_API_KEY = os.getenv('HF_TOKEN')
HF_API_URL = "https://router.huggingface.co/hf-inference/models/intfloat/multilingual-e5-large/pipeline/feature-extraction"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def get_embeddings(text: str):
    payload = {"inputs": text}
    response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)
    response.raise_for_status()
    embeddings = response.json()
    return embeddings[0] if isinstance(embeddings[0], list) else embeddings

def get_llm_model():
    gemini_key = os.getenv('GEMINI_API_KEY')
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=gemini_key)
    return llm

def get_pinecone_index():
    pinecone_key = os.getenv("PINECONE_API_KEY")
    pinecone_client = Pinecone(api_key=pinecone_key)
    index = pinecone_client.Index("jain-bot")
    return index

def get_chatbot_response(user_input: str) -> str:
    vectorized_query = get_embeddings(f"query: {user_input}")

    index = get_pinecone_index()
    namespace = "jain-vidya-3"
    search_result = index.query(
        namespace=namespace,
        vector=vectorized_query,
        top_k=3,
        include_metadata=True
    )

    retrieved_docs = [res["metadata"]["text"] for res in search_result["matches"]]
    db_context = "\n\n---\n\n".join(retrieved_docs)

    rag_prompt = f"""You are an assistant for question-answering tasks in Hindi.
    Use the below given context to answer question. Read and understand the context carefully.
    {db_context}

    now carefully read the user question:
    {user_input}
    
    Provide a correct answer to the question by using the above context.
    Answer:"""

    llm = get_llm_model()
    model_response = llm.invoke([HumanMessage(content=rag_prompt)])

    return model_response.content