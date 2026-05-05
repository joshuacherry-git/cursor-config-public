#!/usr/bin/env python3
"""Extract user turns from Cursor agent transcripts into the voice-match corpus.

Walks the user's local agent-transcripts tree, pulls role=user turns, strips
wrapper context blocks, dedupes near-duplicates, stratifies by session date /
session length / turn position, and writes JSONL to corpus/cursor-agents.jsonl.

Run from anywhere; defaults assume the script lives in
~/.cursor/skills/voice-match/scripts/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

DEFAULT_TRANSCRIPTS_DIR = (
    Path.home() / ".cursor/projects/Users-joshua-cherry-code/agent-transcripts"
)
DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "corpus/cursor-agents.jsonl"

USER_QUERY_RE = re.compile(r"<user_query>\s*(.*?)\s*</user_query>", re.DOTALL)
WRAPPER_TAG_RE = re.compile(
    r"<(external_links|system_reminder|attached_files|"
    r"open_and_recently_viewed_files|timestamp|user_info|agent_transcripts|"
    r"agent_skills|rules|mcp_file_system)[^>]*>.*?</\1>",
    re.DOTALL,
)


def extract_user_text(turn: dict) -> str | None:
    """Pull the user's actual prompt out of a turn, dropping injected context."""
    msg = turn.get("message") or {}
    content = msg.get("content") or []
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "text":
            parts.append(item.get("text") or "")
    raw = "\n".join(parts).strip()
    if not raw:
        return None
    matches = USER_QUERY_RE.findall(raw)
    if matches:
        return "\n\n".join(m.strip() for m in matches if m.strip()) or None
    cleaned = WRAPPER_TAG_RE.sub("", raw).strip()
    return cleaned or None


def length_bucket(text: str) -> str:
    n = len(text)
    if n < 30:
        return "xs"
    if n < 150:
        return "s"
    if n < 600:
        return "m"
    return "l"


def session_length_bucket(turn_count: int) -> str:
    if turn_count <= 2:
        return "short"
    if turn_count <= 8:
        return "iterative"
    return "extended"


def turn_position(idx: int, total: int) -> str:
    if idx == 0:
        return "opener"
    if idx == total - 1:
        return "closer"
    return "mid"


def signature(text: str) -> tuple[str, str, int]:
    """Cheap near-dup signature: first 3 + last 3 normalized words + length bucket."""
    tokens = re.findall(r"\w+", text.lower())
    if not tokens:
        return ("", "", 0)
    head = " ".join(tokens[:3])
    tail = " ".join(tokens[-3:])
    bucket = len(tokens) // 5
    return (head, tail, bucket)


def iter_transcripts(root: Path) -> Iterator[Path]:
    for sub in sorted(root.iterdir()):
        if not sub.is_dir():
            continue
        for jsonl in sub.glob("*.jsonl"):
            yield jsonl


def parse_session(path: Path) -> tuple[str, list[str]]:
    session_id = path.stem
    turns: list[str] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("role") != "user":
                continue
            text = extract_user_text(obj)
            if text:
                turns.append(text)
    return session_id, turns


def session_month(path: Path) -> str:
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return mtime.strftime("%Y-%m")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transcripts-dir", type=Path, default=DEFAULT_TRANSCRIPTS_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--max-turns", type=int, default=2000, help="Cap on output turns"
    )
    parser.add_argument(
        "--min-tokens", type=int, default=3, help="Skip turns with fewer than N words"
    )
    parser.add_argument("--seed", type=int, default=17, help="Sampling RNG seed")
    args = parser.parse_args()

    if not args.transcripts_dir.exists():
        print(f"Transcripts dir not found: {args.transcripts_dir}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)

    seen_signatures: set[tuple[str, str, int]] = set()
    rows: list[dict] = []
    skipped_dup = 0
    skipped_short = 0
    skipped_empty = 0

    for path in iter_transcripts(args.transcripts_dir):
        session_id, turns = parse_session(path)
        if not turns:
            skipped_empty += 1
            continue
        month = session_month(path)
        sess_bucket = session_length_bucket(len(turns))
        for idx, text in enumerate(turns):
            if len(re.findall(r"\w+", text)) < args.min_tokens:
                skipped_short += 1
                continue
            sig = signature(text)
            if sig in seen_signatures:
                skipped_dup += 1
                continue
            seen_signatures.add(sig)
            rows.append(
                {
                    "id": f"cursor-{hashlib.sha1(text.encode()).hexdigest()[:12]}",
                    "source": "cursor",
                    "text": text,
                    "ts": None,
                    "stratum": {
                        "month": month,
                        "audience": session_id,
                        "length_bucket": length_bucket(text),
                        "role": "initiator" if idx == 0 else "iterator",
                    },
                    "meta": {
                        "session_id": session_id,
                        "turn_index": idx,
                        "session_turns": len(turns),
                        "session_length_bucket": sess_bucket,
                        "turn_position": turn_position(idx, len(turns)),
                    },
                }
            )

    if len(rows) > args.max_turns:
        by_month: dict[str, list[dict]] = defaultdict(list)
        for r in rows:
            by_month[r["stratum"]["month"]].append(r)
        for batch in by_month.values():
            rng.shuffle(batch)
        per_bucket = max(1, args.max_turns // max(1, len(by_month)))
        sampled: list[dict] = []
        for month in sorted(by_month):
            sampled.extend(by_month[month][:per_bucket])
        rng.shuffle(sampled)
        rows = sampled[: args.max_turns]

    with args.output.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {len(rows)} turns to {args.output}", file=sys.stderr)
    print(
        f"Skipped: {skipped_dup} dupes, {skipped_short} short, "
        f"{skipped_empty} empty sessions",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
