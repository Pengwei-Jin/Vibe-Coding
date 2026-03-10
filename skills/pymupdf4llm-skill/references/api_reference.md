# PyMuPDF4LLM API Reference

## Core Functions

### `pymupdf4llm.to_markdown(doc, pages=None, **kwargs)`

Convert a PDF document to Markdown format.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `doc` | `str` or `pymupdf.Document` | (required) | Path to PDF file or a PyMuPDF Document object |
| `pages` | `list[int]` or `None` | `None` | List of 0-based page numbers to extract. `None` means all pages |

**Returns:** `str` — Markdown-formatted text content of the PDF.

**Example:**

```python
import pymupdf4llm

# All pages
md = pymupdf4llm.to_markdown("report.pdf")

# Specific pages
md = pymupdf4llm.to_markdown("report.pdf", pages=[0, 1, 5])
```

---

### `pymupdf4llm.to_markdown(doc)` with PyMuPDF Document

You can pass an already-opened PyMuPDF document:

```python
import pymupdf
import pymupdf4llm

doc = pymupdf.open("report.pdf")
md = pymupdf4llm.to_markdown(doc)
doc.close()
```

This is useful when you need to perform other operations on the document before or after extraction.

---

### LlamaIndex Integration

pymupdf4llm can output directly as LlamaIndex documents:

```python
import pymupdf4llm

# Get LlamaIndex documents
llama_docs = pymupdf4llm.to_markdown("report.pdf", as_llama_index=True)
```

This returns a list of LlamaIndex `Document` objects, ready for use in LlamaIndex pipelines.

---

## PyMuPDF Companion Functions

These are from the underlying PyMuPDF library, useful alongside pymupdf4llm:

### `pymupdf.open(filename)`

Open a PDF document.

```python
import pymupdf
doc = pymupdf.open("file.pdf")
print(f"Pages: {len(doc)}")
doc.close()
```

### `page.get_text()`

Get plain text from a page (PyMuPDF native, not pymupdf4llm):

```python
import pymupdf
doc = pymupdf.open("file.pdf")
for page in doc:
    text = page.get_text()
doc.close()
```

---

## Error Handling

Common exceptions to handle:

```python
import pymupdf4llm

try:
    md = pymupdf4llm.to_markdown("file.pdf")
except FileNotFoundError:
    print("PDF file not found")
except RuntimeError as e:
    print(f"PDF processing error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```
