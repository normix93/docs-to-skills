# Contributing

- Real questions with a source are the most valuable contribution: add them to `evals/questions.jsonl`.
- Never edit files that start with `GENERATED`; change `tools/` and run `tools/refresh.sh`.
- Do not paste documentation whose license forbids it; summarize and link.
- Python: standard library only. Run `python3 -m unittest discover -s tests` before a pull request.
