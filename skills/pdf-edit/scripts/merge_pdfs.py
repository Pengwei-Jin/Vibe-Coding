#!/usr/bin/env python3
"""Merge multiple PDF files into one using PyMuPDF.

Usage:
    python merge_pdfs.py file1.pdf file2.pdf [file3.pdf ...] -o merged.pdf

Arguments:
    files       PDF files to merge (in order)
    -o/--output Output file path
"""

import argparse
import sys

try:
    import fitz
except ImportError:
    print("Error: PyMuPDF is not installed.")
    print("Install it with: pip install pymupdf")
    sys.exit(1)


def merge_pdfs(pdf_files: list[str], output_path: str) -> None:
    result = fitz.open()
    total_pages = 0

    for pdf_file in pdf_files:
        try:
            doc = fitz.open(pdf_file)
            result.insert_pdf(doc)
            total_pages += len(doc)
            print(f"  Added: {pdf_file} ({len(doc)} pages)")
            doc.close()
        except Exception as e:
            print(f"  Error processing {pdf_file}: {e}")

    result.save(output_path, garbage=4, deflate=True)
    result.close()
    print(f"\nMerged -> {output_path} ({total_pages} pages)")


def main():
    parser = argparse.ArgumentParser(description="Merge multiple PDF files")
    parser.add_argument("files", nargs="+", help="PDF files to merge")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    for f in args.files:
        from pathlib import Path
        if not Path(f).exists():
            print(f"Error: File '{f}' does not exist.")
            sys.exit(1)

    print(f"Merging {len(args.files)} PDF file(s)...")
    merge_pdfs(args.files, args.output)


if __name__ == "__main__":
    main()
