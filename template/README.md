# __PRODUCT__ Skills (unofficial)

Agent Skills that turn Claude into a __PRODUCT__ reference, built from the official open sources and checked by
scripts that run before an answer is handed over.

## Skills

| Skill | Ask it about |
|---|---|
| `__PREFIX__-example` | <topic> |

## Checkers

| Script | What it catches |
|---|---|
| `skills/__PREFIX__-example/scripts/check_example.py` | <...> |

## Measured

<Results of evals/: N questions, X% without the skills, Y% with them, graded blind. Link evals/results.md.>

## Install

```
/plugin marketplace add __GITHUB__/__REPO__
/plugin install __REPO__@__REPO__
```

## Keeping it current

`tools/refresh.sh` rebuilds every GENERATED file; `.github/workflows/refresh-references.yml` runs it weekly and
opens a pull request only when something changed.

## License

MIT for hand-written content; generated files keep their source's license (`NOTICE`). Not affiliated with the
vendor.

Built with [docs-to-skills](https://github.com/normix93/docs-to-skills).
