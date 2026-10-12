from __future__ import annotations

from pathlib import Path
import json


def ensure_parent(path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def append_jsonl(path: str | Path, record: dict) -> None:
    p = ensure_parent(path)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def write_jsonl(path: str | Path, records: list[dict]) -> None:
    p = ensure_parent(path)
    with p.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, sort_keys=True) + "\n")


def write_summary_csv(path: str | Path, rows: list[dict]) -> None:
    p = ensure_parent(path)
    if not rows:
        p.write_text("condition,metric_name,value,unit\n", encoding="utf-8")
        return

    headers = sorted({key for row in rows for key in row})
    lines = [",".join(headers)]
    for row in rows:
        values = []
        for key in headers:
            value = row.get(key, "")
            values.append(str(value))
        lines.append(",".join(values))
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
