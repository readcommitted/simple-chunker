import pinecone
import uuid
import PyPDF2
import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

# --- Pinecone Setup ---
PINECONE_INDEX = os.environ.get("PINECONE_INDEX")
PINECONE_NAMESPACE = os.environ.get("PINECONE_NAMESPACE", "default")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# --- Configurable Constants ---
TOKEN_LIMIT = 20  # Tokens per chunk
TOKEN_OVERLAP = 5  # Overlapping tokens between chunks
EMBEDDING_MODEL = "text-embedding-3-small"

# --- OpenAI Setup ---
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

client = OpenAI(api_key=api_key)


# --- Pinecone Setup ---
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)


# --- Basic Token Counter ---
def count_tokens(text: str) -> int:
    return len(text.split())  # Swap for true tokenizer later if desired


# --- PDF Parsing and Chunking ---
def parse_pdf_to_chunks(pdf_path: str, token_limit: int, token_overlap: int) -> List[str]:
    reader = PyPDF2.PdfReader(pdf_path)
    full_text = " ".join(page.extract_text() or "" for page in reader.pages)

    words = full_text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + token_limit
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += token_limit - token_overlap

    return chunks


# --- Embedding Generator with Correct Client Usage ---
def get_embedding(text: str) -> List[float]:
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding


# --- Ingest PDF to Pinecone ---
def ingest_pdf_to_pinecone(pdf_path: str, source: str, title: str):
    chunks = parse_pdf_to_chunks(pdf_path, TOKEN_LIMIT, TOKEN_OVERLAP)

    vectors = []
    for idx, chunk in enumerate(chunks):
        vector_id = str(uuid.uuid4())
        embedding = get_embedding(chunk)

        metadata = {
            "source": source,
            "title": title,
            "chunk_id": idx,
            "text_chunk": chunk
        }

        vectors.append({
            "id": vector_id,
            "values": embedding,
            "metadata": metadata
        })

        print(f"\n--- Chunk {idx} ---")
        print(f"Source: {source}")
        print(f"Title: {title}")
        print(f"Text:\n{chunk[:500]}...\n")

    index.upsert(vectors=vectors, namespace=PINECONE_NAMESPACE)
    print(f"✅ Ingested {len(vectors)} chunks to Pinecone.")


if __name__ == "__main__":
    ingest_pdf_to_pinecone(
        pdf_path="assets/refund_return_policy.pdf",
        source="refund_return_policy.pdf",
        title="Refund & Return Policy"
    )
