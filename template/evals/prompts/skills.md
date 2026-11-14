You are answering an evaluation about __PRODUCT__ using ONLY a set of Agent Skills.

Rules (strict):
- Questions: `evals/runs/questions-only.jsonl`.
- Knowledge source: `skills/` only. For each question open the relevant `SKILL.md`, follow its instructions and
  the references/scripts it points to; you may run the scripts.
- Do NOT read `evals/questions.jsonl`, `tests/`, `tools/`, source checkouts or caches. No web search or fetch.
- Answer concisely (3-8 sentences or a short snippet); run the skill's checker on anything you write.
- Write `evals/runs/answers-skills.jsonl`: one JSON object per line, `{"id": "...", "answer": "..."}`, same order.

Reply "done", the number of answers, and up to 10 bullets on places where the skills were missing information,
unclear or wrong. That list is the most useful output of the run: fix the skills from it.
