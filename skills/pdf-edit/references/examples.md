# PyMuPDF PDF Editing Examples

## Example 1: Merge Multiple PDFs

```python
import fitz
from pathlib import Path


def merge_pdfs(pdf_files: list[str], output_path: str) -> None:
    """Merge multiple PDF files into one."""
    result = fitz.open()
    for pdf_file in pdf_files:
        doc = fitz.open(pdf_file)
        result.insert_pdf(doc)
        doc.close()
    result.save(output_path, garbage=4, deflate=True)
    result.close()
    print(f"Merged {len(pdf_files)} files -> {output_path}")


merge_pdfs(["part1.pdf", "part2.pdf", "part3.pdf"], "merged.pdf")
```

## Example 2: Split PDF into Individual Pages

```python
import fitz
from pathlib import Path


def split_pdf(input_path: str, output_dir: str) -> None:
    """Split a PDF into individual page files."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    doc = fitz.open(input_path)
    for i in range(len(doc)):
        out = fitz.open()
        out.insert_pdf(doc, from_page=i, to_page=i)
        out.save(f"{output_dir}/page_{i+1}.pdf")
        out.close()
    doc.close()
    print(f"Split into {len(doc)} pages in {output_dir}/")


split_pdf("document.pdf", "pages_output")
```

## Example 3: Split PDF by Page Ranges

```python
import fitz


def split_by_ranges(input_path: str, ranges: list[tuple[int, int]], output_prefix: str) -> None:
    """Split PDF by page ranges (0-based)."""
    doc = fitz.open(input_path)
    for idx, (start, end) in enumerate(ranges):
        out = fitz.open()
        out.insert_pdf(doc, from_page=start, to_page=end)
        out.save(f"{output_prefix}_{idx+1}.pdf")
        out.close()
    doc.close()


# Split: pages 1-3, 4-6, 7-10 (0-based)
split_by_ranges("report.pdf", [(0, 2), (3, 5), (6, 9)], "section")
```

## Example 4: Add Text Watermark (Diagonal)

```python
import fitz


def add_text_watermark(input_path: str, output_path: str, text: str) -> None:
    """Add a diagonal text watermark to every page."""
    doc = fitz.open(input_path)
    for page in doc:
        rect = page.rect
        # Insert semi-transparent diagonal text
        tw = fitz.TextWriter(page.rect)
        page.insert_text(
            fitz.Point(rect.width / 4, rect.height / 2),
            text,
            fontsize=60,
            color=(0.8, 0.8, 0.8),
            rotate=45,
        )
    doc.save(output_path)
    doc.close()


add_text_watermark("input.pdf", "watermarked.pdf", "CONFIDENTIAL")
```

## Example 5: Add Image Watermark (Logo)

```python
import fitz


def add_image_watermark(input_path: str, output_path: str, image_path: str, opacity: float = 0.3) -> None:
    """Add an image watermark to every page."""
    doc = fitz.open(input_path)
    for page in doc:
        rect = page.rect
        # Place logo in bottom-right corner
        img_rect = fitz.Rect(
            rect.width - 150,
            rect.height - 80,
            rect.width - 20,
            rect.height - 20,
        )
        page.insert_image(img_rect, filename=image_path, overlay=True)
    doc.save(output_path)
    doc.close()


add_image_watermark("input.pdf", "logo_watermarked.pdf", "logo.png")
```

## Example 6: Add Page Numbers

```python
import fitz


def add_page_numbers(input_path: str, output_path: str, fmt: str = "Page {n} of {total}") -> None:
    """Add page numbers to the bottom center of each page."""
    doc = fitz.open(input_path)
    total = len(doc)
    for i, page in enumerate(doc):
        rect = page.rect
        text = fmt.format(n=i + 1, total=total)
        point = fitz.Point(rect.width / 2 - 40, rect.height - 30)
        page.insert_text(point, text, fontsize=10, color=(0.4, 0.4, 0.4))
    doc.save(output_path)
    doc.close()


add_page_numbers("report.pdf", "numbered.pdf")
```

## Example 7: Rotate Specific Pages

```python
import fitz


def rotate_pages(input_path: str, output_path: str, pages: list[int], angle: int = 90) -> None:
    """Rotate specific pages by the given angle."""
    doc = fitz.open(input_path)
    for pno in pages:
        if 0 <= pno < len(doc):
            doc[pno].set_rotation(angle)
    doc.save(output_path)
    doc.close()


# Rotate pages 1 and 3 (0-based) by 90 degrees
rotate_pages("input.pdf", "rotated.pdf", [0, 2], 90)
```

## Example 8: Encrypt PDF

```python
import fitz


def encrypt_pdf(input_path: str, output_path: str, user_pw: str, owner_pw: str) -> None:
    """Encrypt a PDF with AES-256."""
    doc = fitz.open(input_path)
    doc.save(
        output_path,
        encryption=fitz.PDF_ENCRYPT_AES_256,
        owner_pw=owner_pw,
        user_pw=user_pw,
        permissions=fitz.PDF_PERM_PRINT,
    )
    doc.close()


encrypt_pdf("input.pdf", "secured.pdf", "user123", "owner456")
```

## Example 9: Decrypt PDF

```python
import fitz


def decrypt_pdf(input_path: str, output_path: str, password: str) -> None:
    """Decrypt an encrypted PDF."""
    doc = fitz.open(input_path)
    if doc.is_encrypted:
        if not doc.authenticate(password):
            raise ValueError("Invalid password")
    doc.save(output_path, encryption=fitz.PDF_ENCRYPT_NONE)
    doc.close()


decrypt_pdf("secured.pdf", "decrypted.pdf", "user123")
```

## Example 10: Delete Pages

```python
import fitz


def delete_pages(input_path: str, output_path: str, pages_to_delete: list[int]) -> None:
    """Delete specific pages from a PDF (0-based page numbers)."""
    doc = fitz.open(input_path)
    # Delete in reverse order to preserve indices
    for pno in sorted(pages_to_delete, reverse=True):
        if 0 <= pno < len(doc):
            doc.delete_pages(pno)
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()


delete_pages("input.pdf", "trimmed.pdf", [0, 5, 10])
```

## Example 11: Add Highlight Annotations

```python
import fitz


def highlight_text(input_path: str, output_path: str, search_text: str) -> None:
    """Highlight all occurrences of a text string."""
    doc = fitz.open(input_path)
    count = 0
    for page in doc:
        instances = page.search_for(search_text)
        for inst in instances:
            page.add_highlight_annot(inst)
            count += 1
    doc.save(output_path)
    doc.close()
    print(f"Highlighted {count} occurrences of '{search_text}'")


highlight_text("paper.pdf", "highlighted.pdf", "important")
```

## Example 12: Set PDF Metadata

```python
import fitz


def set_metadata(input_path: str, output_path: str, title: str, author: str) -> None:
    """Set PDF document metadata."""
    doc = fitz.open(input_path)
    doc.set_metadata({
        "title": title,
        "author": author,
        "subject": "",
        "creator": "PyMuPDF Script",
    })
    doc.save(output_path)
    doc.close()


set_metadata("input.pdf", "output.pdf", "My Report", "Author Name")
```

## Example 13: Insert a Blank Page

```python
import fitz


def insert_blank_page(input_path: str, output_path: str, position: int) -> None:
    """Insert a blank A4 page at the given position."""
    doc = fitz.open(input_path)
    doc.new_page(pno=position, width=595, height=842)
    doc.save(output_path)
    doc.close()


# Insert blank page at the beginning
insert_blank_page("input.pdf", "with_blank.pdf", 0)
```

## Example 14: Reorder Pages

```python
import fitz


def reorder_pages(input_path: str, output_path: str, new_order: list[int]) -> None:
    """Reorder pages according to the given order (0-based)."""
    doc = fitz.open(input_path)
    doc.select(new_order)
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()


# Reverse page order for a 5-page document
reorder_pages("input.pdf", "reordered.pdf", [4, 3, 2, 1, 0])
```
