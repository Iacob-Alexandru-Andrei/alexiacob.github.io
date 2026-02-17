#!/usr/bin/env python3
"""Sync website CV/publications content from canonical LaTeX and DBLP sources.

This script keeps the website aligned with:
- CV source repo: Iacob-Alexandru-Andrei/Standard_CV_2023
- DBLP author profile: https://dblp.org/pid/346/2270

Outputs:
- assets/cv/main.tex
- _data/cv.yml
- _bibliography/papers.bib
- _data/publication_citations.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CV_TEX_DEST = ROOT / "assets" / "cv" / "main.tex"
DEFAULT_CV_DATA_DEST = ROOT / "_data" / "cv.yml"
DEFAULT_BIB_DEST = ROOT / "_bibliography" / "papers.bib"
DEFAULT_PUBLICATION_CITATIONS_DEST = ROOT / "_data" / "publication_citations.json"

DEFAULT_CV_REPO = "Iacob-Alexandru-Andrei/Standard_CV_2023"
DEFAULT_CV_BRANCH = "main"
DEFAULT_DBLP_PID = "346/2270"

# Preserve stable website keys where they already exist.
TITLE_KEY_OVERRIDES: dict[str, str] = {
    "deptdecoupledembeddingsforpretraininglanguagemodels": "dept-iclr-2025",
    "mtdaomultitimescaledistributedadaptiveoptimizerswithlocalupdates": "mtdao-iclr-2026",
    "deslocdesyncedlowcommunicationadaptiveoptimizersfortrainingfoundationmodels": "desloc-iclr-2026",
    "deslocdesyncedlowcommunicationadaptiveoptimizersforfoundationmodels": "desloc-iclr-2026",
    "thefutureoflargelanguagemodelpretrainingisfederated": "future-federated-pretraining-neurips-2024",
    "futureoflargelanguagemodelpretrainingisfederated": "future-federated-pretraining-neurips-2024",
    "photonfederatedllmpretraining": "photon-mlsys-2025",
    "lunarllmunlearningvianeuralactivationredirection": "unlearning-neurips-2025",
    "privacyinmultimodalfederatedhumanactivityrecognition": "multimodal-federated-har-2023",
    "worldwidefederatedtrainingoflanguagemodels": "worldwide-federated-training-neurips-2024",
    "canfairfederatedlearningreducetheneedforpersonalisation": "fair-federated-learning-euromlsys-2023",
    "rethinkingdatacurationinllmtrainingonlinereweightingoffersbettergeneralizationthanofflinemethods": "rethinking-data-curation-llm-training-iclr-2026",
}

# Manual BibTeX overrides for records where DBLP has not yet promoted the
# highest-venue version (for example, conference version vs. arXiv preprint).
BIBTEX_OVERRIDES_BY_KEY: dict[str, dict[str, Any]] = {
    "desloc-iclr-2026": {
        "venue": "ICLR",
        "year": 2026,
        "level": "conference",
        "source": "openreview:6N2qFixxYZ",
        "bibtex": """
@inproceedings{
iacob2026desloc,
title={{DES}-{LOC}: Desynced Low Communication Adaptive Optimizers for Foundation Models},
author={Alex Iacob and Lorenzo Sani and Mher Safaryan and Paris Giampouras and Samuel Horv{\\'a}th and Meghdad Kurmanji and Andrej Jovanovic and Preslav Aleksandrov and William F. Shen and Xinchi Qiu and Nicholas D. Lane},
booktitle={The Fourteenth International Conference on Learning Representations},
year={2026},
url={https://openreview.net/forum?id=6N2qFixxYZ}
}
""".strip(),
    },
    "mtdao-iclr-2026": {
        "venue": "ICLR",
        "year": 2026,
        "level": "conference",
        "source": "openreview:5yPP238v4c",
        "bibtex": """
@inproceedings{
iacob2026mtdao,
title={{MT}-{DAO}: Multi-Timescale Distributed Adaptive Optimizers with Local Updates},
author={Alex Iacob and Andrej Jovanovic and Mher Safaryan and Meghdad Kurmanji and Lorenzo Sani and Samuel Horv{\\'a}th and William F. Shen and Xinchi Qiu and Nicholas D. Lane},
booktitle={The Fourteenth International Conference on Learning Representations},
year={2026},
url={https://openreview.net/forum?id=5yPP238v4c}
}
""".strip(),
    },
    "unlearning-neurips-2025": {
        "venue": "NeurIPS",
        "year": 2025,
        "level": "conference",
        "source": "openreview:teB4aqJsNP",
        "bibtex": """
@inproceedings{
shen2025lunar,
title={{LUNAR}: {LLM} Unlearning via Neural Activation Redirection},
author={William F. Shen and Xinchi Qiu and Meghdad Kurmanji and Alex Iacob and Lorenzo Sani and Yihong Chen and Nicola Cancedda and Nicholas D. Lane},
booktitle={Advances in Neural Information Processing Systems},
year={2025},
url={https://openreview.net/forum?id=teB4aqJsNP}
}
""".strip(),
    },
}

# Manual additions when a publication is not yet available in DBLP under the
# desired venue/version. These entries are merged into generated outputs.
MANUAL_PUBLICATIONS: list[dict[str, Any]] = [
    {
        "key": "rethinking-data-curation-llm-training-iclr-2026",
        "venue": "ICLR",
        "year": 2026,
        "level": "conference",
        "source": "openreview:UFwnsmFZ6R",
        "bibtex": """
@inproceedings{
zhao2026rethinking,
title={Rethinking Data Curation in {LLM} Training: Online Reweighting Offers Better Generalization than Offline Methods},
author={Wanru Zhao and Yihong Chen and Wentao Ma and Yuzhi Tang and Shengchao Hu and Shell Xu Hu and Alex Iacob and Abhinav Mehrotra and Nicholas D. Lane},
booktitle={The Fourteenth International Conference on Learning Representations},
year={2026},
url={https://openreview.net/forum?id=UFwnsmFZ6R}
}
""".strip(),
    }
]


@dataclass(frozen=True)
class DblpCandidate:
    dblp_key: str
    entry_type: str
    title: str
    year: int
    venue: str
    rank: int
    level: str


def fetch_text(url: str, retries: int = 5) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "alexiacob-site-sync/1.0",
            "Accept": "text/plain,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
            return data.decode("utf-8")
        except urllib.error.HTTPError as error:
            retryable = error.code in {429, 500, 502, 503, 504}
            if not retryable or attempt == retries - 1:
                raise
            retry_after_raw = error.headers.get("Retry-After", "").strip()
            if retry_after_raw.isdigit():
                delay_seconds = max(int(retry_after_raw), 1)
            else:
                delay_seconds = min(2 ** attempt, 10)
            time.sleep(delay_seconds)
        except urllib.error.URLError:
            if attempt == retries - 1:
                raise
            time.sleep(min(2 ** attempt, 10))
    raise RuntimeError(f"Unreachable fetch failure for URL: {url}")


def write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return False
    path.write_text(content, encoding="utf-8")
    return True


def strip_tex_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def parse_bracketed(text: str, start: int, open_ch: str, close_ch: str) -> tuple[str, int]:
    if start >= len(text) or text[start] != open_ch:
        raise ValueError(f"Expected '{open_ch}' at index {start}")
    depth = 0
    i = start
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start + 1 : i], i + 1
        i += 1
    raise ValueError(f"Unclosed bracket starting at {start}")


def skip_ws(text: str, idx: int) -> int:
    while idx < len(text) and text[idx].isspace():
        idx += 1
    return idx


def iter_commands(text: str, name: str, arg_count: int) -> list[tuple[str | None, list[str]]]:
    token = f"\\{name}"
    idx = 0
    results: list[tuple[str | None, list[str]]] = []
    while True:
        pos = text.find(token, idx)
        if pos == -1:
            break
        after = pos + len(token)
        if after < len(text) and text[after].isalpha():
            idx = after
            continue
        cursor = skip_ws(text, after)
        optional: str | None = None
        if cursor < len(text) and text[cursor] == "[":
            optional, cursor = parse_bracketed(text, cursor, "[", "]")
            cursor = skip_ws(text, cursor)
        args: list[str] = []
        for _ in range(arg_count):
            cursor = skip_ws(text, cursor)
            if cursor >= len(text) or text[cursor] != "{":
                break
            arg, cursor = parse_bracketed(text, cursor, "{", "}")
            args.append(arg)
        results.append((optional, args))
        idx = cursor
    return results


def section_content(tex: str, section_name: str) -> str:
    marker = f"\\section{{{section_name}}}"
    start = tex.find(marker)
    if start == -1:
        return ""
    start += len(marker)
    end = tex.find("\\section{", start)
    if end == -1:
        return tex[start:]
    return tex[start:end]


def decode_latex_accents(text: str) -> str:
    accent_to_combining = {
        "'": "\u0301",
        "`": "\u0300",
        "^": "\u0302",
        '"': "\u0308",
        "~": "\u0303",
        "c": "\u0327",
    }

    def replace_accent(match: re.Match[str]) -> str:
        accent = match.group("accent")
        letter = match.group("letter")
        combining = accent_to_combining.get(accent)
        if not combining:
            return letter
        return unicodedata.normalize("NFC", letter + combining)

    patterns = [
        re.compile(r"\{\\(?P<accent>['\"`^~c])\{(?P<letter>[A-Za-z])\}\}"),
        re.compile(r"\\(?P<accent>['\"`^~c])\{(?P<letter>[A-Za-z])\}"),
        re.compile(r"\\(?P<accent>['\"`^~c])(?P<letter>[A-Za-z])"),
    ]

    out = text.replace("\\i", "i").replace("\\j", "j")
    for pattern in patterns:
        out = pattern.sub(replace_accent, out)
    return out


def latex_to_plain(text: str) -> str:
    out = text
    out = decode_latex_accents(out)

    while True:
        previous = out
        out = re.sub(r"\\href\s*\{[^{}]*\}\s*\{([^{}]*)\}", r"\1", out)
        for cmd in (
            "textbf",
            "textit",
            "textsb",
            "texttt",
            "emph",
            "textnormal",
            "textrm",
            "textsc",
            "underline",
        ):
            out = re.sub(rf"\\{cmd}\s*\{{([^{{}}]*)\}}", r"\1", out)
        if out == previous:
            break

    replacements = {
        "\\%": "%",
        "\\&": "&",
        "\\_": "_",
        "\\#": "#",
        "\\$": "$",
        "\\,": " ",
        "~": " ",
        "``": '"',
        "''": '"',
    }
    for src, dst in replacements.items():
        out = out.replace(src, dst)

    out = re.sub(r"\\newline\*?", " ", out)
    out = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", "", out)
    out = out.replace("{", "").replace("}", "")
    out = " ".join(out.split())
    return out.strip()


def parse_itemize_items(text: str) -> list[str]:
    items: list[str] = []
    for match in re.finditer(r"\\item\s*(.+?)(?=(?:\\item|\\end\{itemize\}))", text, flags=re.S):
        value = latex_to_plain(match.group(1))
        if value:
            items.append(value)
    return items


def split_csv_like(text: str) -> list[str]:
    parts: list[str] = []
    cursor: list[str] = []
    depth = 0
    for ch in text:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(depth - 1, 0)
        if ch == "," and depth == 0:
            part = "".join(cursor).strip()
            if part:
                parts.append(part)
            cursor = []
            continue
        cursor.append(ch)
    tail = "".join(cursor).strip()
    if tail:
        parts.append(tail)
    return [latex_to_plain(part) for part in parts if latex_to_plain(part)]


def extract_cv_data(tex: str) -> dict[str, Any]:
    source = strip_tex_comments(tex)

    education: list[dict[str, Any]] = []
    education_section = section_content(source, "Education")
    for _, args in iter_commands(education_section, "edentry", 6):
        if len(args) < 6:
            continue
        entry = {
            "period": latex_to_plain(args[0]),
            "degree": latex_to_plain(args[1]),
            "institution": latex_to_plain(args[2]),
            "details": parse_itemize_items(args[5]),
        }
        education.append(entry)

    experience: list[dict[str, Any]] = []
    work_section = section_content(source, "Work Experience")
    for _, args in iter_commands(work_section, "cventry", 6):
        if len(args) < 6:
            continue
        entry = {
            "period": latex_to_plain(args[0]),
            "role": latex_to_plain(args[1]),
            "organization": latex_to_plain(args[2]),
            "bullets": parse_itemize_items(args[5]),
        }
        experience.append(entry)

    skills: list[dict[str, Any]] = []
    skills_section = section_content(source, "Technical Skills")
    for _, args in iter_commands(skills_section, "cvitem", 2):
        if len(args) < 2:
            continue
        entry = {
            "category": latex_to_plain(args[0]),
            "items": split_csv_like(args[1]),
        }
        skills.append(entry)

    selected_publications: list[str] = []
    selected_section = section_content(source, "Selected Publications")
    for _, args in iter_commands(selected_section, "cvitem", 2):
        if len(args) < 2:
            continue
        label = latex_to_plain(args[0])
        text = latex_to_plain(args[1])
        if label and text:
            selected_publications.append(f"{label}: {text}")
        elif text:
            selected_publications.append(text)

    return {
        "education": education,
        "experience": experience,
        "skills": skills,
        "selected_publications": selected_publications,
    }


def normalize_for_key(text: str) -> str:
    plain = latex_to_plain(text).lower()
    plain = re.sub(r"[^a-z0-9]+", "", plain)
    return plain


def slugify(text: str) -> str:
    slug = latex_to_plain(text).lower()
    slug = slug.replace("&", " and ")
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def publication_level(entry_type: str, venue: str) -> tuple[int, str]:
    lowered = venue.lower()
    if "corr" in lowered or "arxiv" in lowered:
        return 1, "arxiv"
    if entry_type == "inproceedings":
        if "workshop" in lowered or "@" in venue:
            return 2, "workshop"
        return 3, "conference"
    if entry_type == "article":
        return 3, "journal"
    return 2, "other"


def work_identifier(title: str) -> str:
    plain = latex_to_plain(title).strip().rstrip(".")
    if ":" in plain:
        prefix = plain.split(":", 1)[0]
        normalized_prefix = normalize_for_key(prefix)
        if normalized_prefix:
            return normalized_prefix
    return normalize_for_key(plain)


def fetch_dblp_candidates(pid: str) -> list[DblpCandidate]:
    xml_text = fetch_text(f"https://dblp.org/pid/{pid}.xml")
    root = ET.fromstring(xml_text)
    out: list[DblpCandidate] = []
    for container in root.findall("r"):
        if not list(container):
            continue
        record = list(container)[0]
        key = record.attrib.get("key", "").strip()
        title = (record.findtext("title") or "").strip()
        year_text = (record.findtext("year") or "").strip()
        venue = (record.findtext("booktitle") or record.findtext("journal") or "").strip()
        if not key or not title or not year_text:
            continue
        try:
            year = int(year_text)
        except ValueError:
            continue
        rank, level = publication_level(record.tag, venue)
        out.append(
            DblpCandidate(
                dblp_key=key,
                entry_type=record.tag,
                title=title,
                year=year,
                venue=venue,
                rank=rank,
                level=level,
            )
        )
    return out


def select_highest_level_publications(candidates: list[DblpCandidate]) -> list[DblpCandidate]:
    best: dict[str, tuple[tuple[int, int, int], DblpCandidate]] = {}
    for candidate in candidates:
        key = work_identifier(candidate.title)
        score = (
            candidate.rank,
            candidate.year,
            1 if candidate.entry_type == "inproceedings" else 0,
        )
        current = best.get(key)
        if current is None or score > current[0]:
            best[key] = (score, candidate)
    selected = [item[1] for item in best.values()]
    selected.sort(key=lambda item: (item.year, latex_to_plain(item.title).lower()), reverse=True)
    return selected


def choose_publication_key(title: str, year: int, used: set[str]) -> str:
    normalized_title = normalize_for_key(title)
    if normalized_title in TITLE_KEY_OVERRIDES:
        base_key = TITLE_KEY_OVERRIDES[normalized_title]
    else:
        base_slug = slugify(title)
        base_key = f"{base_slug}-{year}" if year else base_slug

    key = base_key
    index = 2
    while key in used:
        key = f"{base_key}-{index}"
        index += 1
    used.add(key)
    return key


def fetch_bibtex_record(dblp_key: str) -> str:
    return fetch_text(f"https://dblp.org/rec/{dblp_key}.bib").strip()


def replace_bibtex_key(entry: str, new_key: str) -> str:
    return re.sub(r"^(@\w+\{)[^,]+,", rf"\1{new_key},", entry, count=1, flags=re.M)


def extract_bibtex_field(entry: str, field_name: str) -> str:
    field_pattern = re.compile(rf"^\s*{re.escape(field_name)}\s*=\s*", flags=re.M)
    match = field_pattern.search(entry)
    if not match:
        return ""
    index = match.end()
    while index < len(entry) and entry[index].isspace():
        index += 1
    if index >= len(entry) or entry[index] != "{":
        return ""
    value, _ = parse_bracketed(entry, index, "{", "}")
    return " ".join(value.split())


def bibtex_value_to_plain(value: str) -> str:
    text = value.replace("{-}", "-")
    text = decode_latex_accents(text)
    text = text.replace("{", "").replace("}", "")
    text = text.replace("~", " ")
    text = re.sub(r"\\[A-Za-z]+", "", text)
    text = text.replace("``", '"').replace("''", '"')
    text = " ".join(text.split())
    return text.strip()


def parse_bibtex_authors(entry: str) -> list[str]:
    raw = extract_bibtex_field(entry, "author")
    if not raw:
        return []
    cleaned = " ".join(raw.split())
    parts = [part.strip() for part in cleaned.split(" and ") if part.strip()]
    return [bibtex_value_to_plain(part) for part in parts]


def build_citation(authors: list[str], venue: str, year: int) -> str:
    if authors:
        author_text = ", ".join(authors)
    else:
        author_text = ""
    venue_text = venue.strip()

    fragments = []
    if author_text:
        fragments.append(f"{author_text}.")
    if venue_text:
        fragments.append(f"{venue_text} {year}.")
    else:
        fragments.append(f"{year}.")
    return " ".join(fragments)


def render_yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def dump_yaml(value: Any, indent: int = 0) -> list[str]:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {render_yaml_scalar(item)}")
        return lines
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{prefix}- {render_yaml_scalar(item)}")
        return lines
    return [f"{prefix}{render_yaml_scalar(value)}"]


def sync_cv(
    cv_source_file: Path | None,
    cv_repo: str,
    cv_branch: str,
    cv_tex_dest: Path,
    cv_data_dest: Path,
) -> tuple[bool, bool]:
    if cv_source_file:
        tex = cv_source_file.read_text(encoding="utf-8")
    else:
        raw_url = f"https://raw.githubusercontent.com/{cv_repo}/{cv_branch}/main.tex"
        tex = fetch_text(raw_url)

    tex_changed = write_if_changed(cv_tex_dest, tex)

    cv_data = extract_cv_data(tex)
    yaml_lines = [
        "# Auto-generated from assets/cv/main.tex by scripts/sync_cv_and_publications.py.",
        "# Do not edit this file manually; edit the LaTeX CV source instead.",
        "",
    ]
    yaml_lines.extend(dump_yaml(cv_data))
    yaml_lines.append("")
    cv_yaml = "\n".join(yaml_lines)
    data_changed = write_if_changed(cv_data_dest, cv_yaml)
    return tex_changed, data_changed


def sync_publications(
    dblp_pid: str,
    bib_dest: Path,
    citation_data_dest: Path,
) -> tuple[bool, bool, int]:
    candidates = fetch_dblp_candidates(dblp_pid)
    selected = select_highest_level_publications(candidates)

    used_keys: set[str] = set()
    entries: list[dict[str, Any]] = []

    for candidate in selected:
        publication_key = choose_publication_key(candidate.title, candidate.year, used_keys)

        override = BIBTEX_OVERRIDES_BY_KEY.get(publication_key)
        if override:
            rewritten = replace_bibtex_key(str(override["bibtex"]).strip(), publication_key)
            venue = str(override.get("venue", candidate.venue))
            year = int(override.get("year", candidate.year))
            level = str(override.get("level", candidate.level))
            source_key = str(override.get("source", candidate.dblp_key))
        else:
            bibtex = fetch_bibtex_record(candidate.dblp_key)
            rewritten = replace_bibtex_key(bibtex, publication_key)
            venue = candidate.venue
            year = candidate.year
            level = candidate.level
            source_key = candidate.dblp_key

        authors = parse_bibtex_authors(rewritten)
        title = bibtex_value_to_plain(extract_bibtex_field(rewritten, "title") or candidate.title)
        citation = build_citation(authors, venue, year)

        entries.append(
            {
                "key": publication_key,
                "dblp_key": source_key,
                "title": title,
                "year": year,
                "venue": venue,
                "level": level,
                "authors": authors,
                "citation": citation,
                "bibtex": rewritten,
            }
        )

    # Merge manual publications that are not yet surfaced in DBLP selection.
    existing_keys = {entry["key"] for entry in entries}
    for manual in MANUAL_PUBLICATIONS:
        publication_key = str(manual["key"])
        if publication_key in existing_keys:
            continue

        rewritten = replace_bibtex_key(str(manual["bibtex"]).strip(), publication_key)
        venue = str(manual["venue"])
        year = int(manual["year"])
        level = str(manual.get("level", "conference"))
        source_key = str(manual.get("source", publication_key))

        authors = parse_bibtex_authors(rewritten)
        title = bibtex_value_to_plain(extract_bibtex_field(rewritten, "title"))
        citation = build_citation(authors, venue, year)

        entries.append(
            {
                "key": publication_key,
                "dblp_key": source_key,
                "title": title,
                "year": year,
                "venue": venue,
                "level": level,
                "authors": authors,
                "citation": citation,
                "bibtex": rewritten,
            }
        )
        existing_keys.add(publication_key)

    entries.sort(key=lambda item: (item["year"], item["title"].lower()), reverse=True)

    bib_parts = [
        "% Auto-generated from DBLP by scripts/sync_cv_and_publications.py.",
        "% Selection policy: conference > workshop > arXiv (for duplicate works).",
        "",
    ]
    for entry in entries:
        bib_parts.append(entry["bibtex"].strip())
        bib_parts.append("")
    bib_text = "\n".join(bib_parts).rstrip() + "\n"
    bib_changed = write_if_changed(bib_dest, bib_text)

    citation_payload = {
        entry["key"]: {
            "title": entry["title"],
            "citation": entry["citation"],
            "venue": entry["venue"],
            "year": entry["year"],
            "authors": entry["authors"],
            "dblp_key": entry["dblp_key"],
            "level": entry["level"],
        }
        for entry in entries
    }
    citation_text = json.dumps(citation_payload, indent=2, ensure_ascii=False) + "\n"
    citation_changed = write_if_changed(citation_data_dest, citation_text)

    return bib_changed, citation_changed, len(entries)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-cv", action="store_true", help="Skip CV tex/data sync")
    parser.add_argument("--skip-publications", action="store_true", help="Skip DBLP publication sync")
    parser.add_argument("--cv-source-file", type=Path, help="Use local CV tex file instead of GitHub source")
    parser.add_argument("--cv-repo", default=DEFAULT_CV_REPO, help=f"GitHub repo owner/name (default: {DEFAULT_CV_REPO})")
    parser.add_argument("--cv-branch", default=DEFAULT_CV_BRANCH, help=f"GitHub branch/tag (default: {DEFAULT_CV_BRANCH})")
    parser.add_argument("--dblp-pid", default=DEFAULT_DBLP_PID, help=f"DBLP author PID (default: {DEFAULT_DBLP_PID})")
    parser.add_argument("--cv-tex-dest", type=Path, default=DEFAULT_CV_TEX_DEST, help="Destination for synced CV TeX")
    parser.add_argument("--cv-data-dest", type=Path, default=DEFAULT_CV_DATA_DEST, help="Destination for generated CV data YAML")
    parser.add_argument("--bib-dest", type=Path, default=DEFAULT_BIB_DEST, help="Destination for generated papers.bib")
    parser.add_argument(
        "--publication-citations-dest",
        type=Path,
        default=DEFAULT_PUBLICATION_CITATIONS_DEST,
        help="Destination for generated publication citations JSON",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    try:
        if not args.skip_cv:
            tex_changed, data_changed = sync_cv(
                cv_source_file=args.cv_source_file,
                cv_repo=args.cv_repo,
                cv_branch=args.cv_branch,
                cv_tex_dest=args.cv_tex_dest,
                cv_data_dest=args.cv_data_dest,
            )
            print(f"[cv] tex updated: {tex_changed}")
            print(f"[cv] data updated: {data_changed}")

        if not args.skip_publications:
            bib_changed, citation_changed, total = sync_publications(
                dblp_pid=args.dblp_pid,
                bib_dest=args.bib_dest,
                citation_data_dest=args.publication_citations_dest,
            )
            print(f"[pubs] selected publications: {total}")
            print(f"[pubs] bib updated: {bib_changed}")
            print(f"[pubs] citation data updated: {citation_changed}")

    except (OSError, urllib.error.URLError, ET.ParseError, ValueError) as error:
        print(f"sync failed: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
