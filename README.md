# PDF to Pinecone Ingest Utility

This tool processes a PDF document, splits the text into manageable chunks, generates embeddings using OpenAI, and uploads the results to Pinecone for use with retrieval-augmented generation (RAG) or search applications.

---

## 🚀 Features

- Parses PDF documents with token-based chunking  
- Supports overlapping chunks to improve context retention  
- Generates vector embeddings using OpenAI's `text-embedding-3-small` model  
- Stores vectors in Pinecone with rich metadata for easy retrieval  

---

## ⚙️ Environment Configuration

Create a `.env` file in your project root with the following:

PINECONE_INDEX=your-index
PINECONE_NAMESPACE=default
PINECONE_API_KEY=your-pinecone-api-key
OPENAI_API_KEY=your-openai-api-key

## 🧩 Chunking Considerations

Effective chunking is essential for building reliable search or retrieval-augmented generation (RAG) systems. The size and overlap of your text chunks directly impact retrieval accuracy, context retention, and downstream LLM performance.

### Key Factors to Consider

- **Document Size**  
  For small documents, use smaller chunks to avoid over-splitting limited content. Example:  
  `TOKEN_LIMIT = 20`  
  `TOKEN_OVERLAP = 5`  

- **Context Length of Your LLM or Search Application**  
  If downstream models can handle larger context windows (e.g., GPT-4-turbo), you may increase chunk size to preserve more coherent sections of text.

- **Overlap for Better Context**  
  Overlapping tokens help maintain continuity between chunks, improving semantic search results and reducing information gaps.

- **Token Counting Accuracy**  
  This script uses a basic word-based token estimate. For production-grade implementations, integrate a true tokenizer like [`tiktoken`](https://github.com/openai/tiktoken) to ensure precise token-level chunking.

---

### Example Configurations

| Document Type       | Token Limit | Overlap |
|---------------------|-------------|----------|
| Small Policy PDFs   | 20          | 5        |
| Medium Reports      | 100         | 20       |
| Large Legal Docs    | 200         | 50       |

---

### General Recommendations

- Test different chunk sizes based on your specific documents and retrieval use case  
- Larger chunks improve context but may reduce retrieval precision  
- Smaller chunks increase granularity but risk losing coherence  

---

### ⚡ Next Steps

### ⚡ Next Steps for Advanced Implementations

- ✅ Swap in a true tokenizer for accurate token-based chunking (e.g., [`tiktoken`](https://github.com/openai/tiktoken))  
- ✅ Explore dynamic chunking based on natural boundaries (sentences, paragraphs, headings) for improved semantic coherence  
- ✅ Add **annotations or metadata tags** to each chunk to capture context such as section titles, document structure, or legal citations  
- ✅ Validate chunk quality with semantic search, test queries, and downstream LLM performance  
- ✅ Use overlapping chunks strategically to balance context retention and retrieval precision  

