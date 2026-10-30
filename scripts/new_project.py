#!/usr/bin/env python3
"""Create a standalone publishing project without replacing existing files."""
import argparse
import json
from pathlib import Path
import shutil
import shlex


def create(destination, title, author, language="en"):
    root = Path(__file__).resolve().parents[1]
    template = root / "template"
    if not title.strip() or not author.strip():
        raise ValueError("Title and author must be nonblank")
    if language not in {"en", "de", "fr"}:
        raise ValueError("Language must be en, de or fr")
    destination = Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination already exists: {destination}")
    if template.resolve() in destination.resolve().parents:
        raise ValueError("Destination cannot be inside the template")
    config = json.loads((template / "_quarto.yml").read_text())
    kind = config["project"]["type"]
    config[kind]["title"] = title.strip()
    config["author"] = author.strip()
    config["lang"] = language
    config_text = json.dumps(config, ensure_ascii=False, indent=2) + "\n"
    shutil.copytree(template, destination, symlinks=False)
    (destination / "_quarto.yml").write_text(config_text, encoding="utf-8")
    (destination / "LICENSE").write_bytes((root / "LICENSE").read_bytes())
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--language", choices=["en", "de", "fr"], default="en")
    args = parser.parse_args()
    try:
        target = create(args.destination, args.title, args.author, args.language)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Cannot create project: {exc}\n")
    print(f"Created {target}\nNext: cd {shlex.quote(str(target))} && quarto render --to html")


if __name__ == "__main__":
    main()
