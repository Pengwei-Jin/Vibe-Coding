---
name: pdf-edit
description: Edit and manipulate PDF documents using PyMuPDF (fitz). Use this skill when users need to merge, split, rotate, add watermarks, insert text or images, encrypt/decrypt, add annotations, or perform any PDF modification tasks. Also trigger when users mention editing PDFs, combining PDFs, securing PDFs, or adding content to existing PDF files.
---

# PDF Edit Skill

This skill helps you edit and manipulate PDF documents using the PyMuPDF library (imported as `fitz`). PyMuPDF provides comprehensive PDF editing capabilities including merging, splitting, watermarking, text/image insertion, encryption, and more.

## When to Use This Skill

Use this skill when the user needs to:

- Merge multiple PDF files into one
- Split a PDF into separate files
- Rotate PDF pages
- Add text or image watermarks
- Insert text, images, or vector graphics into PDF pages
- Encrypt or decrypt PDF files
- Add or remove annotations
- Delete, reorder, or duplicate pages
- Add headers, footers, or page numbers
- Redact sensitive content
- Modify PDF metadata

## Installation

```bash
pip install pymupdf
```

Verify installation:

```bash
python scripts/validate_install.py
```

## Basic Usage Patterns

### Open and Save a PDF

```python
import fitz  # PyMuPDF

doc = fitz.open("input.pdf")
# ... perform edits ...
doc.save("output.pdf")
doc.close()
```

### Merge PDFs

```python
import fitz

result = fitz.open()  # new empty PDF
for pdf_file in ["file1.pdf", "file2.pdf", "file3.pdf"]:
    doc = fitz.open(pdf_file)
    result.insert_pdf(doc)
    doc.close()
result.save("merged.pdf")
result.close()
```

### Split PDF by Pages

```python
import fitz

doc = fitz.open("input.pdf")
for i in range(len(doc)):
    out = fitz.open()
    out.insert_pdf(doc, from_page=i, to_page=i)
    out.save(f"page_{i+1}.pdf")
    out.close()
doc.close()
```

### Rotate Pages

```python
import fitz

doc = fitz.open("input.pdf")
for page in doc:
    page.set_rotation(90)  # 90, 180, 270
doc.save("rotated.pdf")
doc.close()
```

### Add Text Watermark

```python
import fitz

doc = fitz.open("input.pdf")
for page in doc:
    rect = page.rect
    text = "CONFIDENTIAL"
    point = fitz.Point(rect.width / 2 - 100, rect.height / 2)
    page.insert_text(
        point,
        text,
        fontsize=60,
        color=(0.75, 0.75, 0.75),
        rotate=45,
    )
doc.save("watermarked.pdf")
doc.close()
```

### Insert Image

```python
import fitz

doc = fitz.open("input.pdf")
page = doc[0]
img_rect = fitz.Rect(50, 50, 200, 150)
page.insert_image(img_rect, filename="logo.png")
doc.save("with_image.pdf")
doc.close()
```

### Encrypt PDF

```python
import fitz

doc = fitz.open("input.pdf")
doc.save(
    "encrypted.pdf",
    encryption=fitz.PDF_ENCRYPT_AES_256,
    owner_pw="owner_password",
    user_pw="user_password",
    permissions=fitz.PDF_PERM_PRINT,
)
doc.close()
```

### Decrypt PDF

```python
import fitz

doc = fitz.open("encrypted.pdf")
if doc.is_encrypted:
    doc.authenticate("user_password")
doc.save("decrypted.pdf", encryption=fitz.PDF_ENCRYPT_NONE)
doc.close()
```

## Common Workflows

### Workflow 1: Merge Multiple PDFs

1. Collect all PDF file paths
2. Create a new empty PDF document
3. Insert each PDF sequentially using `insert_pdf()`
4. Save the merged result
5. Report page count summary

### Workflow 2: Split PDF

1. Open the source PDF
2. Determine split strategy (by page, by range, by bookmark)
3. Create new documents for each split
4. Save each part separately
5. Provide summary of output files

### Workflow 3: Add Watermark to All Pages

1. Open the PDF
2. Determine watermark type (text or image)
3. Calculate position (center, corner, etc.)
4. Apply watermark to each page
5. Save with a new filename to preserve original

### Workflow 4: Secure a PDF

1. Open the PDF
2. Set encryption method (AES-256 recommended)
3. Set owner and user passwords
4. Configure permissions (print, copy, modify)
5. Save the encrypted file

### Workflow 5: Add Page Numbers

1. Open the PDF
2. For each page, calculate footer position
3. Insert page number text (e.g., "Page 1 of N")
4. Save the result

## Helper Scripts

### merge_pdfs.py

Merge multiple PDF files into one.

```bash
python scripts/merge_pdfs.py file1.pdf file2.pdf -o merged.pdf
```

### add_watermark.py

Add text or image watermark to a PDF.

```bash
python scripts/add_watermark.py input.pdf -t "CONFIDENTIAL" -o watermarked.pdf
python scripts/add_watermark.py input.pdf -i logo.png -o watermarked.pdf
```

### validate_install.py

Check if PyMuPDF is properly installed.

```bash
python scripts/validate_install.py
```

## Best Practices

### File Safety

- Always save to a new file rather than overwriting the original
- Validate input files exist before processing
- Use try-except blocks for all PDF operations

### Performance

- Close documents after use to free memory
- For large merges, process sequentially rather than loading all at once
- Use `doc.save(..., garbage=4, deflate=True)` to optimize file size

### Security

- Use AES-256 encryption for sensitive documents
- Set appropriate permissions when encrypting
- Never log or expose passwords in code

### Coordinate System

- PyMuPDF uses a coordinate system with origin (0,0) at the top-left
- X-axis extends right, Y-axis extends down
- Use `page.rect` to get page dimensions
- Use `fitz.Rect(x0, y0, x1, y1)` to define rectangular areas

## Troubleshooting

**Import Error**: If `import fitz` fails:
```bash
pip install pymupdf
```

**Encrypted PDF**: If operations fail on an encrypted PDF:
```python
doc = fitz.open("file.pdf")
if doc.is_encrypted:
    doc.authenticate("password")
```

**Large File Size After Edit**: Optimize on save:
```python
doc.save("output.pdf", garbage=4, deflate=True)
```

## Reference Documentation

- `references/api_reference.md` - Complete API documentation for editing operations
- `references/examples.md` - More usage examples and patterns
- `references/advanced_editing.md` - Advanced editing techniques (annotations, redaction, metadata)
