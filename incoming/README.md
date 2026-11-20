# Incoming

**A loose drop zone for humans. The AI sorts it into the library.**

Drop any file into [`drop/`](drop/). It can be a PDF, a report, a dataset, a note, a screenshot, a media clipping or a draft. You do not need to name it properly or know where it belongs. The triage process classifies it, files it in [`../raw/`](../raw/), writes a metadata sidecar and updates the manifest.

The goal is simple: **the human should be able to dump, and the system should do the filing.**

---

## The workflow

```
incoming/drop/  →  triage  →  raw/<portfolio>/  →  sidecar + manifest
                         ↘  incoming/rejected/ (if unsafe or unreadable)
```

1. **Drop** the file into `incoming/drop/`. Do not rename it. Do not create subfolders.
2. **Run** the triage script in dry-run mode:
   ```bash
   python incoming/triage.py
   ```
3. **Review** the proposed destination, portfolio and document type. If a file is ambiguous, the script sends it to `raw/_unsorted/`.
4. **Apply**:
   ```bash
   python incoming/triage.py --apply
   ```
5. **Review** the sidecar and the manifest line. Correct the classification if needed.
6. **Promote** anything that is really a method (`00-method/`) or a proposal (`03-proposals/`) out of `raw/`.
7. **Link** the source from the relevant portfolio README and update the fact if it changes the evidence base.

The script is deterministic and does not delete anything. It moves files, writes metadata and appends to the log.

---

## Rules for humans

- **Do not drop sensitive personal information.** If a document contains names, addresses, health records or other personal data, redact it first or put it in a restricted system outside this repository.
- **Do not drop confidential commercial material** unless it is already public or you have permission to store it.
- **Do not drop giant files.** Link to them and drop a `.md` note with the URL.
- **One file per drop.** If you have a folder, zip it or drop the key documents.
- **Do not rename or move files inside `drop/` while triage is running.**
- **Do not put portfolio READMEs or proposals here.** They belong in `01-portfolio/` or `03-proposals/`.

---

## Rules for the AI

- Read the file, not just the filename. The filename is a hint, not a classification.
- Prefer the **primary policy relevance** over the publisher or the document type.
- If two portfolios score closely, choose the one the document would change most, and note the other in the sidecar.
- If the document is a **method** (skill, framework, template, playbook), send it to `00-method/` and also keep a raw copy.
- If the document is a **costed proposal**, send it to `03-proposals/<area>/` and link the raw source.
- If the document is **unsafe, unreadable or out of scope**, move it to `incoming/rejected/` with a `REASON.md` note. Do not delete it.
- Every filed source gets a sidecar and a manifest line. No exceptions.
- If a number in a portfolio README changes because of the new source, update the README and the source register.

---

## Folder map

| Folder | Purpose |
|---|---|
| [`drop/`](drop/) | The loose inbox. Drop files here. |
| [`processed/`](processed/) | A copy of the triage receipt for files that were filed. Optional; the manifest is the source of truth. |
| [`rejected/`](rejected/) | Files that could not be filed, with a `REASON.md`. |
| [`triage.py`](triage.py) | The classifier and filer. |
| [`triage-log.csv`](triage-log.csv) | Every triage action, with timestamp and destination. |
| [`TRIAGE.md`](TRIAGE.md) | The AI agent brief for ambiguous or high-value items. |

---

## Quick commands

```bash
# Dry run: show what would happen
python incoming/triage.py

# Apply: move, rename, write sidecars, update manifest
python incoming/triage.py --apply

# Keep original filenames (still writes metadata)
python incoming/triage.py --apply --keep-name

# Re-file a single file
python incoming/triage.py --apply --file "incoming/drop/my-report.pdf"
```

---

## What "organised" means

A source is organised when:

- It has a stable, dated filename.
- It sits in the portfolio folder it most directly informs.
- It has a sidecar with title, publisher, date, URL, confidence and what it supports.
- It has a manifest line.
- It is linked from the relevant portfolio README if it changes a material claim.
- It is labelled `[A]`, `[B]`, `[C]` or `[D]`.
