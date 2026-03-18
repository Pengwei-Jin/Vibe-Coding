#!/usr/bin/env python3
"""Add text or image watermark to a PDF using PyMuPDF.

Usage:
    python add_watermark.py input.pdf -t "CONFIDENTIAL" -o watermarked.pdf
    python add_watermark.py input.pdf -i logo.png -o watermarked.pdf

Arguments:
    input_pdf       Input PDF file
    -t/--text       Text watermark content
    -i/--image      Image watermark file path
    -o/--output     Output file path
    --fontsize      Font size for text watermark (default: 50)
    --opacity       Color intensity 0-1 for text watermark (default: 0.8)
    --rotate        Rotation angle for text watermark (default: 45)
"""

import argparse
import sys

try:
    import fitz
except ImportError:
    print("Error: PyMuPDF is not installed.")
    print("Install it with: pip install pymupdf")
    sys.exit(1)


def add_text_watermark(input_path: str, output_path: str, text: str,
                       fontsize: float = 50, opacity: float = 0.8, rotate: int = 45) -> None:
    doc = fitz.open(input_path)
    gray = opacity
    for page in doc:
        rect = page.rect
        point = fitz.Point(rect.width / 4, rect.height / 2)
        page.insert_text(
            point,
            text,
            fontsize=fontsize,
            color=(gray, gray, gray),
            rotate=rotate,
        )
    doc.save(output_path)
    doc.close()
    print(f"Text watermark added -> {output_path} ({len(doc)} pages)")


def add_image_watermark(input_path: str, output_path: str, image_path: str) -> None:
    doc = fitz.open(input_path)
    for page in doc:
        rect = page.rect
        img_rect = fitz.Rect(
            rect.width - 150,
            rect.height - 80,
            rect.width - 20,
            rect.height - 20,
        )
        page.insert_image(img_rect, filename=image_path, overlay=True)
    doc.save(output_path)
    doc.close()
    print(f"Image watermark added -> {output_path} ({len(doc)} pages)")


def main():
    parser = argparse.ArgumentParser(description="Add watermark to PDF")
    parser.add_argument("input_pdf", help="Input PDF file")
    parser.add_argument("-t", "--text", help="Text watermark content")
    parser.add_argument("-i", "--image", help="Image watermark file path")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    parser.add_argument("--fontsize", type=float, default=50, help="Font size (default: 50)")
    parser.add_argument("--opacity", type=float, default=0.8, help="Gray level 0-1 (default: 0.8)")
    parser.add_argument("--rotate", type=int, default=45, help="Rotation angle (default: 45)")
    args = parser.parse_args()

    from pathlib import Path
    if not Path(args.input_pdf).exists():
        print(f"Error: File '{args.input_pdf}' does not exist.")
        sys.exit(1)

    if not args.text and not args.image:
        print("Error: Specify either --text or --image for watermark.")
        sys.exit(1)

    if args.text:
        add_text_watermark(args.input_pdf, args.output, args.text,
                           args.fontsize, args.opacity, args.rotate)
    elif args.image:
        if not Path(args.image).exists():
            print(f"Error: Image file '{args.image}' does not exist.")
            sys.exit(1)
        add_image_watermark(args.input_pdf, args.output, args.image)


if __name__ == "__main__":
    main()
