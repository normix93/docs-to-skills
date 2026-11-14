#!/usr/bin/env python3
"""Un-blind the grades and print a Markdown results table.

  python3 evals/score.py evals/runs/grades.jsonl evals/runs/blind_map.json [evals/questions.jsonl] > evals/results.md

grades.jsonl: {"id": "...", "A": {"score": 0|1|2, "note": "..."}, "B": {...}}
blind_map.json: {"<id>": {"A": "baseline"|"skills", "B": "..."}}
"""
from __future__ import annotations

import collections
import json
import sys


def main(grades_path: str, map_path: str, questions_path: str = "evals/questions.jsonl") -> None:
    with open(map_path, encoding="utf-8") as fh:
        blind = json.load(fh)
    group = {}
    try:
        with open(questions_path, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    q = json.loads(line)
                    group[q["id"]] = q.get("skill") or q.get("area") or q["id"].split("-")[0]
    except OSError:
        pass
    per = collections.defaultdict(lambda: {"baseline": 0, "skills": 0, "n": 0})
    tot = {"baseline": 0, "skills": 0}
    rows = []
    with open(grades_path, encoding="utf-8") as fh:
        grades = [json.loads(l) for l in fh if l.strip()]
    for g in grades:
        m = blind[g["id"]]
        s = {m["A"]: g["A"], m["B"]: g["B"]}
        k = group.get(g["id"], g["id"].split("-")[0])
        per[k]["n"] += 1
        for side in ("baseline", "skills"):
            per[k][side] += s[side]["score"]
            tot[side] += s[side]["score"]
        rows.append((g["id"], s["baseline"], s["skills"]))
    n = len(grades)
    print("# Results\n")
    print(f"{n} questions, 0–2 points each (max {2 * n}). Blind grading by a separate agent.\n")
    print("| Group | Questions | Without skills | With skills |\n|---|---|---|---|")
    for k in sorted(per):
        p = per[k]
        print(f"| {k} | {p['n']} | {p['baseline']}/{2 * p['n']} | {p['skills']}/{2 * p['n']} |")
    pct = lambda v: round(100 * v / (2 * n)) if n else 0
    print(f"| **Total** | {n} | **{tot['baseline']}/{2 * n} ({pct(tot['baseline'])}%)** | "
          f"**{tot['skills']}/{2 * n} ({pct(tot['skills'])}%)** |\n")
    print("## Per question\n\n| Question | Without | With | Grader note (without) | Grader note (with) |\n|---|---|---|---|---|")
    for qid, b, s in rows:
        print(f"| {qid} | {b['score']} | {s['score']} | {b.get('note', '').replace('|', '/')} | "
              f"{s.get('note', '').replace('|', '/')} |")


if __name__ == "__main__":
    main(*sys.argv[1:])
