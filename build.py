#!/usr/bin/env python3
"""
Regenerates the bio section of index.html from bio.md.

Usage:
    python3 build.py

How it works:
- Reads bio.md, treating each blank-line-separated block as one paragraph.
- Wraps each paragraph in <p>...</p>.
- Replaces everything between the <!-- BIO_START --> and <!-- BIO_END -->
  markers in index.html with the freshly generated paragraphs.
- Leaves the rest of index.html (styling, nav, photo, etc.) untouched.

Run this any time you edit bio.md, then commit both files to GitHub.
"""

import re
import sys
from pathlib import Path

BIO_FILE = Path("bio.md")
HTML_FILE = Path("index.html")
START_MARKER = "<!-- BIO_START -->"
END_MARKER = "<!-- BIO_END -->"


def main():
    if not BIO_FILE.exists():
        sys.exit(f"Error: {BIO_FILE} not found. Run this script from the site folder.")
    if not HTML_FILE.exists():
        sys.exit(f"Error: {HTML_FILE} not found. Run this script from the site folder.")

    bio_text = BIO_FILE.read_text(encoding="utf-8").strip()
    html_text = HTML_FILE.read_text(encoding="utf-8")

    if START_MARKER not in html_text or END_MARKER not in html_text:
        sys.exit(
            f"Error: could not find {START_MARKER} / {END_MARKER} markers in "
            f"{HTML_FILE}. They must both be present for the script to know "
            f"where to insert the bio."
        )

    # Split bio.md into paragraphs on blank lines
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", bio_text) if p.strip()]
    paragraphs_html = "\n\n".join(f"      <p>{p}</p>" for p in paragraphs)

    new_bio_block = f"{START_MARKER}\n{paragraphs_html}\n      {END_MARKER}"

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL
    )
    updated_html = pattern.sub(new_bio_block, html_text)

    HTML_FILE.write_text(updated_html, encoding="utf-8")
    print(f"Done. {len(paragraphs)} paragraph(s) written into {HTML_FILE}.")


if __name__ == "__main__":
    main()
