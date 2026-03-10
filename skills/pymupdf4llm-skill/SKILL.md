---
name: pymupdf4llm
description: Extract and convert PDF content to Markdown format optimized for LLM and RAG applications using pymupdf4llm. Use this skill when users need to extract text from PDFs, convert PDFs to Markdown, prepare PDF content for LLM processing, work with RAG systems, or mention pymupdf4llm. Also trigger when users want to process academic papers, documentation, reports, or any PDF documents for AI consumption.
---

# PyMuPDF4LLM Skill

This skill helps you work with PDF documents using the pymupdf4llm library, which is specifically designed to extract and format PDF content for Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) systems.

## What is PyMuPDF4LLM?

PyMuPDF4LLM is a specialized library built on top of PyMuPDF that extracts PDF content in formats optimized for AI applications. Unlike traditional PDF extraction tools, it:

- Preserves document structure with proper Markdown formatting
- Identifies headers based on font size and adds appropriate `#` tags
- Maintains readability for LLM consumption
- Supports selective page extraction
- Can output directly to LlamaIndex document format
- Works with both text-based and scanned PDFs (with OCR support)

## When to Use This Skill

Use this skill when the user needs to:

- Extract text from PDF files for LLM processing
- Convert PDF documents to Markdown format
- Prepare PDF content for RAG pipelines
- Process academic papers, research documents, or technical reports
- Batch process multiple PDF files
- Extract specific pages from PDF documents
- Work with PDF content in AI/ML workflows

## Installation

Before using pymupdf4llm, ensure it's installed. The basic installation includes the core library:

```bash
pip install pymupdf4llm
```

For full feature support including layout analysis and OCR:

```bash
pip install pymupdf4llm[full]
```

This installs additional dependencies:
- `opencv-python` - for image processing
- `pymupdf-layout` - for advanced layout analysis
- OCR capabilities for scanned documents

## Basic Usage Pattern

### Simple PDF to Markdown Conversion

The most common use case is converting a PDF to Markdown:

```python
import pymupdf4llm

# Convert entire PDF to Markdown
md_text = pymupdf4llm.to_markdown("input.pdf")

# Save to file
import pathlib
pathlib.Path("output.md").write_bytes(md_text.encode())
```

### Working with Specific Pages

To extract only certain pages, pass a list of 0-based page numbers:

```python
import pymupdf4llm

# Extract only first 3 pages (pages 0, 1, 2)
md_text = pymupdf4llm.to_markdown("input.pdf", pages=[0, 1, 2])
```

### Using PyMuPDF Document Objects

You can also work with PyMuPDF document objects directly:

```python
import pymupdf
import pymupdf4llm

# Open document with PyMuPDF
doc = pymupdf.open("input.pdf")

# Convert to Markdown
md_text = pymupdf4llm.to_markdown(doc)

# Or specific pages
md_text = pymupdf4llm.to_markdown(doc, pages=[0, 1, 2])

doc.close()
```

## Common Workflows

### Workflow 1: Single PDF Extraction

When a user provides a single PDF file:

1. Check if the file exists and is accessible
2. Verify pymupdf4llm is installed (install if needed)
3. Extract content using `to_markdown()`
4. Save or display the result based on user needs
5. Provide summary of extracted content (page count, approximate word count)

### Workflow 2: Batch Processing Multiple PDFs

When processing multiple PDF files:

1. Use the batch processing script from `scripts/batch_convert.py`
2. Process files in the specified directory
3. Handle errors gracefully (corrupted PDFs, permission issues)
4. Provide progress updates for large batches
5. Generate a summary report of successful/failed conversions

### Workflow 3: Selective Page Extraction

When user needs specific pages:

1. Parse the page specification (ranges, individual pages)
2. Convert to 0-based page numbers
3. Extract only specified pages
4. Validate page numbers are within document bounds

### Workflow 4: RAG Pipeline Preparation

When preparing content for RAG systems:

1. Extract PDF content to Markdown
2. Optionally chunk the content into appropriate segments
3. Preserve document structure and headers for better retrieval
4. Consider using LlamaIndex output format if applicable

## Helper Scripts

This skill includes helper scripts in the `scripts/` directory:

### batch_convert.py

Batch converts multiple PDF files to Markdown. Use this when the user has a directory of PDFs to process.

```bash
python scripts/batch_convert.py <input_dir> <output_dir> [--pages 0,1,2]
```

### extract_pages.py

Extracts specific pages from a PDF. Useful for targeted extraction.

```bash
python scripts/extract_pages.py <input.pdf> <output.md> --pages 0-5,10,15-20
```

### validate_install.py

Checks if pymupdf4llm and dependencies are properly installed.

```bash
python scripts/validate_install.py
```

## Best Practices

### Installation Management

- Always check if pymupdf4llm is installed before attempting to use it
- For scanned PDFs or complex layouts, recommend the `[full]` installation
- If OCR is needed, verify Tesseract is installed on the system

### Error Handling

- Wrap PDF operations in try-except blocks to handle corrupted files
- Check file existence before processing
- Validate page numbers are within document bounds
- Provide clear error messages when operations fail

### Performance Considerations

- For large PDFs (>100 pages), inform the user processing may take time
- Consider processing pages in batches for very large documents
- When batch processing, use progress indicators

### Output Quality

- The Markdown output preserves document structure, but complex layouts may need manual review
- Tables and images are handled, but complex formatting might not be perfect
- For critical documents, recommend spot-checking the output

### Memory Management

- For very large PDFs, consider processing in chunks
- Close PyMuPDF document objects when done to free memory
- When batch processing, process files sequentially rather than loading all at once

## Troubleshooting

### Common Issues

**Import Error**: If `import pymupdf4llm` fails, install the package:
```bash
pip install pymupdf4llm
```

**Poor OCR Results**: For scanned PDFs, ensure the full installation with OCR support:
```bash
pip install pymupdf4llm[full]
```

**Missing Layout Features**: Install pymupdf-layout for better structure detection:
```bash
pip install pymupdf-layout
```

**Memory Issues with Large PDFs**: Process pages in smaller batches or use selective page extraction.

## Reference Documentation

For detailed information, see:

- `references/api_reference.md` - Complete API documentation
- `references/examples.md` - More usage examples and patterns
- `references/rag_integration.md` - Integrating with RAG systems

## Output Format

The Markdown output from pymupdf4llm includes:

- Headers identified by font size, prefixed with `#` tags
- Paragraphs separated by blank lines
- Lists and bullet points preserved
- Tables converted to Markdown table format
- Document structure maintained for better LLM comprehension

This format is specifically optimized for LLM consumption, making it ideal for:
- RAG system document ingestion
- LLM context preparation
- Document Q&A systems
- Semantic search applications

## Example Interaction

**User**: "I have a research paper in PDF format. Can you extract the text so I can analyze it?"

**Your Response**:
1. Ask for the PDF file path
2. Check if pymupdf4llm is installed
3. Extract the content: `md_text = pymupdf4llm.to_markdown("paper.pdf")`
4. Save to a Markdown file or display the content
5. Offer to help with further analysis of the extracted text

**User**: "I need to process all PDFs in my documents folder for my RAG system."

**Your Response**:
1. Confirm the directory path
2. Use the batch processing script
3. Process all PDFs to Markdown format
4. Provide a summary of results
5. Suggest next steps for RAG integration (chunking, embedding, etc.)
