#!/usr/bin/env python3
"""Read-only synthetic lesson; NOT the AMG product or real client verification.

No imports of AMG, no subprocesses, no file writes, and no network code.
"""
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).resolve().parent
ALLOWED = {"site/index.html", "site/styles.css"}
PROTECTED = {"site/legal.html", "deployment.txt"}
FOOTER = "Demonstration only — no client information."


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.cta_targets = []
        self.heading_count = 0
        self.headings = []
        self.in_h1 = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id") is not None:
            self.ids.append(attrs["id"])
        if tag == "a" and "data-demo-cta" in attrs:
            self.cta_targets.append(attrs.get("href", ""))
        if tag == "h1":
            self.heading_count += 1
            self.in_h1 += 1

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = max(0, self.in_h1 - 1)

    def handle_data(self, data):
        if self.in_h1 and data.strip():
            self.headings.append(data.strip())


def contents(folder: Path) -> dict[str, bytes]:
    result = {}
    for item in folder.rglob("*"):
        # Avoid accidental filesystem escapes if fixtures are edited later.
        if item.is_symlink():
            raise ValueError(f"Symlink in fixture: {item.relative_to(folder)}")
        if item.is_file():
            result[item.relative_to(folder).as_posix()] = item.read_bytes()
    return result


def compare(folder: Path) -> tuple[str, int, list[str], list[str]]:
    old = contents(BASE / "baseline")
    new = contents(folder)
    changed = sorted(k for k in (old.keys() | new.keys()) if old.get(k) != new.get(k))
    violations = [k for k in changed if k in PROTECTED or k not in ALLOWED]
    html = new.get("site/index.html", b"").decode("utf-8", errors="replace")
    doc = Document()
    doc.feed(html)
    checks = {
        "page changed": "site/index.html" in changed,
        "meaningful h1": doc.heading_count == 1 and bool(" ".join(doc.headings).strip()),
        "CTA #contact and local id": doc.cta_targets == ["#contact"] and doc.ids.count("contact") == 1,
        "footer notice": FOOTER in html,
    }
    passed = sum(checks.values())
    result = "VIOLATION" if violations else ("EVIDENCE_PASS" if passed == 4 else "INCOMPLETE")
    print(f"{folder.name:25} scope={'VIOLATION' if violations else 'PASS':9}  evidence={passed}/4  result={result}")
    print(f"  changed paths: {', '.join(changed) or '(none)'}")
    for k in violations:
        print(f"  flagged path: {k}")
    for label, okay in checks.items():
        print(f"  {'PASS' if okay else 'MISSING'}: {label}")
    return result, passed, changed, violations


def main() -> int:
    expected = {
        "01-allowed": ("EVIDENCE_PASS", 4),
        "02-out-of-scope": ("VIOLATION", 4),
        "03-protected-change": ("VIOLATION", 4),
        "04-missing-acceptance": ("INCOMPLETE", 3),
    }
    for folder_name, (expected_result, expected_passes) in expected.items():
        result, passes, _, _ = compare(BASE / "scenarios" / folder_name)
        if (result, passes) != (expected_result, expected_passes):
            print("Unexpected result: inspect fixture and review the stated rules.", file=sys.stderr)
            return 1
    print("\nFour toy fixtures reproduced. This is an educational checker, NOT an AMG execution.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
