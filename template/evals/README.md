# Evaluation

1. Write questions in `questions.jsonl` (`id`, `skill`, `q`, `must`, `must_not`, `source`). Prefer real questions;
   verify every `must` against the source before running anything.
2. `python3 -c "import json;[print(json.dumps({'id':q['id'],'q':q['q']})) for q in map(json.loads,open('evals/questions.jsonl'))]" > evals/runs/questions-only.jsonl`
3. Run two agents with the same model, no web: `prompts/baseline.md` (closed book) and `prompts/skills.md` (skills
   only). Keep the second one's list of gaps.
4. `python3 evals/blind.py evals/questions.jsonl evals/runs/answers-baseline.jsonl evals/runs/answers-skills.jsonl --out evals/runs`
5. Run a third agent with `prompts/grader.md` on `runs/blind.jsonl` only.
6. `python3 evals/score.py evals/runs/grades.jsonl evals/runs/blind_map.json evals/questions.jsonl > evals/results.md`
7. Fix the skills from the gaps list; publish the first run's numbers honestly, then re-run.
