# Advanced PDF Editing with PyMuPDF

## Redacting Sensitive Content

Redaction permanently removes content from a PDF, unlike annotations which can be removed.

### Text Redaction

```python
import fitz


def redact_text(input_path: str, output_path: str, search_text: str) -> None:
    """Permanently redact all occurrences of a text string."""
    doc = fitz.open(input_path)
    count = 0
    for page in doc:
        instances = page.search_for(search_text)
        for inst in instances:
            page.add_redact_annot(inst, fill=(0, 0, 0))
            count += 1
        page.apply_redactions()
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    print(f"Redacted {count} occurrences")


redact_text("contract.pdf", "redacted.pdf", "[email]")
```

### Area Redaction

```python
import fitz


def redact_area(input_path: str, output_path: str, page_num: int, rect: tuple) -> None:
    """Redact a rectangular area on a specific page."""
    doc = fitz.open(input_path)
    page = doc[page_num]
    r = fitz.Rect(*rect)
    page.add_redact_annot(r, fill=(0, 0, 0))
    page.apply_redactions()
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()


redact_area("form.pdf", "redacted_form.pdf", 0, (100, 200, 300, 230))
```

---

## Drawing Shapes and Graphics

### Draw Lines, Rectangles, Circles

```python
import fitz


def draw_shapes(input_path: str, output_path: str) -> None:
    """Draw various shapes on the first page."""
    doc = fitz.open(input_path)
    page = doc[0]
    shape = page.new_shape()

    # Draw a rectangle
    shape.draw_rect(fitz.Rect(50, 50, 200, 150))
    shape.finish(color=(1, 0, 0), width=2)

    # Draw a circle
    shape.draw_circle(fitz.Point(300, 100), 50)
    shape.finish(color=(0, 0, 1), fill=(0.8, 0.8, 1), width=1.5)

    # Draw a line
    shape.draw_line(fitz.Point(50, 200), fitz.Point(500, 200))
    shape.finish(color=(0, 0.5, 0), width=1)

    shape.commit()
    doc.save(output_path)
    doc.close()


draw_shapes("input.pdf", "with_shapes.pdf")
```

---

## Working with Table of Contents (TOC)

### Read TOC

```python
import fitz


def get_toc(input_path: str) -> list:
    """Get the table of contents."""
    doc = fitz.open(input_path)
    toc = doc.get_toc()
    doc.close()
    return toc  # list of [level, title, page_number]


toc = get_toc("book.pdf")
for level, title, page in toc:
    indent = "  " * (level - 1)
    print(f"{indent}{title} (page {page})")
```

### Set TOC

```python
import fitz


def set_toc(input_path: str, output_path: str, toc: list) -> None:
    """Set a custom table of contents."""
    doc = fitz.open(input_path)
    doc.set_toc(toc)
    doc.save(output_path)
    doc.close()


toc = [
    [1, "Chapter 1: Introduction", 1],
    [2, "1.1 Background", 2],
    [2, "1.2 Objectives", 5],
    [1, "Chapter 2: Methods", 8],
    [2, "2.1 Data Collection", 9],
]
set_toc("report.pdf", "with_toc.pdf", toc)
```

---

## Stamping and Overlaying PDFs

### Overlay One PDF on Another

```python
import fitz


def overlay_pdf(base_path: str, overlay_path: str, output_path: str) -> None:
    """Overlay pages from one PDF onto another (e.g., letterhead)."""
    base = fitz.open(base_path)
    overlay = fitz.open(overlay_path)

    for i in range(len(base)):
        if i < len(overlay):
            base[i].show_pdf_page(base[i].rect, overlay, i)

    base.save(output_path)
    base.close()
    overlay.close()


overlay_pdf("content.pdf", "letterhead.pdf", "final.pdf")
```

---

## Extracting and Replacing Images

### List All Images in a PDF

```python
import fitz


def list_images(input_path: str) -> None:
    """List all images in a PDF."""
    doc = fitz.open(input_path)
    for i, page in enumerate(doc):
        images = page.get_images(full=True)
        for img in images:
            xref = img[0]
            print(f"Page {i+1}: xref={xref}, size={img[2]}x{img[3]}")
    doc.close()


list_images("document.pdf")
```

### Extract Images

```python
import fitz
from pathlib import Path


def extract_images(input_path: str, output_dir: str) -> None:
    """Extract all images from a PDF."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    doc = fitz.open(input_path)
    count = 0
    for i, page in enumerate(doc):
        images = page.get_images(full=True)
        for img_idx, img in enumerate(images):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n >= 5:  # CMYK
                pix = fitz.Pixmap(fitz.csRGB, pix)
            pix.save(f"{output_dir}/page{i+1}_img{img_idx+1}.png")
            pix = None
            count += 1
    doc.close()
    print(f"Extracted {count} images to {output_dir}/")


extract_images("document.pdf", "extracted_images")
```

---

## Batch Operations

### Batch Add Watermark to Directory

```python
import fitz
from pathlib import Path


def batch_watermark(input_dir: str, output_dir: str, text: str) -> None:
    """Add watermark to all PDFs in a directory."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    pdf_files = sorted(Path(input_dir).glob("*.pdf"))

    for pdf_file in pdf_files:
        doc = fitz.open(str(pdf_file))
        for page in doc:
            rect = page.rect
            page.insert_text(
                fitz.Point(rect.width / 4, rect.height / 2),
                text,
                fontsize=50,
                color=(0.85, 0.85, 0.85),
                rotate=45,
            )
        out_path = Path(output_dir) / pdf_file.name
        doc.save(str(out_path))
        doc.close()
        print(f"Watermarked: {pdf_file.name}")


batch_watermark("input_pdfs/", "watermarked_pdfs/", "DRAFT")
```

---

## Creating PDFs from Scratch

### Create a Simple PDF

```python
import fitz


def create_pdf(output_path: str, title: str, content: str) -> None:
    """Create a simple PDF with title and content."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4

    # Title
    page.insert_text(fitz.Point(72, 72), title, fontsize=24, color=(0, 0, 0))

    # Content
    rect = fitz.Rect(72, 120, 523, 770)
    page.insert_textbox(rect, content, fontsize=12, align=0)

    doc.set_metadata({"title": title, "creator": "PyMuPDF"})
    doc.save(output_path)
    doc.close()


create_pdf("new_doc.pdf", "My Document", "This is the content of my new PDF document.")
```

### Create Multi-Page PDF with Headers/Footers

```python
import fitz


def create_report(output_path: str, pages_content: list[str], title: str = "Report") -> None:
    """Create a multi-page PDF with headers and footers."""
    doc = fitz.open()
    total = len(pages_content)

    for i, content in enumerate(pages_content):
        page = doc.new_page(width=595, height=842)

        # Header
        page.insert_text(fitz.Point(72, 40), title, fontsize=10, color=(0.5, 0.5, 0.5))
        # Header line
        shape = page.new_shape()
        shape.draw_line(fitz.Point(72, 50), fitz.Point(523, 50))
        shape.finish(color=(0.8, 0.8, 0.8), width=0.5)
        shape.commit()

        # Content
        rect = fitz.Rect(72, 72, 523, 770)
        page.insert_textbox(rect, content, fontsize=11)

        # Footer
        footer = f"Page {i+1} of {total}"
        page.insert_text(fitz.Point(260, 820), footer, fontsize=9, color=(0.5, 0.5, 0.5))

    doc.save(output_path)
    doc.close()


create_report("report.pdf", ["Chapter 1 content...", "Chapter 2 content..."], "Annual Report")
```
