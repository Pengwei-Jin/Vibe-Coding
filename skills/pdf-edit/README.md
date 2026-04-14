# PDF Edit Skill

A skill for editing and manipulating PDF documents using PyMuPDF (fitz), supporting merge, split, watermark, encryption, and more.

## Structure

```
pdf-edit/
├── SKILL.md                    # Main skill documentation
├── scripts/                    # Helper scripts
│   ├── merge_pdfs.py          # Merge multiple PDFs
│   ├── add_watermark.py       # Add text/image watermark
│   ├── highlight_text.py      # Highlight text with comments
│   └── validate_install.py    # Validate installation
├── references/                 # Reference documentation
│   ├── api_reference.md       # API documentation
│   ├── examples.md            # Usage examples
│   └── advanced_editing.md    # Advanced editing guide
└── evals/                      # Test cases
    └── evals.json             # Evaluation prompts
```

## Installation

```bash
pip install pymupdf
```

## Quick Start

### Merge PDFs

```bash
python scripts/merge_pdfs.py file1.pdf file2.pdf -o merged.pdf
```

### Add Watermark

```bash
python scripts/add_watermark.py input.pdf -t "CONFIDENTIAL" -o watermarked.pdf
```

### Highlight Text

```bash
python scripts/highlight_text.py input.pdf -t "error" -o highlighted.pdf
python scripts/highlight_text.py input.pdf -t "error" -c "Fix this" -o annotated.pdf
```

### Edit in Python

```python
import fitz

doc = fitz.open("input.pdf")
page = doc[0]
page.insert_text(fitz.Point(100, 100), "Hello World", fontsize=20)
doc.save("output.pdf")
doc.close()
```

## Features

- Merge multiple PDFs into one
- Split PDF into separate files
- Rotate pages
- Add text or image watermarks
- Insert text, images, and graphics
- Encrypt and decrypt PDFs
- Add highlights and comments/annotations
- Add page numbers, headers, footers
- Manage annotations and redactions
- Modify PDF metadata

## Documentation

- See `SKILL.md` for complete usage instructions
- See `references/api_reference.md` for API details
- See `references/examples.md` for code examples
- See `references/advanced_editing.md` for advanced editing techniques
