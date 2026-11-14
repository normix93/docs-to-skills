---
name: __PREFIX__-example
description: __PRODUCT__ <topic> reference — <the 4-8 things people ask about this topic, in their words>. Use when someone asks <typical question 1>, <typical question 2>, or writes/reviews <the artefact this topic produces>.
---

# __PRODUCT__ <topic>

<!-- One paragraph: what this topic is, and the one distinction people most often get wrong. -->

## How to answer

1. <Kind of question> → `references/<generated-file>.md` (GENERATED from <source>: exact names, never guess).
2. <Kind of question> → `references/<hand-written-file>.md`.
3. Version-specific behaviour: say which version the answer applies to.
4. Anything you write for the user (JSON, XML, query, code): run `scripts/check_example.py` first and fix every
   ERROR.
5. Point to the official page for the full rule (link from the reference file); never paste documentation whose
   license does not allow it (see the repo's NOTICE).

## Rules that prevent most mistakes

1. <The rule your eval baseline got wrong most often.>
2. <...>

## Checker

```bash
python3 scripts/check_example.py file.json
```

<What it catches, in one paragraph. What it cannot know (tenant data, custom schema).>

## References

| File | Use for |
|---|---|
| `references/README.md` | what is generated and what is hand-written, and from which sources |
