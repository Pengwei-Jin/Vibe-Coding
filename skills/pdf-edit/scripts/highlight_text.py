#!/usr/bin/env python3
"""Highlight text in a PDF and optionally add comments."""

import argparse
import fitz


def highlight_text(input_path: str, output_path: str, text: str, 
                   color: tuple = (1, 0, 0)) -> int:
    """Highlight all occurrences of text in a PDF.
    
    Args:
        input_path: Path to input PDF
        output_path: Path to output PDF
        text: Text to highlight
        color: RGB color tuple (default: red)
    
    Returns:
        Number of highlights added
    """
    doc = fitz.open(input_path)
    count = 0
    
    for page in doc:
        areas = page.search_for(text)
        for area in areas:
            annot = page.add_highlight_annot(area)
            annot.set_colors({"stroke": color})
            annot.update()
            count += 1
    
    doc.save(output_path)
    doc.close()
    return count


def highlight_with_comment(input_path: str, output_path: str, text: str, 
                           comment: str, color: tuple = (1, 0.5, 0)) -> int:
    """Highlight text and add a comment annotation next to it.
    
    Args:
        input_path: Path to input PDF
        output_path: Path to output PDF
        text: Text to highlight
        comment: Comment to add
        color: RGB color tuple (default: orange)
    
    Returns:
        Number of highlights added
    """
    doc = fitz.open(input_path)
    count = 0
    
    for page in doc:
        areas = page.search_for(text)
        for area in areas:
            # Highlight
            annot = page.add_highlight_annot(area)
            annot.set_colors({"stroke": color})
            annot.update()
            
            # Add comment
            comment_point = fitz.Point(area.x1 + 10, area.y0)
            text_annot = page.add_text_annot(comment_point, comment)
            text_annot.update()
            count += 1
    
    doc.save(output_path)
    doc.close()
    return count


def main():
    parser = argparse.ArgumentParser(description="Highlight text in PDF")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("-o", "--output", required=True, help="Output PDF file")
    parser.add_argument("-t", "--text", required=True, help="Text to highlight")
    parser.add_argument("-c", "--comment", help="Comment to add next to highlight")
    parser.add_argument("--color", nargs=3, type=float, default=[1, 0, 0],
                        metavar=("R", "G", "B"), help="RGB color (0-1), default: red")
    
    args = parser.parse_args()
    color = tuple(args.color)
    
    if args.comment:
        count = highlight_with_comment(args.input, args.output, args.text, 
                                       args.comment, color)
        print(f"Added {count} highlights with comments")
    else:
        count = highlight_text(args.input, args.output, args.text, color)
        print(f"Added {count} highlights")


if __name__ == "__main__":
    main()