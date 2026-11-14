#!/usr/bin/env python3
"""Build the blinded file for the grader from two answer sets.

  python3 evals/blind.py evals/questions.jsonl evals/runs/answers-baseline.jsonl evals/runs/answers-skills.jsonl \
          --out evals/runs [--seed 42] [--prefix <id prefix to include>]

Writes runs/blind.jsonl (question, must, must_not, source, answers "A"/"B" in random order) and
runs/blind_map.json (which of A/B is which). Give the grader ONLY blind.jsonl.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("questions")
    ap.add_argument("baseline")
    ap.add_argument("skills")
    ap.add_argument("--out", default="evals/runs")
    ap.add_argument("--seed", type=int, default=20261114)
    ap.add_argument("--prefix", default="")
    a = ap.parse_args()
    qs = [q for q in load(a.questions) if q["id"].startswith(a.prefix)]
    base = {x["id"]: x["answer"] for x in load(a.baseline)}
    skl = {x["id"]: x["answer"] for x in load(a.skills)}
    missing = [q["id"] for q in qs if q["id"] not in base or q["id"] not in skl]
    if missing:
        raise SystemExit(f"answers missing for: {', '.join(missing)}")
    rnd = random.Random(a.seed)
    blind, mapping = [], {}
    for q in qs:
        pair = [("baseline", base[q["id"]]), ("skills", skl[q["id"]])]
        rnd.shuffle(pair)
        mapping[q["id"]] = {"A": pair[0][0], "B": pair[1][0]}
        blind.append({"id": q["id"], "q": q["q"], "must": q["must"], "must_not": q["must_not"],
                      "source": q.get("source", ""), "A": pair[0][1], "B": pair[1][1]})
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "blind.jsonl").write_text("".join(json.dumps(b, ensure_ascii=False) + "\n" for b in blind), encoding="utf-8")
    (out / "blind_map.json").write_text(json.dumps(mapping, indent=1), encoding="utf-8")
    print(f"{len(blind)} questions blinded -> {out}/blind.jsonl (map in blind_map.json: do not show it to the grader)")


if __name__ == "__main__":
    main()
