# docs-to-skills

A method and a template for turning a product's official documentation, specs and source code into
[Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that answer precisely,
**check their own output**, stay current by themselves, and come with a **blind measurement** of how much they help.

It is the process behind three public skill sets:

| Project | Sources | Checkers | Without skills → with skills (blind) |
|---|---|---|---|
| [sailpoint-isc-skills](https://github.com/normix93/sailpoint-isc-skills) | SailPoint OpenAPI specs + developer docs (MIT), product help (summarized) | workflows, transforms, API filters, rules, templates, search, sources | **44% → 100%** (50 questions) |
| [midpoint-skills](https://github.com/normix93/midpoint-skills) | midPoint XSDs + Java sources (Apache/EUPL), connector code; docs linked (CC BY-NC-ND) | XML objects vs schema per version, query language, connector properties | **74% → 99%** (40) |
| [scim-skills](https://github.com/normix93/scim-skills) | RFC 7643/7644 (facts, ABNF code components) | resources, filters, PATCH, bulk, errors | **83% → 96%** (12) |

## Why

A general model has read part of any product's documentation and fills the rest with things that sound right:
invented field names, operators in the wrong case, features placed in the wrong version. In identity and access
management, where these answers grant and remove access, a confident wrong answer is worse than none. The fix is
not more prompting; it is giving the model the exact names, the rules people get wrong, and a script that refuses
broken output.

## The method in one screen

1. **Sources and licenses first** — what is published, under which license, and what that lets you do
   ([docs/licensing.md](docs/licensing.md)).
2. **Generate** every reference that has a machine-readable source (specs, schemas, code), with a `GENERATED`
   banner, deterministic output, checker data as JSON.
3. **Hand-write** the rest from the full official page, in your own words, linked and dated.
4. **SKILL.md as a router**: which question goes to which reference; the rules the baseline got wrong.
5. **A checker per artefact** users ask for (JSON, XML, queries, code). Official examples must pass — when they
   don't, you have found a bug in your checker or in the vendor's docs (it happened in every project).
6. **Measure blind**: same model with and without skills, a third agent grades without knowing which is which.
7. **Refresh weekly** with a GitHub Action that opens a PR only on real changes.

Details, examples and lessons: [docs/method.md](docs/method.md).

## Start a new project

```bash
git clone https://github.com/normix93/docs-to-skills
python3 docs-to-skills/init.py --product "Acme IAM" --prefix acme --skill workflows \
        --dest ../acme-skills --author "Your Name" --github your-user
```

You get a repository with: a skill skeleton (`skills/acme-workflows/SKILL.md`, references, a checker), a generator
(`tools/build_references.py`) and refresh script, tests (front matter, links, banners, good/bad fixtures with
expected errors), the evaluation kit (`evals/`: question format, blind/score scripts, prompts for the three
agents), CI and weekly-refresh workflows, LICENSE/NOTICE/README/CHANGELOG templates — and its tests already pass.

## What's here

| Path | What |
|---|---|
| `docs/method.md` | the seven steps, with examples and results from the reference projects |
| `docs/licensing.md` | MIT / Apache / EUPL / GPL / CC BY(-SA) / CC BY-NC-ND / IETF / proprietary: what you may copy, generate or only link |
| `template/` | the files `init.py` copies |
| `template/evals/` | `blind.py`, `score.py`, `prompts/{baseline,skills,grader}.md`, question format |
| `init.py` | creates a new project from the template (stdlib only) |
| `tests/` | the template must produce a green repository; the eval scripts must round-trip |

## License

MIT. Projects you create are yours; the template's files are MIT so you can relicense your hand-written content.
