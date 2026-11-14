# The method

Seven steps. Each one exists because skipping it produced a wrong answer in one of the reference projects
([sailpoint-isc-skills](https://github.com/normix93/sailpoint-isc-skills),
[midpoint-skills](https://github.com/normix93/midpoint-skills), [scim-skills](https://github.com/normix93/scim-skills)).

## 1. Find the sources of truth and their licenses

List what the product publishes and under which license, before writing anything: OpenAPI specs, XSD or JSON
schemas, SDK or server source, docs repositories, RFCs, sample repositories, product help pages.

The license decides what you may do with each source (`licensing.md`):

| You may | Typical sources | Use it for |
|---|---|---|
| copy and adapt (MIT, Apache-2.0, BSD) | OpenAPI specs, developer docs repos, connectors | generated references that keep the text |
| copy, but derived files keep the license (EUPL, GPL, CC BY-SA) | some product source trees | generated files under that license, kept separate |
| link only (CC BY-NC-ND, proprietary help, IETF prose) | product docs sites, RFC text | facts, titles + URLs, summaries in your own words |

*Example:* midPoint's documentation is CC BY-NC-ND, so midpoint-skills generates its references from the XSDs and
Java sources (EUPL/Apache) and links the docs; midPoint 4.10's code is EUPL-only while 4.8 was dual-licensed, so
generated files carry the license of the branch they come from.

## 2. Generate everything that has a machine-readable source

Write `tools/build_references.py` to turn specs and code into references: one file per API service, schema file or
topic; every operation, field, enum, default, since/deprecated flag. Rules:

- a `GENERATED` banner with source, commit, date and license on every file;
- deterministic output (a rebuild without upstream changes changes nothing but dates);
- checker data (enums, allowed fields, forbidden calls) as JSON next to the checker, never hard-coded.

What generation buys: exact names. Models invent field names, operators and endpoints that sound right; a generated
table removes the guess. *Example:* SailPoint's 1,100 operations, each with the exact filter fields and operators.

## 3. Write the rest by hand, verified and dated

For behaviour that lives only in product help pages (when a trigger fires, how correlation decides, what a
threshold does), read the full page, write the rule in your own words with the numbers, link it and write the date
you checked it. Never write from memory: in the reference projects, claims that "everybody knows" turned out
wrong when checked (midPoint's `basicAuthentication` was assumed to be 4.10-only and is in 4.8 too; a SAML
attribute was placed on the wrong element; an OIDC redirect URI pattern turned out to be undocumented).

## 4. Write the SKILL.md as a router

The SKILL.md is short: what the topic is, *how to answer* (which question → which reference), the 5–10 rules that
prevent the most common mistakes (take them from the baseline errors of step 6), the checker, the references
table. The description field decides when the skill triggers: write it with the words users use.

## 5. Build a checker for every artefact users ask a model to write

JSON workflow, transform, XML object, query, filter, PATCH body, rule code. A stdlib Python script that returns
ERROR (would be rejected or misbehave) and WARNING (legal but risky), with messages that say what to write
instead. Then test it two ways:

- **official examples must pass** — and when one does not, either your checker or the vendor's documentation is
  wrong. Both happened in every project: a five-condition limit that was the basic editor's only; a SailPoint guide
  using `start` where the API requires `begin`; RFC 7644 examples with invalid filters; an Evolveum sample with
  connector properties removed years ago. Record vendor mistakes as known issues so the test keeps detecting them;
- **broken fixtures must fail** with exactly the expected messages (`tests/fixtures/bad/*.expected`).

## 6. Measure blind

Write 10–50 questions with `must`/`must_not` facts and a source each, run the same model closed-book and with the
skills, have a third agent grade both blind, un-blind with `score.py` (`template/evals/`). The answering agent's
list of gaps is the most valuable output: fix the skills from it.

Publish the first run's numbers, including what the method does not prove (you wrote the questions from the same
sources). Results so far:

| Project | Without skills | With skills |
|---|---|---|
| SailPoint ISC (50 questions) | 44% | 100% |
| midPoint 4.8/4.10 (40) | 74% | 99% |
| SCIM 2.0 (12) | 83% | 96% |

The less public the product, the bigger the gap; for public standards the checker matters more than the text.

## 7. Keep it current without effort

`tools/refresh.sh` re-fetches sources (shallow, sparse clones) and rebuilds; a weekly GitHub Action runs it, drops
files whose only change is the banner date, runs the tests and opens a pull request only when something really
changed. No credentials, no tenant access.

## Publishing checklist

- README: what it answers (example questions), checkers, measured results, findings, install, license.
- NOTICE: which files come from which source under which license.
- Tests green in CI; plugin manifests valid.
- Unofficial / not affiliated statement.
