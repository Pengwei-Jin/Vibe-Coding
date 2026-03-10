#!/usr/bin/env python3
"""Batch convert PDF files to Markdown using pymupdf4llm.

Usage:
    python batch_convert.py <input_dir> <output_dir> [--pages 0,1,2]

Arguments:
    input_dir   Directory containing PDF files
    output_dir  Directory to save Markdown output
    --pages     Optional comma-separated list of 0-based page numbers
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


def parse_pages(pages_str: str) -> list[int] | None:
    if not pages_str:
        return None
    pages = []
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return sorted(set(pages))


def convert_pdf(pdf_path: Path, output_dir: Path, pages: list[int] | None = None) -> bool:
    try:
        kwargs = {}
        if pages is not None:
            kwargs["pages"] = pages

        md_text = pymupdf4llm.to_markdown(str(pdf_path), **kwargs)

        output_file = output_dir / f"{pdf_path.stem}.md"
        output_file.write_bytes(md_text.encode())
        return True
    except Exception as e:
        print(f"  Error processing {pdf_path.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Batch convert PDFs to Markdown")
    parser.add_argument("input_dir", type=Path, help="Directory containing PDF files")
    parser.add_argument("output_dir", type=Path, help="Directory for Markdown output")
    parser.add_argument("--pages", type=str, default=None, help="Comma-separated page numbers or ranges (e.g., 0,1,2 or 0-5,10)")
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    pages = parse_pages(args.pages)

    pdf_files = sorted(args.input_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in '{args.input_dir}'.")
        sys.exit(0)

    print(f"Found {len(pdf_files)} PDF file(s) to process.")
    if pages:
        print(f"Extracting pages: {pages}")

    success = 0
    failed = 0

    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
        if convert_pdf(pdf_path, args.output_dir, pages):
            success += 1
            print(f"  -> Saved: {pdf_path.stem}.md")
        else:
            failed += 1

    print(f"\nDone. Success: {success}, Failed: {failed}")


if __name__ == "__main__":
    main()
