#!/usr/bin/env python3
"""Validate PyMuPDF installation for PDF editing.

Usage:
    python validate_install.py
"""

import sys


def check_import(module_name: str, package_name: str = None) -> bool:
    package_name = package_name or module_name
    try:
        mod = __import__(module_name)
        version = getattr(mod, "__version__", getattr(mod, "version", "unknown"))
        print(f"✓ {package_name} is installed (version: {version})")
        return True
    except ImportError:
        print(f"✗ {package_name} is NOT installed")
        return False


def main():
    print("Checking PyMuPDF installation for PDF editing...\n")

    print("Core dependency:")
    ok = check_import("fitz", "PyMuPDF")
    if not ok:
        print("  Install with: pip install pymupdf")

    print("\nOptional dependencies:")
    has_pil = check_import("PIL", "Pillow")
    if not has_pil:
        print("  Install with: pip install Pillow")
        print("  (Useful for image preprocessing before inserting into PDFs)")

    print("\nInstallation command:")
    print("  pip install pymupdf")

    if ok:
        print("\n✓ Core installation is complete! PDF editing is ready.")
        return 0
    else:
        print("\n✗ Installation incomplete. Please install missing packages.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
