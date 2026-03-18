# PyMuPDF PDF Editing API Reference

## Core: Opening and Saving Documents

### `fitz.open(filename=None)`

Open an existing PDF or create a new empty document.

```python
import fitz

# Open existing PDF
doc = fitz.open("input.pdf")

# Create new empty PDF
doc = fitz.open()
```

### `Document.save(filename, **kwargs)`

Save the document.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filename` | `str` | (required) | Output file path |
| `garbage` | `int` | `0` | Garbage collection level (0-4). 4 = maximum compression |
| `deflate` | `bool` | `False` | Compress uncompressed streams |
| `encryption` | `int` | `PDF_ENCRYPT_NONE` | Encryption method |
| `owner_pw` | `str` | `None` | Owner password |
| `user_pw` | `str` | `None` | User password |
| `permissions` | `int` | `0xFFFF` | Permission flags |

```python
doc.save("output.pdf", garbage=4, deflate=True)
doc.close()
```

---

## Page Operations

### `Document.insert_pdf(src, from_page=-1, to_page=-1, start_at=-1)`

Insert pages from another PDF.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `src` | `Document` | (required) | Source PDF document |
| `from_page` | `int` | `-1` | First page to copy (-1 = first page) |
| `to_page` | `int` | `-1` | Last page to copy (-1 = last page) |
| `start_at` | `int` | `-1` | Position to insert at (-1 = end) |

```python
result = fitz.open()
src = fitz.open("source.pdf")
result.insert_pdf(src, from_page=0, to_page=4)
```

### `Document.delete_pages(*args)`

Delete pages from the document.

```python
doc.delete_pages(0)          # delete first page
doc.delete_pages(2, 5)       # delete pages 2 through 5
doc.delete_pages([0, 3, 7])  # delete specific pages
```

### `Document.move_page(pno, to=-1)`

Move a page within the document.

```python
doc.move_page(5, to=0)  # move page 5 to the beginning
```

### `Document.copy_page(pno, to=-1)`

Copy a page within the document.

```python
doc.copy_page(0, to=-1)  # copy first page to end
```

### `Page.set_rotation(value)`

Set page rotation. Value must be 0, 90, 180, or 270.

```python
page = doc[0]
page.set_rotation(90)
```

### `Document.new_page(pno=-1, width=595, height=842)`

Insert a new blank page.

```python
page = doc.new_page(pno=0, width=595, height=842)  # A4 at beginning
```

---

## Text Operations

### `Page.insert_text(point, text, **kwargs)`

Insert text at a specific point.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `point` | `Point` | (required) | Insertion point (x, y) |
| `text` | `str` | (required) | Text to insert |
| `fontsize` | `float` | `11` | Font size |
| `fontname` | `str` | `"helv"` | Font name (helv, cour, tiro, etc.) |
| `color` | `tuple` | `(0,0,0)` | RGB color, values 0-1 |
| `rotate` | `int` | `0` | Text rotation angle |

```python
page.insert_text(
    fitz.Point(72, 72),
    "Hello World",
    fontsize=16,
    color=(0, 0, 1),
)
```

### `Page.insert_textbox(rect, text, **kwargs)`

Insert text within a rectangular area with automatic line wrapping.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `rect` | `Rect` | (required) | Target rectangle |
| `text` | `str` | (required) | Text to insert |
| `fontsize` | `float` | `11` | Font size |
| `align` | `int` | `0` | 0=left, 1=center, 2=right, 3=justify |

```python
rect = fitz.Rect(72, 72, 500, 200)
page.insert_textbox(rect, "Long text content...", fontsize=12, align=1)
```

---

## Image Operations

### `Page.insert_image(rect, **kwargs)`

Insert an image into a rectangular area.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `rect` | `Rect` | (required) | Target rectangle |
| `filename` | `str` | `None` | Image file path |
| `pixmap` | `Pixmap` | `None` | Pixmap object |
| `stream` | `bytes` | `None` | Image bytes |

```python
rect = fitz.Rect(50, 50, 250, 200)
page.insert_image(rect, filename="image.png")
```

---

## Encryption and Decryption

### Encryption Constants

| Constant | Description |
|----------|-------------|
| `fitz.PDF_ENCRYPT_NONE` | No encryption |
| `fitz.PDF_ENCRYPT_RC4_40` | RC4 40-bit |
| `fitz.PDF_ENCRYPT_RC4_128` | RC4 128-bit |
| `fitz.PDF_ENCRYPT_AES_128` | AES 128-bit |
| `fitz.PDF_ENCRYPT_AES_256` | AES 256-bit (recommended) |

### Permission Constants

| Constant | Description |
|----------|-------------|
| `fitz.PDF_PERM_PRINT` | Allow printing |
| `fitz.PDF_PERM_MODIFY` | Allow modification |
| `fitz.PDF_PERM_COPY` | Allow copying text |
| `fitz.PDF_PERM_ANNOTATE` | Allow annotations |
| `fitz.PDF_PERM_FORM` | Allow form filling |

```python
# Encrypt
doc.save("encrypted.pdf",
    encryption=fitz.PDF_ENCRYPT_AES_256,
    owner_pw="owner123",
    user_pw="user123",
    permissions=fitz.PDF_PERM_PRINT | fitz.PDF_PERM_COPY,
)

# Decrypt
doc = fitz.open("encrypted.pdf")
doc.authenticate("user123")
doc.save("decrypted.pdf", encryption=fitz.PDF_ENCRYPT_NONE)
```

---

## Annotations

### `Page.add_text_annot(point, text)`

Add a sticky note annotation.

```python
page.add_text_annot(fitz.Point(100, 100), "Review this section")
```

### `Page.add_highlight_annot(quads)`

Highlight text on a page.

```python
text_instances = page.search_for("important")
for inst in text_instances:
    page.add_highlight_annot(inst)
```

### `Page.add_rect_annot(rect)`

Add a rectangle annotation.

```python
page.add_rect_annot(fitz.Rect(100, 100, 300, 200))
```

### `Page.delete_annot(annot)`

Delete an annotation.

```python
for annot in page.annots():
    if annot.type[1] == "Highlight":
        page.delete_annot(annot)
```

---

## Metadata

### `Document.metadata`

Get document metadata as a dictionary.

```python
meta = doc.metadata
print(meta["title"], meta["author"])
```

### `Document.set_metadata(metadata)`

Set document metadata.

```python
doc.set_metadata({
    "title": "My Document",
    "author": "Author Name",
    "subject": "Subject",
    "creator": "Python Script",
})
```

---

## Geometry Helpers

### `fitz.Point(x, y)`

A 2D point.

### `fitz.Rect(x0, y0, x1, y1)`

A rectangle defined by top-left and bottom-right corners.

### `Page.rect`

The page's rectangle (dimensions).

```python
page = doc[0]
width = page.rect.width
height = page.rect.height
```

---

## Error Handling

```python
import fitz

try:
    doc = fitz.open("file.pdf")
    if doc.is_encrypted:
        if not doc.authenticate("password"):
            raise ValueError("Invalid password")
    # ... edit operations ...
    doc.save("output.pdf")
except FileNotFoundError:
    print("PDF file not found")
except fitz.FileDataError:
    print("Invalid or corrupted PDF")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'doc' in locals():
        doc.close()
```
