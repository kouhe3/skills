#!/usr/bin/env python3
"""Validate ./skills against the Agent Skills specification."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
TOP_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):", re.M)
REF_RE = re.compile(r"(?:references|scripts|assets)/[A-Za-z0-9_.\-/]+")


def main() -> int:
    errors: list[str] = []
    checked = 0

    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        checked += 1
        path = skill_dir / "SKILL.md"
        if not path.is_file():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue

        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            errors.append(f"{skill_dir.name}: missing YAML frontmatter")
            continue

        frontmatter = match.group(1)
        body = text[match.end():]
        keys = set(TOP_KEY_RE.findall(frontmatter))
        extra = keys - ALLOWED
        if extra:
            errors.append(f"{skill_dir.name}: unsupported frontmatter keys: {sorted(extra)}")

        name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.M)
        desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
        if not name_match:
            errors.append(f"{skill_dir.name}: missing name")
            continue
        if not desc_match:
            errors.append(f"{skill_dir.name}: missing description")
            continue

        name = name_match.group(1).strip()
        description = desc_match.group(1).strip()

        if len(name) > 64:
            errors.append(f"{skill_dir.name}: name longer than 64 characters")
        if not NAME_RE.match(name):
            errors.append(f"{skill_dir.name}: name is not lowercase kebab-case")
        if name != skill_dir.name:
            errors.append(f"{skill_dir.name}: name must match directory ({name})")
        if not 1 <= len(description) <= 1024:
            errors.append(f"{skill_dir.name}: description length {len(description)} not in 1..1024")

        body_lines = len(body.splitlines())
        if body_lines >= 500:
            errors.append(f"{skill_dir.name}: SKILL.md body is {body_lines} lines (spec recommends <500)")

        for ref in sorted(set(REF_RE.findall(text))):
            if not (skill_dir / ref).exists():
                errors.append(f"{skill_dir.name}: referenced file missing: {ref}")

    if errors:
        print("FAIL")
        for error in errors:
            print(" -", error)
        return 1

    print(f"OK: {checked} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())