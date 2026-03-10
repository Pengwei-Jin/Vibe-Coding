# PyMuPDF4LLM Skill

A skill for extracting and converting PDF content to Markdown format using pymupdf4llm, optimized for LLM and RAG applications.

## Structure

```
pymupdf4llm-skill/
├── SKILL.md                    # Main skill documentation
├── scripts/                    # Helper scripts
│   ├── batch_convert.py       # Batch convert PDFs to Markdown
│   ├── extract_pages.py       # Extract specific pages
│   └── validate_install.py    # Validate installation
├── references/                 # Reference documentation
│   ├── api_reference.md       # API documentation
│   ├── examples.md            # Usage examples
│   └── rag_integration.md     # RAG integration guide
└── evals/                      # Test cases
    └── evals.json             # Evaluation prompts

## Installation

To use this skill, ensure pymupdf4llm is installed:

```bash
pip install pymupdf4llm
```

For full features (OCR, advanced layout):

```bash
pip install pymupdf4llm[full]
```

## Quick Start

### Single PDF Conversion

```python
import pymupdf4llm

md_text = pymupdf4llm.to_markdown("input.pdf")
```

### Batch Processing

```bash
python scripts/batch_convert.py input_dir/ output_dir/
```

### Extract Specific Pages

```bash
python scripts/extract_pages.py input.pdf output.md --pages 0-5,10
```

## Features

- Convert PDF to Markdown format
- Extract specific pages
- Batch process multiple PDFs
- Preserve document structure
- Optimize for LLM/RAG consumption
- LlamaIndex integration support

## Use Cases

- Preparing PDFs for RAG systems
- Extracting research papers for analysis
- Converting documentation to Markdown
- Processing academic papers
- Building knowledge bases from PDF collections

## Documentation

- See `SKILL.md` for complete usage instructions
- See `references/api_reference.md` for API details
- See `references/examples.md` for code examples
- See `references/rag_integration.md` for RAG integration patterns
