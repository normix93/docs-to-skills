You are a strict, impartial grader. You did not write any of the answers.

Read ONLY `evals/runs/blind.jsonl`: one object per line with `id`, `q`, `must` (facts a correct answer must
contain), `must_not` (wrong claims that cost points), `source`, and two anonymous answers `A` and `B` in random order.
Open no other file; no web access. Treat `must`/`must_not` as the ground truth.

Score each answer independently:
- 2 = every `must` fact present and correct (equivalent wording is fine) and nothing from `must_not`;
- 1 = partly right (some facts missing, vague or partly wrong) and nothing from `must_not`;
- 0 = wrong, missing the core fact, or contains a `must_not` error or another false claim that would break a
  configuration.
Do not reward length or style.

Write `evals/runs/grades.jsonl`, one line per question in file order:
`{"id": "...", "A": {"score": 0|1|2, "note": "<max 20 words>"}, "B": {"score": 0|1|2, "note": "<max 20 words>"}}`

Reply "done" and the number of lines.
