# RAG Integration Guide

## Overview

PyMuPDF4LLM is specifically designed for Retrieval-Augmented Generation (RAG) systems. This guide shows how to integrate PDF extraction into your RAG pipeline.

## Why PyMuPDF4LLM for RAG?

Traditional PDF extraction tools often produce poorly formatted text that's difficult for LLMs to process. PyMuPDF4LLM addresses this by:

- **Preserving Structure**: Headers, lists, and document hierarchy are maintained
- **Markdown Format**: Clean, readable format that LLMs understand well
- **Semantic Chunking**: Structure preservation enables better chunk boundaries
- **Metadata Retention**: Document structure helps with retrieval relevance

## Basic RAG Pipeline

### Step 1: Extract PDF Content

```python
import pymupdf4llm

# Extract PDF to Markdown
md_text = pymupdf4llm.to_markdown("knowledge_base.pdf")
```

### Step 2: Chunk the Content

```python
def chunk_by_headers(md_text: str) -> list[dict]:
    """Chunk Markdown by headers for semantic coherence."""
    chunks = []
    current_chunk = []
    current_header = ""
    
    for line in md_text.split("\n"):
        if line.startswith("#"):
            if current_chunk:
                chunks.append({
                    "header": current_header,
                    "content": "\n".join(current_chunk)
                })
            current_header = line
            current_chunk = [line]
        else:
            current_chunk.append(line)
    
    if current_chunk:
        chunks.append({
            "header": current_header,
            "content": "\n".join(current_chunk)
        })
    
    return chunks

chunks = chunk_by_headers(md_text)
```

### Step 3: Create Embeddings

```python
from openai import OpenAI

client = OpenAI()

def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Add embeddings to chunks."""
    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["content"]
        )
        chunk["embedding"] = response.data[0].embedding
    return chunks

embedded_chunks = embed_chunks(chunks)
```

### Step 4: Store in Vector Database

```python
# Example with ChromaDB
import chromadb

client = chromadb.Client()
collection = client.create_collection("pdf_knowledge")

for i, chunk in enumerate(embedded_chunks):
    collection.add(
        ids=[f"chunk_{i}"],
        embeddings=[chunk["embedding"]],
        documents=[chunk["content"]],
        metadatas=[{"header": chunk["header"]}]
    )
```

### Step 5: Query and Retrieve

```python
def query_rag(question: str, collection, top_k: int = 3) -> str:
    """Query the RAG system."""
    # Get question embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )
    query_embedding = response.data[0].embedding
    
    # Retrieve relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    context = "\n\n".join(results["documents"][0])
    
    # Generate answer with LLM
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Answer based on the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    
    return completion.choices[0].message.content

answer = query_rag("What are the main findings?", collection)
```

## LlamaIndex Integration

LlamaIndex provides a higher-level abstraction:

```python
import pymupdf4llm
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# Extract PDF as LlamaIndex documents
documents = pymupdf4llm.to_markdown("paper.pdf", as_llama_index=True)

# Setup vector store
chroma_client = chromadb.Client()
chroma_collection = chroma_client.create_collection("papers")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Build index
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("Summarize the methodology")
print(response)
```

## LangChain Integration

```python
import pymupdf4llm
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Extract PDF
md_text = pymupdf4llm.to_markdown("document.pdf")

# Split by headers
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
splits = markdown_splitter.split_text(md_text)

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(splits, embeddings)

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Query
result = qa_chain.run("What is the conclusion?")
print(result)
```

## Best Practices for RAG

### 1. Chunk Size Optimization

```python
# Test different chunk sizes
chunk_sizes = [500, 1000, 1500, 2000]
for size in chunk_sizes:
    chunks = chunk_markdown(md_text, chunk_size=size)
    # Evaluate retrieval quality
```

### 2. Preserve Document Structure

Use header-based chunking to maintain semantic coherence:

```python
def smart_chunk(md_text: str, max_size: int = 1000) -> list[str]:
    """Chunk by headers, respecting max size."""
    chunks = []
    current = []
    current_size = 0
    
    for line in md_text.split("\n"):
        line_size = len(line)
        
        if line.startswith("#") and current_size > 0:
            if current_size + line_size > max_size:
                chunks.append("\n".join(current))
                current = [line]
                current_size = line_size
            else:
                current.append(line)
                current_size += line_size
        else:
            current.append(line)
            current_size += line_size
    
    if current:
        chunks.append("\n".join(current))
    
    return chunks
```

### 3. Add Metadata

```python
import pymupdf
import pymupdf4llm

doc = pymupdf.open("paper.pdf")
metadata = {
    "title": doc.metadata.get("title", "Unknown"),
    "author": doc.metadata.get("author", "Unknown"),
    "pages": len(doc)
}

md_text = pymupdf4llm.to_markdown(doc)
doc.close()

# Include metadata in chunks
for chunk in chunks:
    chunk["metadata"] = metadata
```

### 4. Handle Multi-Document Collections

```python
from pathlib import Path

def process_pdf_collection(pdf_dir: Path) -> list[dict]:
    """Process multiple PDFs for RAG."""
    all_chunks = []
    
    for pdf_file in pdf_dir.glob("*.pdf"):
        md = pymupdf4llm.to_markdown(str(pdf_file))
        chunks = chunk_by_headers(md)
        
        for chunk in chunks:
            chunk["source"] = pdf_file.name
            all_chunks.append(chunk)
    
    return all_chunks
```

## Performance Considerations

- **Large PDFs**: Process in batches to manage memory
- **Embedding Costs**: Cache embeddings to avoid recomputation
- **Retrieval Speed**: Use approximate nearest neighbor search for large collections
- **Update Strategy**: Implement incremental updates rather than full reprocessing

## Evaluation

Test your RAG system with these metrics:

```python
def evaluate_rag(questions: list[str], expected_answers: list[str]):
    """Evaluate RAG performance."""
    correct = 0
    for q, expected in zip(questions, expected_answers):
        answer = query_rag(q, collection)
        # Use LLM to judge if answer matches expected
        # Or use exact match, semantic similarity, etc.
    
    accuracy = correct / len(questions)
    return accuracy
```
