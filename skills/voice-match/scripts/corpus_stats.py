#!/usr/bin/env python3
"""Compute stylometric baselines for each source in corpus/.

Outputs JSON per source to corpus/stats/<source>.json with both overall and
per-stratum metrics (by month, audience, length bucket, role). Distillation
passes consume this to ground voice rules in objective measurements rather than
guessing.

Usage:
    python scripts/corpus_stats.py                       # all sources
    python scripts/corpus_stats.py --source meetings     # one source
    python scripts/corpus_stats.py --spoken-features     # add filler metrics
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

DEFAULT_CORPUS_DIR = Path(__file__).resolve().parent.parent / "corpus"

HEDGES = (
    "maybe",
    "perhaps",
    "probably",
    "might",
    "kinda",
    "sorta",
    "i think",
    "i guess",
    "i suppose",
    "sort of",
    "kind of",
    "somewhat",
    "a bit",
    "a little",
    "fairly",
    "pretty much",
)

FILLERS = (
    " um ",
    " uh ",
    " umm ",
    " uhh ",
    " er ",
    " ah ",
    " like ",
    "you know",
    "i mean",
    " right? ",
    " so, ",
    " well, ",
    "basically",
    "literally",
    "honestly",
)

LLM_FILLER = (
    "it's worth noting",
    "it is worth noting",
    "let's dive in",
    "lets dive in",
    "it's important to note",
    "it is important to note",
    "in conclusion",
    "i hope this helps",
    "feel free to",
    "delve into",
    "navigate the",
    "tapestry of",
    "in today's fast-paced",
    "a testament to",
    "moreover,",
    "furthermore,",
)

FUNCTION_WORDS = {
    "a", "an", "the", "of", "in", "on", "at", "for", "to", "with", "by", "from",
    "and", "or", "but", "so", "if", "when", "while", "as", "than", "that",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "should", "could", "can", "may", "might",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their",
    "this", "these", "those", "what", "which", "who", "how", "why", "where",
    "not", "no", "just", "very", "really", "also", "only", "even", "still",
}

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[\"'(A-Z])")
PARA_SPLIT = re.compile(r"\n\s*\n")
WORD_RE = re.compile(r"\b[\w']+\b")


def percentiles(values: list[float], pcts: list[int]) -> dict[str, float]:
    if not values:
        return {f"p{p}": 0.0 for p in pcts}
    s = sorted(values)
    n = len(s)
    out: dict[str, float] = {}
    for p in pcts:
        k = int(round((p / 100) * (n - 1)))
        out[f"p{p}"] = float(s[k])
    return out


def count_phrases(text_lower: str, phrases: Iterable[str]) -> int:
    return sum(text_lower.count(p) for p in phrases)


def stylo_metrics(snippets: list[dict], spoken: bool = False) -> dict:
    sentence_lens: list[int] = []
    para_lens: list[int] = []
    type_counts: Counter[str] = Counter()
    function_word_counts: Counter[str] = Counter()
    total_words = 0
    total_chars = 0
    hedge_hits = 0
    filler_hits = 0
    llm_hits = 0
    em_dashes = 0
    semicolons = 0
    parens = 0
    ellipses = 0
    questions = 0

    for row in snippets:
        text = row.get("text") or ""
        if not text:
            continue
        text_lower = text.lower()
        for s in SENTENCE_SPLIT.split(text):
            words_in_sent = WORD_RE.findall(s)
            if words_in_sent:
                sentence_lens.append(len(words_in_sent))
        for para in PARA_SPLIT.split(text):
            words_in_para = WORD_RE.findall(para)
            if words_in_para:
                para_lens.append(len(words_in_para))
        words = WORD_RE.findall(text_lower)
        type_counts.update(words)
        total_words += len(words)
        total_chars += len(text)
        for w in words:
            if w in FUNCTION_WORDS:
                function_word_counts[w] += 1
        # Pad with surrounding spaces to make filler regex-style matches more robust.
        padded = " " + text_lower + " "
        hedge_hits += count_phrases(padded, HEDGES)
        if spoken:
            filler_hits += count_phrases(padded, FILLERS)
        llm_hits += count_phrases(text_lower, LLM_FILLER)
        em_dashes += text.count("\u2014") + text.count("--")
        semicolons += text.count(";")
        parens += text.count("(")
        ellipses += text.count("...") + text.count("\u2026")
        questions += text.count("?")

    n_words = max(1, total_words)
    metrics: dict = {
        "n_snippets": len(snippets),
        "total_words": total_words,
        "total_chars": total_chars,
        "sentence_length": {
            "mean": statistics.mean(sentence_lens) if sentence_lens else 0,
            "stdev": statistics.pstdev(sentence_lens) if len(sentence_lens) > 1 else 0,
            **percentiles(sentence_lens, [25, 50, 75, 90, 95]),
        },
        "paragraph_length": {
            "mean": statistics.mean(para_lens) if para_lens else 0,
            **percentiles(para_lens, [50, 90]),
        },
        "type_token_ratio": len(type_counts) / n_words if n_words else 0.0,
        "hedge_density_per_1k": 1000 * hedge_hits / n_words,
        "llm_filler_density_per_1k": 1000 * llm_hits / n_words,
        "punctuation_per_1k_words": {
            "em_dash": 1000 * em_dashes / n_words,
            "semicolon": 1000 * semicolons / n_words,
            "paren_open": 1000 * parens / n_words,
            "ellipsis": 1000 * ellipses / n_words,
            "question_mark": 1000 * questions / n_words,
        },
        "function_word_top": [
            {"word": w, "count": c, "freq_per_1k": 1000 * c / n_words}
            for w, c in function_word_counts.most_common(50)
        ],
    }
    if spoken:
        metrics["filler_density_per_1k"] = 1000 * filler_hits / n_words
    return metrics


def by_stratum(
    snippets: list[dict], key: str, sub: str | None = None
) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for row in snippets:
        if sub:
            val = (row.get(key) or {}).get(sub, "unknown")
        else:
            val = row.get(key, "unknown")
        out[str(val)].append(row)
    return dict(out)


def compute_for_source(snippets: list[dict], spoken: bool) -> dict:
    return {
        "overall": stylo_metrics(snippets, spoken=spoken),
        "by_month": {
            k: stylo_metrics(v, spoken=spoken)
            for k, v in by_stratum(snippets, "stratum", "month").items()
        },
        "by_audience": {
            k: stylo_metrics(v, spoken=spoken)
            for k, v in by_stratum(snippets, "stratum", "audience").items()
        },
        "by_length_bucket": {
            k: stylo_metrics(v, spoken=spoken)
            for k, v in by_stratum(snippets, "stratum", "length_bucket").items()
        },
        "by_role": {
            k: stylo_metrics(v, spoken=spoken)
            for k, v in by_stratum(snippets, "stratum", "role").items()
        },
    }


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-dir", type=Path, default=DEFAULT_CORPUS_DIR)
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="Restrict to one source (matches corpus/<source>.jsonl)",
    )
    parser.add_argument(
        "--spoken-features",
        action="store_true",
        help="Compute spoken-specific metrics (fillers etc.) for all sources",
    )
    args = parser.parse_args()

    out_dir = args.corpus_dir / "stats"
    out_dir.mkdir(parents=True, exist_ok=True)

    targets: list[tuple[str, Path]] = []
    for jsonl in sorted(args.corpus_dir.glob("*.jsonl")):
        name = jsonl.stem
        if args.source and name != args.source:
            continue
        targets.append((name, jsonl))

    if not targets:
        print("No corpus files found.", file=sys.stderr)
        return 1

    for name, path in targets:
        snippets = load_jsonl(path)
        spoken = args.spoken_features or name == "meetings"
        stats = compute_for_source(snippets, spoken=spoken)
        out_path = out_dir / f"{name}.json"
        with out_path.open("w") as f:
            json.dump(stats, f, indent=2, default=str)
        print(f"Wrote {out_path} ({len(snippets)} snippets)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
