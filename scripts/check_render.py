#!/usr/bin/env python3
"""Check a rendered template's local links and published file boundary."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import zipfile

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.refs, self.ids = [], set()
        self.feed(path.read_text(encoding="utf-8"))
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for field in ("href", "src"):
            if attrs.get(field):
                self.refs.append(attrs[field])

def check(project):
    output = project / ("_book" if (project / "_book").exists() else "_site")
    if not (output / "index.html").is_file():
        raise ValueError("Rendered index.html is missing")
    pages = {path.resolve(): Page(path) for path in output.rglob("*.html")}
    errors = []
    for path, page in pages.items():
        for ref in page.refs:
            uri = urlsplit(ref)
            if uri.scheme or uri.netloc or ref.startswith("/"):
                continue
            target = (path.parent / unquote(uri.path)).resolve() if uri.path else path
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{path.relative_to(output.resolve())}: missing {ref}")
            elif uri.fragment and target in pages and unquote(uri.fragment) not in pages[target].ids:
                errors.append(f"{path.relative_to(output.resolve())}: missing anchor {ref}")
    if (project / "instructor").exists():
        if (output / "instructor").exists():
            errors.append("Instructor directory was published")
        for path in output.rglob("*"):
            if path.is_file() and path.suffix in {".html", ".json"}:
                if "Instructor answer key" in path.read_text(encoding="utf-8"):
                    errors.append("Instructor answer key appears in rendered content")
    if output.name == "_book":
        books = list(output.glob("*.epub"))
        if len(books) != 1:
            errors.append("Expected one EPUB alongside the HTML book")
        else:
            with zipfile.ZipFile(books[0]) as book:
                if book.testzip() or book.read("mimetype") != b"application/epub+zip":
                    errors.append("Invalid EPUB container")
    if errors:
        raise ValueError("\n".join(errors))
    print(f"Checked {len(pages)} HTML pages, local links, anchors and publication boundaries")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    try:
        check(args.project.resolve())
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, str(error) + "\n")
