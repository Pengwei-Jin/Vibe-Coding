#!/usr/bin/env python3
"""Extract specific pages from a PDF to Markdown.

Usage:
    python extract_pages.py <input.pdf> <output.md> --pages 0-5,10,15-20

Arguments:
    input.pdf   Input PDF file
    output.md   Output Markdown file
    --pages     Page specification (0-based): ranges (0-5) or individual (10) or mixed (0-5,10,15-20)
"""

import argparse
import sys
from pathlib import Path

try:
    import pymupdf4llm
except ImportError:
    print("Error: pymupdf4llm is not installed.")
    print("Install it with: pip install pymupdf4llm")
    sys.exit(1)


def parse_pages(pages_str: str) -> list[int]:
    pages = []
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return sorted(set(pages))


def main():
    parser = argparse.ArgumentParser(description="Extract specific pages from PDF to Markdown")
    parser.add_argument("input_pdf", type=Path, help="Input PDF file")
    parser.add_argument("output_md", type=Path, help="Output Markdown file")
    parser.add_argument("--pages", type=str, required=True, help="Page specification (e.g., 0-5,10,15-20)")
    args = parser.parse_args()

    if not args.input_pdf.exists():
        print(f"Error: Input file '{args.input_pdf}' does not exist.")
        sys.exit(1)

    pages = parse_pages(args.pages)
    print(f"Extracting pages: {pages}")

    try:
        md_text = pymupdf4llm.to_markdown(str(args.input_pdf), pages=pages)
        args.output_md.write_bytes(md_text.encode())
        print(f"Successfully extracted {len(pages)} page(s) to '{args.output_md}'")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
