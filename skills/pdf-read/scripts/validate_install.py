#!/usr/bin/env python3
"""Validate pymupdf4llm installation and dependencies.

Usage:
    python validate_install.py
"""

import sys


def check_import(module_name: str, package_name: str = None) -> bool:
    package_name = package_name or module_name
    try:
        __import__(module_name)
        print(f"✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name} is NOT installed")
        return False


def main():
    print("Checking pymupdf4llm installation...\n")

    all_ok = True

    # Core dependencies
    print("Core dependencies:")
    if not check_import("pymupdf4llm"):
        print("  Install with: pip install pymupdf4llm")
        all_ok = False

    if not check_import("pymupdf", "PyMuPDF"):
        print("  Install with: pip install pymupdf")
        all_ok = False

    print("\nOptional dependencies (for full features):")
    
    has_cv2 = check_import("cv2", "opencv-python")
    if not has_cv2:
        print("  Install with: pip install opencv-python")

    has_layout = check_import("pymupdf_layout", "pymupdf-layout")
    if not has_layout:
        print("  Install with: pip install pymupdf-layout")

    print("\nFull installation command:")
    print("  pip install pymupdf4llm[full]")

    if all_ok:
        print("\n✓ Core installation is complete!")
        if has_cv2 and has_layout:
            print("✓ All optional features are available!")
        else:
            print("⚠ Some optional features are missing (OCR, advanced layout)")
        return 0
    else:
        print("\n✗ Installation incomplete. Please install missing packages.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
