#!/usr/bin/env python3
"""Triage loose files in incoming/drop/ into the raw/ evidence library.

Default is a dry run. Use --apply to move files, write sidecars and update the
manifest. The script never deletes files and never overwrites an existing file.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DROP = ROOT / "incoming" / "drop"
RAW = ROOT / "raw"
MANIFEST = RAW / "MANIFEST.csv"
LOG = ROOT / "incoming" / "triage-log.csv"
SIDECAR_SUFFIX = ".meta.md"

HEADERS = [
    "filed_date",
    "original_filename",
    "filed_path",
    "portfolio",
    "document_type",
    "publisher",
    "date",
    "confidence",
    "notes",
]

# Primary policy relevance. Keep names aligned with 01-portfolio/.
KEYWORDS = {
    "00-cross-cutting": [
        ("method", 6), ("framework", 4), ("template", 5), ("skill", 6),
        ("playbook", 5), ("efficiency", 4), ("governance", 3), ("reform", 2),
        ("procurement", 2), ("digital", 2), ("artificial intelligence", 3),
        ("regulation", 2), ("federalism", 3), ("integrity", 2),
        ("cost of living", 3), ("policy", 1),
    ],
    "01-fiscal-and-public-sector": [
        ("budget", 5), ("treasury", 5), ("public sector", 5), ("overhead", 6),
        ("duplication", 6), ("consultant", 5), ("executive", 4), ("vps", 5),
        ("deficit", 4), ("debt", 4), ("fiscal", 5), ("efficiency", 3),
        ("workforce", 2), ("shared services", 5), ("entity", 3),
    ],
    "02-housing-and-planning": [
        ("housing", 6), ("planning", 6), ("zoning", 6), ("building permit", 6),
        ("planning permit", 6), ("vcat", 6), ("dwelling", 5), ("homes", 4),
        ("precinct", 4), ("rent", 4), ("construction", 3), ("approval", 3),
        ("townhouse", 5), ("apartment", 4),
    ],
    "03-health-and-hospitals": [
        ("hospital", 6), ("ambulance", 6), ("ramping", 6),
        ("emergency department", 6), ("patient", 5), ("health service", 5),
        ("healthcare", 4), ("surgery", 5), ("bed", 3), ("nurse", 3),
    ],
    "04-mental-health-and-wellbeing": [
        ("mental health", 8), ("wellbeing", 5), ("suicide", 6), ("crisis", 4),
        ("peer", 3), ("psychosocial", 5), ("mental health and wellbeing", 8),
    ],
    "05-education-and-early-childhood": [
        ("school", 6), ("teacher", 6), ("education", 5), ("early childhood", 6),
        ("kindergarten", 5), ("curriculum", 5), ("student", 5),
        ("principal", 4), ("schooling", 5),
    ],
    "06-skills-jobs-and-industry": [
        ("skills", 5), ("tafe", 7), ("apprenticeship", 7), ("training", 4),
        ("jobs", 4), ("industry", 4), ("manufacturing", 5), ("vocational", 5),
        ("employer", 3), ("workforce", 3), ("free tafe", 7),
    ],
    "07-transport-and-roads": [
        ("road", 6), ("pothole", 8), ("jetpatcher", 8), ("transport", 5),
        ("rail", 5), ("tram", 5), ("bus", 4), ("traffic", 5), ("freeway", 5),
        ("arterial", 5), ("metro tunnel", 5), ("suburban rail loop", 5),
        ("mobility", 4),
    ],
    "08-energy-and-climate": [
        ("energy", 6), ("electricity", 6), ("renewable", 6), ("solar", 6),
        ("battery", 6), ("sec", 4), ("coal", 6), ("gas", 4), ("climate", 5),
        ("emissions", 5), ("grid", 5), ("electrification", 5),
    ],
    "09-environment-water-and-circular-economy": [
        ("waste", 6), ("recycling", 6), ("circular", 6), ("water", 5),
        ("catchment", 5), ("environment", 4), ("container deposit", 6),
        ("epa", 4), ("parks", 3), ("biodiversity", 4), ("landfill", 5),
    ],
    "10-justice-police-and-community-safety": [
        ("police", 6), ("crime", 6), ("bail", 6), ("prison", 6),
        ("corrections", 6), ("court", 5), ("justice", 5),
        ("youth justice", 6), ("victim", 4), ("recidivism", 5),
    ],
    "11-families-children-and-community": [
        ("family", 4), ("child protection", 7), ("family violence", 7),
        ("disability", 6), ("carer", 5), ("seniors", 4), ("kinship", 6),
        ("out-of-home care", 7), ("orange door", 6), ("ndis", 5),
    ],
    "12-regional-victoria-and-agriculture": [
        ("regional", 6), ("agriculture", 7), ("farm", 6), ("drought", 6),
        ("irrigation", 6), ("rural", 5), ("regional development", 6),
        ("food", 3), ("agribusiness", 6),
    ],
    "13-emergency-management-and-resilience": [
        ("emergency", 6), ("fire", 6), ("flood", 6), ("storm", 4),
        ("bushfire", 7), ("cfa", 6), ("ses", 5), ("resilience", 5),
        ("disaster", 5), ("recovery", 4),
    ],
    "14-first-peoples-and-multicultural-affairs": [
        ("treaty", 8), ("first peoples", 8), ("aboriginal", 7),
        ("yoorrook", 8), ("gelung", 8), ("multicultural", 6), ("racism", 5),
        ("cultural safety", 5), ("self-determination", 5),
    ],
    "15-local-government-and-civic-infrastructure": [
        ("local government", 7), ("council", 5), ("rates", 4),
        ("rate cap", 7), ("councillor", 6), ("municipal", 5),
        ("local council", 6), ("ratepayers", 5),
    ],
    "16-arts-sport-and-tourism": [
        ("arts", 6), ("creative", 5), ("sport", 5), ("tourism", 6),
        ("major event", 6), ("screen", 5), ("music", 4), ("games", 4),
        ("festival", 4), ("culture", 3), ("visitor economy", 5),
    ],
}

# High-confidence overrides. Checked before scoring. Order matters.
RULES = [
    (r"public sector overhead|overhead.{0,20}duplication|duplication.{0,20}public sector", "01-fiscal-and-public-sector"),
    (r"pothole|jetpatcher|road maintenance|road condition|patching", "07-transport-and-roads"),
    (r"planning permit|building permit|zoning|vcat|townhouse|dwelling|planning reform", "02-housing-and-planning"),
    (r"treaty|yoorrook|first peoples|aboriginal|gelung|multicultural", "14-first-peoples-and-multicultural-affairs"),
    (r"family violence|child protection|kinship|out-of-home care|orange door|ndis", "11-families-children-and-community"),
    (r"bushfire|flood|storm|emergency management|vicses|cfa|fire rescue", "13-emergency-management-and-resilience"),
    (r"container deposit|recycling|circular economy|landfill|waste", "09-environment-water-and-circular-economy"),
    (r"local government|rate cap|council rates|councillor", "15-local-government-and-civic-infrastructure"),
    (r"tafe|apprenticeship|free tafe|vocational", "06-skills-jobs-and-industry"),
    (r"teacher|school|curriculum|early childhood|kindergarten", "05-education-and-early-childhood"),
    (r"hospital|ambulance|ramping|emergency department", "03-health-and-hospitals"),
    (r"mental health|wellbeing|suicide|psychosocial", "04-mental-health-and-wellbeing"),
    (r"police|bail|prison|corrections|youth justice|crime", "10-justice-police-and-community-safety"),
    (r"agriculture|farm|drought|irrigation|regional development", "12-regional-victoria-and-agriculture"),
    (r"renewable|solar|battery|electricity|coal|electrification|energy", "08-energy-and-climate"),
    (r"creative industries|tourism|major event|sport|screen|festival", "16-arts-sport-and-tourism"),
]

MONTHS = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12",
}

PUBLISHERS = [
    ("victorian auditor-general", "vago"),
    ("vago", "vago"),
    ("auditor-general", "vago"),
    ("department of treasury and finance", "dtf"),
    ("dtf", "dtf"),
    ("department of energy, environment and climate action", "deeca"),
    ("deeca", "deeca"),
    ("department of jobs, skills, industry and regions", "djsir"),
    ("djsir", "djsir"),
    ("department of health", "health-vic"),
    ("department of education", "education-vic"),
    ("department of families, fairness and housing", "dffh"),
    ("dffh", "dffh"),
    ("department of justice and community safety", "djcs"),
    ("djcs", "djcs"),
    ("department of transport and planning", "dtp"),
    ("dtp", "dtp"),
    ("department of premier and cabinet", "dpc"),
    ("dpc", "dpc"),
    ("parliament of victoria", "parliament-vic"),
    ("victorian parliament", "parliament-vic"),
    ("productivity commission", "productivity-commission"),
    ("grattan institute", "grattan"),
    ("reserve bank of australia", "rba"),
    ("australian bureau of statistics", "abs"),
    ("abc news", "abc-news"),
    ("the age", "the-age"),
    ("herald sun", "herald-sun"),
]


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt", ".csv", ".json", ".html", ".htm", ".xml"}:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return ""
    if suffix == ".pdf":
        try:
            result = subprocess.run(
                ["pdftotext", "-layout", str(path), "-"],
                capture_output=True,
                text=True,
                timeout=45,
            )
            if result.returncode == 0:
                return result.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            pass
        try:
            from pypdf import PdfReader  # type: ignore

            reader = PdfReader(str(path))
            pages = []
            for page in reader.pages[:20]:
                pages.append(page.extract_text() or "")
            return "\n".join(pages)
        except Exception:
            return ""
    return ""


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-")


def guess_date(filename: str, text: str) -> str:
    # Prefer explicit metadata, then an ISO date, then a month/year near the
    # start. Do not use a bare year: forward estimates and citations produce
    # false dates.
    head = text[:1500]
    haystack = f"{filename}\n{head}"
    labelled = re.search(
        r"(?:date|published|publication date)\s*[:\-]\s*"
        r"(?:\d{1,2}\s+)?"
        r"(january|february|march|april|may|june|july|august|september|october|november|december)?\s*"
        r"(20\d{2})",
        haystack,
        re.IGNORECASE,
    )
    if labelled and labelled.group(1):
        return f"{labelled.group(2)}-{MONTHS[labelled.group(1).lower()]}"
    iso = re.search(r"(20\d{2})[-_/](0[1-9]|1[0-2])[-_/](0[1-9]|[12]\d|3[01])", haystack)
    if iso:
        return f"{iso.group(1)}-{iso.group(2)}-{iso.group(3)}"
    month = re.search(
        r"(january|february|march|april|may|june|july|august|september|october|november|december)\s+(20\d{2})",
        haystack[:800],
        re.IGNORECASE,
    )
    if month:
        return f"{month.group(2)}-{MONTHS[month.group(1).lower()]}"
    return "undated"


def guess_publisher(filename: str, text: str) -> str:
    # Attribute only from the filename or an explicit metadata label. Scanning
    # the body catches cited publishers (VAGO, DTF) and misattributes the file.
    name = filename.lower()
    for needle, slug in PUBLISHERS:
        if needle in name:
            return slug
    head = f"{filename}\n{text[:400]}".lower()
    labelled = re.search(r"(?:publisher|author|prepared by|commissioned by)\s*[:\-]\s*([^\n]{2,120})", head)
    if labelled:
        value = labelled.group(1).strip().lower()
        for needle, slug in PUBLISHERS:
            if needle in value:
                return slug
        return slugify(value)[:60] or "unknown"
    return "unknown"


def guess_doc_type(filename: str, text: str) -> str:
    name = filename.lower().replace("_", " ").replace("-", " ")
    header = f"{name}\n{text[:1200]}".lower()
    frontmatter = text[:600].lower()
    if re.search(r"\b(skill|method|playbook|template|builder)\b", name):
        return "method"
    if re.search(r"^---\s*\nname:", frontmatter) and "skill" in text[:3000].lower():
        return "method"
    if re.search(r"\b(policy brief|proposal|business case|blueprint)\b", header):
        return "proposal"
    if "auditor-general" in header or "vago" in header or re.search(r"\baudit\b", header):
        return "audit"
    if "annual report" in header:
        return "annual-report"
    if re.search(r"\bbudget\b", header):
        return "budget"
    if re.search(r"\b(bill|act|regulation)\b", header):
        return "legislation"
    if re.search(r"\b(strategy|plan)\b", header):
        return "strategy"
    if re.search(r"\breview\b", header):
        return "review"
    if re.search(r"\b(research|report|analysis)\b", header):
        return "research"
    if re.search(r"\b(data|csv|xlsx|dataset)\b", header):
        return "data"
    if re.search(r"\b(news|abc|herald|the age)\b", header):
        return "media"
    return "source"


def classify(filename: str, text: str) -> tuple[str, int, list[str], bool]:
    haystack = f"{filename}\n{text}".lower()
    normalised_name = filename.lower().replace("_", " ").replace("-", " ")
    method_hint = bool(re.search(r"\b(skill|method|playbook|template|builder)\b", normalised_name))
    method_hint = method_hint or (
        bool(re.search(r"^---\s*\nname:", text[:600], re.IGNORECASE | re.MULTILINE))
        and "skill" in text[:3000].lower()
    )
    if method_hint:
        return "00-cross-cutting", 100, ["method/skill hint"], False

    for pattern, portfolio in RULES:
        if re.search(pattern, haystack):
            return portfolio, 50, [pattern], False

    scores: dict[str, int] = {}
    matches: dict[str, list[str]] = {}
    for portfolio, terms in KEYWORDS.items():
        total = 0
        found = []
        for term, weight in terms:
            count = haystack.count(term)
            if count:
                total += min(count, 5) * weight
                found.append(term)
        scores[portfolio] = total
        matches[portfolio] = found

    best = max(scores, key=lambda key: scores[key])
    best_score = scores[best]
    if best_score == 0:
        return "_unsorted", 0, [], True

    # A tie is a signal to review, not a confident classification.
    tied = [key for key, value in scores.items() if value == best_score]
    ambiguous = len(tied) > 1
    return best, best_score, matches[best][:8], ambiguous


def unique_destination(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    counter = 2
    while True:
        candidate = dest.with_name(f"{stem}-{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def write_sidecar(dest: Path, meta: dict) -> Path:
    sidecar = dest.with_name(dest.stem + SIDECAR_SUFFIX)
    lines = [
        "# Source Metadata",
        "",
        f"- **Original filename:** `{meta['original_filename']}`",
        f"- **Filed:** `{meta['filed_path']}`",
        f"- **Portfolio:** `{meta['portfolio']}`",
        f"- **Document type:** `{meta['document_type']}`",
        f"- **Publisher:** `{meta['publisher']}`",
        f"- **Date:** `{meta['date']}`",
        "- **Confidence:** `[C]` auto-filed; verify against the primary source before citing.",
        f"- **Classification score:** `{meta['score']}`",
        f"- **Ambiguous:** `{'yes' if meta['ambiguous'] else 'no'}`",
        f"- **Matched terms:** {', '.join(meta['matched']) if meta['matched'] else 'none'}",
        f"- **Filed on:** `{meta['filed_date']}`",
        "- **Notes:** Auto-filed by `incoming/triage.py`. Review this sidecar, correct the portfolio if needed, and add the URL, key figures and what the source supports.",
        "",
        "## Review checklist",
        "",
        "- [ ] Title and publisher confirmed",
        "- [ ] Date and URL confirmed",
        "- [ ] Confidence label confirmed (A/B/C/D)",
        "- [ ] Key figures linked to the relevant portfolio README",
        "- [ ] Cross-portfolio relevance noted",
        "",
    ]
    sidecar.write_text("\n".join(lines), encoding="utf-8")
    return sidecar


def append_csv(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        if not exists:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in HEADERS})


def triage_file(path: Path, apply: bool, keep_name: bool) -> dict:
    text = extract_text(path)
    portfolio, score, matched, ambiguous = classify(path.name, text)
    doc_type = guess_doc_type(path.name, text)
    publisher = guess_publisher(path.name, text)
    date = guess_date(path.name, text)
    confidence = "[C]"

    if keep_name:
        filename = path.name
    else:
        title = path.stem
        filename = f"{date}__{publisher}__{slugify(title)}{path.suffix.lower()}"

    dest_dir = RAW / portfolio
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = unique_destination(dest_dir / filename)

    filed_date = datetime.now().strftime("%Y-%m-%d")
    row = {
        "filed_date": filed_date,
        "original_filename": path.name,
        "filed_path": str(dest.relative_to(ROOT)).replace("\\", "/"),
        "portfolio": portfolio,
        "document_type": doc_type,
        "publisher": publisher,
        "date": date,
        "confidence": confidence,
        "notes": (
            f"auto-filed; score={score}; ambiguous={'yes' if ambiguous else 'no'}; "
            f"matched={', '.join(matched) if matched else 'none'}"
        ),
        "score": score,
        "matched": matched,
        "ambiguous": ambiguous,
    }

    if apply:
        shutil.move(str(path), str(dest))
        write_sidecar(dest, row)
        append_csv(MANIFEST, row)
        append_csv(LOG, row)

    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="File loose incoming documents into raw/.")
    parser.add_argument("--apply", action="store_true", help="Move files and write metadata. Default is a dry run.")
    parser.add_argument("--keep-name", action="store_true", help="Keep the original filename instead of renaming.")
    parser.add_argument("--file", help="Triage a single file instead of the whole drop folder.")
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        if not path.is_absolute():
            path = ROOT / path
        files = [path] if path.is_file() else []
    else:
        files = sorted(
            p for p in DROP.rglob("*")
            if p.is_file()
            and not p.name.startswith(".")
            and p.name.lower() != "readme.md"
        )

    if not files:
        print(f"No files to triage in {DROP}")
        return 0

    rows = []
    for path in files:
        row = triage_file(path, apply=args.apply, keep_name=args.keep_name)
        rows.append(row)
        print(
            f"{'FILED' if args.apply else 'WOULD FILE'}  {path.name}\n"
            f"    -> {row['filed_path']}\n"
            f"    portfolio={row['portfolio']} type={row['document_type']} "
            f"publisher={row['publisher']} date={row['date']} "
            f"score={row['score']} ambiguous={'yes' if row['ambiguous'] else 'no'}"
        )

    if not args.apply:
        print("\nDry run only. Re-run with --apply to move files and write metadata.")
    else:
        print(f"\nFiled {len(rows)} file(s). Review raw/_unsorted/ and the sidecars.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
