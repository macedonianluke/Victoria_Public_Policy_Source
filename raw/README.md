# Raw Evidence Library

**The source layer behind every claim in this repository.**

`raw/` holds primary and secondary source material: PDFs, reports, datasets, submissions, media clippings, working notes and source documents. It is organised to mirror the 16 portfolio areas, plus a cross-cutting folder and an unsorted folder. Every file has a sidecar `.meta.md` record and a line in [`MANIFEST.csv`](MANIFEST.csv).

The rule is simple: **if a claim matters, the source lives here.** If it does not, the claim is a hypothesis, not evidence.

---

## Structure

```
raw/
├── README.md
├── MANIFEST.csv
├── _template/SOURCE.md
├── 00-cross-cutting/
├── 01-fiscal-and-public-sector/
├── 02-housing-and-planning/
├── 03-health-and-hospitals/
├── 04-mental-health-and-wellbeing/
├── 05-education-and-early-childhood/
├── 06-skills-jobs-and-industry/
├── 07-transport-and-roads/
├── 08-energy-and-climate/
├── 09-environment-water-and-circular-economy/
├── 10-justice-police-and-community-safety/
├── 11-families-children-and-community/
├── 12-regional-victoria-and-agriculture/
├── 13-emergency-management-and-resilience/
├── 14-first-peoples-and-multicultural-affairs/
├── 15-local-government-and-civic-infrastructure/
├── 16-arts-sport-and-tourism/
└── _unsorted/
```

A source is filed by **primary policy relevance**, not by publisher. A VAGO report on road maintenance goes in `07-transport-and-roads/`; a VAGO report on public sector consultants goes in `01-fiscal-and-public-sector/`. A source that spans several areas goes in the area it most directly informs, with cross-links in the sidecar.

---

## File naming

```
YYYY-MM-DD__publisher__short-title.ext
```

Examples:

```
2026-11-12__dtf__pre-election-budget-update.pdf
2026-09-09__vago__maintaining-state-roads.pdf
2026-10-22__abc-news__victorian-school-funding-deal.html
```

- Use the **publication date**, not the download date.
- Use `YYYY-MM` if the day is unknown.
- Use `undated` if the date is unknown.
- Use `unknown` if the publisher is unknown.
- Keep the original filename in the sidecar and the manifest.

---

## Every file gets a sidecar

Create a `.meta.md` file next to the source with the template in [`_template/SOURCE.md`](_template/SOURCE.md). At minimum:

- Original filename
- Title
- Publisher / author
- Publication date
- URL or access path
- Portfolio
- Document type
- Confidence label (A/B/C/D)
- What it supports
- Verification notes

The sidecar is not bureaucracy. It is what makes the source usable six months later.

---

## The manifest

[`MANIFEST.csv`](MANIFEST.csv) is the single index. Columns:

```
filed_date, original_filename, filed_path, portfolio, document_type, publisher, date, confidence, notes
```

Every new source gets a line. If a source is replaced or superseded, do not delete the old line; add a new line and mark the old one `superseded`.

---

## What belongs here

- Government reports, budget papers, annual reports, audit reports, legislation, strategies.
- Parliamentary inquiries, submissions and Hansard extracts.
- Academic and independent research.
- Data extracts, tables and methodology notes.
- Stakeholder submissions and community evidence.
- Media articles used as evidence of a claim or a position.
- Working notes that explain how a number was derived.

## What does not belong here

- Personal or sensitive information that is not necessary for policy analysis.
- Large binary files that can be linked instead of stored.
- Drafts of portfolio READMEs or proposals — those live in `01-portfolio/` and `03-proposals/`.
- Unverified AI-generated summaries presented as sources. Label them `[D]` or `[C]` and link to the primary source.

---

## How files arrive

1. A human drops loose files into [`../incoming/drop/`](../incoming/drop/).
2. The triage script (`python incoming/triage.py --apply`) classifies them, renames them, files them here, writes a sidecar and updates the manifest.
3. An AI or human reviews the `_unsorted/` folder and the sidecars, corrects misclassifications, and promotes anything that is really a method or a proposal to `00-method/` or `03-proposals/`.
4. The relevant portfolio README gets a link and, if material, a verified fact.

See [`../incoming/README.md`](../incoming/README.md) for the drop-zone rules.

---

## Confidence labels

| Label | Meaning |
|---|---|
| **[A]** | Primary, current, independently auditable |
| **[B]** | Official, but dated, partial or not independently audited |
| **[C]** | Stakeholder, industry or media claim |
| **[D]** | Assumption, estimate or projection |

See [`../00-method/evidence-standard.md`](../00-method/evidence-standard.md) for the full standard.

---

## Housekeeping

- Do not commit confidential, personal or commercially sensitive material. Use a link and a note instead.
- Do not commit files over 50 MB. Link to the source.
- Do not delete a source because it is inconvenient. Mark it `superseded` or `disputed` and explain why.
- Review `_unsorted/` weekly during active policy development.
