#!/usr/bin/env python3
"""Start a new skill repository for a product, using the docs-to-skills method.

  python3 init.py --product "Acme IAM" --prefix acme --dest ../acme-skills \
                  [--repo acme-skills] [--author "Your Name"] [--github your-user] [--skill topic]

Copies template/ to --dest, replaces the placeholders (__PRODUCT__, __PREFIX__, __REPO__, __AUTHOR__,
__GITHUB__, __YEAR__, __DATE__), names the first skill <prefix>-<skill>, and runs the new repo's tests.
Standard library only. Refuses to write into a non-empty directory.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "template"
TEXT_SUFFIXES = {".md", ".py", ".json", ".jsonl", ".yml", ".yaml", ".sh", ".txt", ""}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--product", required=True, help='product name as people write it, e.g. "Acme IAM"')
    ap.add_argument("--prefix", required=True, help="short lowercase prefix for skill names, e.g. acme")
    ap.add_argument("--dest", required=True, type=Path)
    ap.add_argument("--repo", help="repository name (default: <prefix>-skills)")
    ap.add_argument("--author", default="your-name")
    ap.add_argument("--github", default="your-github-user")
    ap.add_argument("--skill", default="example", help="topic of the first skill (default: example)")
    ap.add_argument("--no-test", action="store_true", help="do not run the new repository's tests")
    a = ap.parse_args(argv)

    if not re.fullmatch(r"[a-z][a-z0-9-]{1,30}", a.prefix):
        print("--prefix must be lowercase letters, digits and dashes (e.g. acme)")
        return 2
    if not re.fullmatch(r"[a-z][a-z0-9-]{1,40}", a.skill):
        print("--skill must be lowercase letters, digits and dashes")
        return 2
    dest = a.dest.resolve()
    if dest.exists() and any(p.name != ".git" for p in dest.iterdir()):
        print(f"{dest} is not empty; choose a new directory")
        return 2
    repo = a.repo or f"{a.prefix}-skills"
    values = {
        "__PRODUCT__": a.product, "__PREFIX__": a.prefix, "__REPO__": repo, "__AUTHOR__": a.author,
        "__GITHUB__": a.github, "__YEAR__": str(dt.date.today().year), "__DATE__": dt.date.today().isoformat(),
    }

    shutil.copytree(TEMPLATE, dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "runs"))
    (dest / "evals" / "runs").mkdir(parents=True, exist_ok=True)
    old_skill = dest / "skills" / "__PREFIX__-example"
    new_name = f"{a.prefix}-{a.skill}"
    old_skill.rename(dest / "skills" / new_name)
    values_skill = {"__PREFIX__-example": new_name}

    for path in dest.rglob("*"):
        if path.is_file() and (path.suffix in TEXT_SUFFIXES):
            text = path.read_text(encoding="utf-8")
            new = text
            for k, v in {**values_skill, **values}.items():
                new = new.replace(k, v)
            if new != text:
                path.write_text(new, encoding="utf-8")
    for script in (dest / "tools" / "refresh.sh",):
        script.chmod(0o755)

    left = [str(p.relative_to(dest)) for p in dest.rglob("*")
            if p.is_file() and "__" in p.read_text(encoding="utf-8", errors="ignore").replace("__name__", "")
            .replace("__main__", "").replace("__future__", "").replace("__pycache__", "").replace("__init__", "")
            and re.search(r"__[A-Z]+__", p.read_text(encoding="utf-8", errors="ignore"))]
    if left:
        print("placeholders left in:", ", ".join(left))
        return 1

    print(f"Created {dest} (repo {repo}, first skill {new_name})")
    if not a.no_test:
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=dest,
                           capture_output=True, text=True)
        print(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else r.stdout)
        if r.returncode:
            print(r.stderr)
            return 1
    print("Next: docs/method.md, step 1 (sources and licenses).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
