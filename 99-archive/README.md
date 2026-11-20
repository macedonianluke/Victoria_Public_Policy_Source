# Archive

**Superseded structures, drafts and files. Append-only. Never delete history.**

The archive exists so that the current repository stays clean without losing the record of how it evolved.

---

## What changed in the 2026 reorganisation

| Old location | New location | Reason |
|---|---|---|
| `Skills/public-policy-inhouse-delivery-builder.md` | [`00-method/in-house-delivery-builder.md`](../00-method/in-house-delivery-builder.md) | A method is not a policy area. The `Skills/` folder was retired. |
| `Skills/Policies/Transport/Bringing Victorian Pothole & Road Patching Back In-House.md` | [`03-proposals/transport-and-roads/potholes-in-house/README.md`](../03-proposals/transport-and-roads/potholes-in-house/README.md) | Detailed proposals live in `03-proposals/`, not in the portfolio layer. |
| Loose raw files in `raw/` | [`raw/00-cross-cutting/`](../raw/00-cross-cutting/), [`raw/01-fiscal-and-public-sector/`](../raw/01-fiscal-and-public-sector/), [`raw/02-housing-and-planning/`](../raw/02-housing-and-planning/), [`raw/07-transport-and-roads/`](../raw/07-transport-and-roads/) | Sources are filed by primary policy relevance, with sidecars and manifest lines. |
| Incoming drops | [`incoming/drop/`](../incoming/drop/) → `raw/` | Humans can dump loose files; the triage process files them. |

---

## Superseded methods

| File | Status | Superseded by |
|---|---|---|
| [`00-method/in-house-delivery-builder.md`](../00-method/in-house-delivery-builder.md) | v1, retained for history | [`00-method/in-house-delivery-builder-v2.md`](../00-method/in-house-delivery-builder-v2.md) |
| [`00-method/10x-efficiency-engine.md`](../00-method/10x-efficiency-engine.md) | v3.0, current | — |

---

## Archive rules

- **Append-only.** Do not overwrite an archived file. Add a new dated copy or a note explaining the change.
- **Keep the provenance.** Record the original path, the new path, the date and the reason.
- **Do not archive a live source.** If a source is still used, keep it in `raw/` and mark it `superseded` in the sidecar.
- **Do not archive a proposal that is still under development.** Move it to `03-proposals/` and mark its status.
- **No deletion.** If a file is unsafe, move it to `incoming/rejected/` with a reason. If it is obsolete, archive it here.

---

## Archive contents

```
99-archive/
├── README.md
├── 2026-11-reorganisation/
│   ├── old-skills-tree.md
│   ├── migration-log.csv
│   └── superseded-drafts/
└── ...
```

Create a dated folder for each significant reorganisation, with a migration log and a copy of any superseded draft that is not already preserved in Git history.
