# PyMuPDF4LLM Usage Examples

## Example 1: Simple PDF to Markdown

```python
import pymupdf4llm
import pathlib

md_text = pymupdf4llm.to_markdown("input.pdf")
pathlib.Path("output.md").write_bytes(md_text.encode())
```

## Example 2: Extract First N Pages

```python
import pymupdf4llm

# Extract only the first 5 pages
md_text = pymupdf4llm.to_markdown("long_document.pdf", pages=list(range(5)))
print(md_text)
```

## Example 3: Batch Processing a Directory

```python
from pathlib import Path
import pymupdf4llm

input_dir = Path("pdfs/")
output_dir = Path("markdown/")
output_dir.mkdir(exist_ok=True)

for pdf_file in input_dir.glob("*.pdf"):
    try:
        md = pymupdf4llm.to_markdown(str(pdf_file))
        out = output_dir / f"{pdf_file.stem}.md"
        out.write_bytes(md.encode())
        print(f"Converted: {pdf_file.name}")
    except Exception as e:
        print(f"Failed: {pdf_file.name} - {e}")
```

## Example 4: Get Document Info Before Extraction

```python
import pymupdf
import pymupdf4llm

doc = pymupdf.open("report.pdf")
print(f"Title: {doc.metadata.get('title', 'N/A')}")
print(f"Pages: {len(doc)}")
print(f"Author: {doc.metadata.get('author', 'N/A')}")

md = pymupdf4llm.to_markdown(doc)
doc.close()
```

## Example 5: Extract and Chunk for RAG

```python
import pymupdf4llm


def chunk_markdown(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Split Markdown text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks


md_text = pymupdf4llm.to_markdown("paper.pdf")
chunks = chunk_markdown(md_text)
print(f"Created {len(chunks)} chunks")
```

## Example 6: Process with Progress Tracking

```python
import pymupdf
import pymupdf4llm

doc = pymupdf.open("large_document.pdf")
total_pages = len(doc)
results = []

# Process in batches of 10 pages
batch_size = 10
for start in range(0, total_pages, batch_size):
    end = min(start + batch_size, total_pages)
    pages = list(range(start, end))
    md = pymupdf4llm.to_markdown(doc, pages=pages)
    results.append(md)
    print(f"Processed pages {start+1}-{end} of {total_pages}")

full_md = "\n\n".join(results)
doc.close()
```

## Example 7: LlamaIndex Integration

```python
import pymupdf4llm
from llama_index.core import VectorStoreIndex

# Get LlamaIndex documents directly
documents = pymupdf4llm.to_markdown("knowledge_base.pdf", as_llama_index=True)

# Build index
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What are the key findings?")
print(response)
```
