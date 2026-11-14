# Licensing of sources: what you may put in a public skill repository

Practical guidance from building public skill sets; not legal advice. When in doubt, link instead of copying, and
read the source's own LICENSE file — a repository's license and its documentation's license often differ.

## The three questions

1. **Can I copy the text?** Only if the license allows redistribution (MIT, Apache, BSD, CC BY, CC BY-SA, EUPL,
   GPL...). "Publicly visible" is not a license.
2. **Can I modify it?** "ND" (no derivatives) licenses forbid adapted versions: no excerpts rewritten into your
   references, no translated tables. Link and summarize in your own words instead.
3. **What license do the derived files get?** Permissive licenses: yours (keep notices). Copyleft (EUPL, GPL,
   CC BY-SA): the derived file keeps that license — keep such files separate and labelled.

Facts — names of fields and endpoints, types, enum values, defaults, version numbers — are generally not protected
by copyright, so extracting them into your own tables is the safe path for restrictive sources. Rewriting a page
sentence by sentence is not "your own words"; a summary organized around the reader's questions is.

## Common source licenses

| License | Copy text? | Modify? | Derived files | In practice |
|---|---|---|---|---|
| MIT, BSD-2/3 | yes | yes | any license, keep the notice | generate freely; credit in NOTICE |
| Apache-2.0 | yes | yes (state changes) | any license, keep NOTICE | generate freely; keep their NOTICE text |
| EUPL-1.2 | yes | yes | EUPL-1.2 (or a listed compatible copyleft license) | keep generated files under EUPL, say so in each banner |
| GPL / LGPL | yes | yes | same license | as EUPL |
| CC BY 4.0 | yes | yes | any, with attribution | cite title, author, link, license |
| CC BY-SA 4.0 | yes | yes | CC BY-SA | keep derived text under CC BY-SA, separate files |
| CC BY-NC(-ND) | NC: not for commercial use; ND: no adaptations | ND: no | — | link only; titles + URLs; facts |
| IETF RFCs | text: only unmodified excerpts | no (except code components) | code components (ABNF, schemas, code marked as such): Simplified BSD | quote ABNF with the IETF notice; summarize prose; extract facts |
| Proprietary docs (most product help sites) | no | no | — | facts, links, your own summaries with the date you checked |

## Patterns used in the reference projects

- **sailpoint-isc-skills**: SailPoint's API specs and developer-docs repositories are MIT → generated references
  carry the text; product help pages are summarized and dated.
- **midpoint-skills**: docs are CC BY-NC-ND → not copied; references generated from XSDs and Java (support-4.8:
  Apache/EUPL dual, redistributed as Apache; support-4.10: EUPL-only, redistributed as EUPL); connectors Apache;
  docs map = titles and URLs only; a test fails if a sentence of the docs appears in a hand-written file.
- **scim-skills**: RFC text is not redistributed (downloaded at build/test time into a git-ignored cache); schema
  data = facts; the filter ABNF is a code component quoted under the IETF's BSD terms.

## Checklist

- [ ] LICENSE of every source read and recorded in NOTICE with the files derived from it.
- [ ] Every generated file states its source and license in its banner.
- [ ] No text from link-only sources in hand-written files (consider a test like midpoint-skills' "no copied
      docs" check).
- [ ] Vendor trademarks used only to name the product; "unofficial, not affiliated" in README.
- [ ] No customer, tenant or employer data anywhere — fixtures are invented.
