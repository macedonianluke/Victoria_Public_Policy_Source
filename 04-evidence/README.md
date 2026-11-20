# Evidence

**The verification layer between the raw source and the public claim.**

`04-evidence/` holds the source register, data notes, contradiction log and verification record. It is deliberately separate from `raw/` (the source files) and `01-portfolio/` (the policy argument). The evidence layer answers: **how do we know, and how confident are we?**

---

## What lives here

| File | Purpose |
|---|---|
| [`source-register.md`](source-register.md) | The master list of sources used across the portfolio READMEs and proposals. |
| [`README.md`](README.md) | This guide: source hierarchy, verification workflow, contradiction log and data notes. |

Future files, as needed:

- `data-notes/` — definitions, methods and caveats for each dataset.
- `verification-log.md` — what was checked, when, by whom, and what changed.
- `contradictions.md` — where sources disagree and why.
- `restricted/` — pointers to material that cannot be stored here.

---

## Source hierarchy

Use the highest available source. Move down only when the higher source does not exist.

| Tier | Source type | Examples |
|---|---|---|
| **1** | Primary official | Legislation, budget papers, annual reports, VAGO, ABS, court judgments, treaties, intergovernmental agreements |
| **2** | Official evaluation / regulator | Program evaluations, productivity commissions, auditor reports, regulator determinations, parliamentary inquiries |
| **3** | Peer-reviewed / expert | Academic research, independent think tanks with transparent methods, professional bodies |
| **4** | Reputable media / industry | Major newspapers, industry associations, unions, advocacy groups |
| **5** | Anecdote / claim / assumption | Individual case, stakeholder assertion, social media, AI-generated summary |

A Tier 4 or 5 source can tell you what someone believes. It cannot tell you what is true.

---

## Confidence labels

| Label | Meaning | Test |
|---|---|---|
| **[A]** | Primary, current, independently auditable | Can a sceptical reader click through to the number and see the same thing? |
| **[B]** | Official, but dated, partial or not independently audited | Is the vintage clear, and is the limitation stated? |
| **[C]** | Stakeholder, industry or media claim | Is it corroborated by a Tier 1–3 source, or clearly presented as a claim? |
| **[D]** | Assumption, estimate or projection | Is the method stated, and is there a sensitivity range? |

If a number has no label, treat it as **[D]**.

---

## The verification workflow

1. **Locate the primary source.** Not the summary, not the media report, not the AI answer.
2. **Record the metadata.** Title, publisher, date, URL, page/table, access date.
3. **Check the definition.** FTE vs headcount; gross vs net; capital vs operating; nominal vs real; Victoria vs national.
4. **Check the vintage.** The period the number describes, not the date it was published.
5. **Label the confidence.** A/B/C/D.
6. **Write what it supports.** Which portfolio claim or proposal line.
7. **Add to the register.**
8. **If it contradicts another source, log it.**
9. **If it changes a portfolio README, update the README and the register together.**
10. **If it cannot be verified, label it [D] and say what would change your mind.**

---

## Contradiction log

When sources disagree, do not average them. Record the disagreement:

| Claim | Source A | Source B | Why they differ | What we will use | Confidence |
|---|---|---|---|---|---|
| Example: net debt | DTF Pre-Election Budget Update | Media report | Different date/definition | DTF figure | [A] |

Common reasons: different definitions, vintages, geographies, gross vs net, optimistic vs conservative assumptions, stakeholder advocacy. The contradiction is often the most useful part of the evidence.

### Current contradictions to resolve

| Claim | Source A | Source B | Why they differ | What we will use | Confidence |
|---|---|---|---|---|---|
| 2026–27 net debt | DTF Pre-Election Budget Update: **$173.1b at 30 June 2027** | Raw overhead review: **$175.6b in 2026–27** | Different vintage/update and possibly different coverage | DTF figure until the review's source is traced | [A] vs [C] |
| Non-frontline savings | Raw overhead review: **$6.2b–$8.6b/year** | Government reform package: **more than $4b over four years** | Different scope, timing, gross vs net, and what counts as a saving | Government figure for enacted commitments; raw range as a hypothesis to test | [D] vs [B] |
| Planning reform dividend | Raw planning blueprint: **$4.5b–$7.0b/year** | No independent estimate located | Modelled, assumes full implementation and behavioural change | Treat as a hypothesis; build a sensitivity model before publication | [D] |
| Pothole fleet savings | Raw pothole proposals: **$28.75m/year from Year 2** | Existing VAGO/DTP figures are not yet reconciled | Different fleet, operating and offset assumptions | Treat as a modelled scenario; verify unit costs and offsets | [D] |
| Health back-office savings | Raw overhead review: **$1.2b–$1.6b/year** from 76 health services | No independent costing located | Assumes full corporate consolidation and no clinical impact | Commission an independent costing before use | [D] |

These rows are not a reason to stop. They are the work. A proposal that cannot survive the contradiction is not ready.

---

## Data notes

For each dataset used in a portfolio README or proposal, record:

- **Dataset name and publisher**
- **Unit and definitions**
- **Coverage and geography**
- **Vintage and update frequency**
- **Known limitations** (who is missing, who is misclassified, who is not counted)
- **Access and licence**
- **What it can and cannot support**

---

## What not to do

- Do not invent a source, a URL or a date.
- Do not cite a secondary summary when the primary source is available.
- Do not add numbers with different definitions.
- Do not present an assumption as an estimate.
- Do not present a judgment as a fact.
- Do not publish a number without a label.
- Do not delete a source because it is inconvenient.

---

## Relationship to `raw/`

- `raw/` stores the source files and sidecars.
- `04-evidence/source-register.md` stores the claim-to-source map.
- `01-portfolio/` and `03-proposals/` store the argument.

A source is only "in the evidence base" when it appears in the register and (where possible) in `raw/`.
