# Triage Brief

**How an AI agent should handle the incoming drop zone, especially the ambiguous or high-value items.**

The script does the mechanical filing. The agent does the judgement. This brief is the judgement layer.

---

## The job

When a human drops a file into `incoming/drop/`, the agent must answer four questions:

1. **What is it?** A primary source, a secondary source, a method, a proposal, a dataset, a media claim or a working note?
2. **Which policy area does it most change?** Not which department published it. Which README, costed proposal or source register should know about it.
3. **How confident are we?** A/B/C/D. What is the primary source behind the claim?
4. **What should happen next?** File it, promote it, link it, challenge it, or reject it.

---

## Step-by-step

### 1. Read before you file

- Read the first 10 pages of a PDF, the whole of a short note, and the metadata of a dataset.
- Do not trust the filename. A file called `final_v2.pdf` could be a budget paper or a consultant's pitch.
- Look for the publisher, date, methodology, data vintage and any caveats.

### 2. Run the dry run

```bash
python incoming/triage.py
```

Review every proposed destination. The script uses keyword scoring and high-confidence rules. It will get most things right and some things wrong.

### 3. Correct the classification

If the script is wrong:

- Move the file manually to `raw/<portfolio>/`.
- Write or edit the sidecar.
- Add a manifest line with a note explaining the correction.
- Add a log line in `incoming/triage-log.csv`.

Do not leave a misclassified file in the wrong portfolio just because the script put it there.

### 4. Apply

```bash
python incoming/triage.py --apply
```

Then review:

- `raw/_unsorted/` — every file here needs a human or AI decision.
- The new sidecars — add the URL, title, key figures and what the source supports.
- `raw/MANIFEST.csv` — check the rows.

### 5. Promote what is not a raw source

| If the file is... | It belongs in... |
|---|---|
| A skill, method, framework or playbook | `00-method/` (keep a raw copy) |
| A costed proposal or business case | `03-proposals/<area>/` (link the raw source) |
| A portfolio README draft | `01-portfolio/<area>/README.md` (merge, do not duplicate) |
| A lever README draft | `02-levers/<lever>/README.md` |
| A data extract | `raw/<area>/` and a note in `04-evidence/` |
| A media claim | `raw/<area>/` with `[C]` and a link to the primary source |
| A confidential or personal document | Outside this repository; leave a `RESTRICTED.md` pointer |

### 6. Update the evidence chain

If the source changes a material claim:

1. Update the relevant portfolio README and its confidence label.
2. Add the source to `04-evidence/source-register.md`.
3. If the source contradicts an existing source, add a line to the contradiction log in `04-evidence/README.md`.
4. If the source is a new proposal, add it to `03-proposals/README.md`.
5. If the source is a method, add it to `00-method/README.md`.

### 7. Do not delete

- Never delete a source because it is inconvenient.
- Never delete a file you did not create.
- If a file is unsafe, unreadable or out of scope, move it to `incoming/rejected/` and write a `REASON.md`.
- If a source is superseded, mark it `superseded` in the sidecar and manifest.

---

## Classification heuristics

| Signal | Likely destination |
|---|---|
| VAGO / Auditor-General report on roads, potholes, maintenance | `raw/07-transport-and-roads/` |
| VAGO / review on public sector overhead, consultants, executives | `raw/01-fiscal-and-public-sector/` |
| Planning, zoning, permits, VCAT, housing supply | `raw/02-housing-and-planning/` |
| Hospital, ambulance, ramping, patient flow | `raw/03-health-and-hospitals/` |
| Mental health, wellbeing, suicide, crisis | `raw/04-mental-health-and-wellbeing/` |
| School, teacher, early childhood, curriculum | `raw/05-education-and-early-childhood/` |
| TAFE, apprenticeship, skills, jobs, industry | `raw/06-skills-jobs-and-industry/` |
| Energy, renewables, SEC, coal, climate | `raw/08-energy-and-climate/` |
| Waste, recycling, water, catchment, environment | `raw/09-environment-water-and-circular-economy/` |
| Police, bail, courts, prisons, youth justice | `raw/10-justice-police-and-community-safety/` |
| Child protection, family violence, disability, carers | `raw/11-families-children-and-community/` |
| Regional, agriculture, drought, irrigation | `raw/12-regional-victoria-and-agriculture/` |
| Fire, flood, storm, emergency, resilience | `raw/13-emergency-management-and-resilience/` |
| Treaty, First Peoples, Aboriginal, multicultural | `raw/14-first-peoples-and-multicultural-affairs/` |
| Councils, rates, rate cap, local government | `raw/15-local-government-and-civic-infrastructure/` |
| Arts, creative, sport, tourism, events | `raw/16-arts-sport-and-tourism/` |
| Method, skill, framework, template | `00-method/` |
| Cross-cutting procurement, digital, regulation, integrity | `raw/00-cross-cutting/` |

---

## High-value items need extra care

A high-value item is one that could change a policy position, a cost estimate or a public claim. For these:

- Verify the primary source, not the summary.
- Check the vintage and the geography.
- Check the definition: FTE vs headcount, gross vs net, capital vs operating.
- Write down what would falsify the claim.
- Add a sensitivity range if the number is an estimate.
- Do not publish the number until it is labelled and sourced.

---

## Example: a new VAGO report

1. Drop `vago-report.pdf` into `incoming/drop/`.
2. Dry run: the script proposes `raw/07-transport-and-roads/` and `audit`.
3. Read the report. Confirm the portfolio. If it is about public sector consultants, move it to `raw/01-fiscal-and-public-sector/`.
4. Apply.
5. Edit the sidecar: title, publisher, date, URL, key findings, confidence [A].
6. Add a line to `04-evidence/source-register.md`.
7. Update the relevant portfolio README if the finding changes the baseline.
8. If the report contradicts an existing claim, add a contradiction log line.

---

## Example: a new method

1. Drop `10x-efficiency-skill.md`.
2. The script proposes `00-cross-cutting` and `method`.
3. Read it. If it is a reusable method, copy it to `00-method/` with a clear name.
4. Keep the raw copy and sidecar in `raw/00-cross-cutting/`.
5. Add it to `00-method/README.md`.
6. If it changes how proposals are built, update `00-method/operator-method.md` or `00-method/in-house-delivery-builder.md`.

---

## The test

A drop is handled well when a new reader can:

- Find the source.
- See who published it and when.
- Know how confident we are.
- See which policy area it informs.
- Trace the claim into the portfolio README.
- Challenge it without having to ask where it came from.
