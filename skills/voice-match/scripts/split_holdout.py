#!/usr/bin/env python3
"""Split each corpus/<source>.jsonl into a 90% main + 10% holdout split.

Stratified split: keep the same time/audience distribution in both halves so the
holdout is a representative blind-test sample, not a random slice.

Holdout rows are removed from corpus/<source>.jsonl and written to
corpus/holdout/<source>.jsonl.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

DEFAULT_CORPUS_DIR = Path(__file__).resolve().parent.parent / "corpus"


def stratified_split(rows: list[dict], holdout_frac: float, seed: int) -> tuple[list[dict], list[dict]]:
    rng = random.Random(seed)
    by_strat: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in rows:
        strat = r.get("stratum") or {}
        key = (str(strat.get("month", "?")), str(strat.get("audience", "?")))
        by_strat[key].append(r)

    main: list[dict] = []
    holdout: list[dict] = []
    for batch in by_strat.values():
        rng.shuffle(batch)
        n_holdout = max(1, int(round(len(batch) * holdout_frac))) if len(batch) >= 5 else 0
        holdout.extend(batch[:n_holdout])
        main.extend(batch[n_holdout:])
    rng.shuffle(main)
    rng.shuffle(holdout)
    return main, holdout


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--corpus-dir", type=Path, default=DEFAULT_CORPUS_DIR)
    p.add_argument("--holdout-frac", type=float, default=0.10)
    p.add_argument("--seed", type=int, default=23)
    args = p.parse_args()

    holdout_dir = args.corpus_dir / "holdout"
    holdout_dir.mkdir(parents=True, exist_ok=True)

    for jsonl in sorted(args.corpus_dir.glob("*.jsonl")):
        name = jsonl.stem
        rows = []
        with jsonl.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        if not rows:
            continue
        main_rows, holdout_rows = stratified_split(rows, args.holdout_frac, args.seed)
        with jsonl.open("w") as f:
            for r in main_rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        with (holdout_dir / f"{name}.jsonl").open("w") as f:
            for r in holdout_rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"{name}: {len(rows)} -> {len(main_rows)} main + {len(holdout_rows)} holdout")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
