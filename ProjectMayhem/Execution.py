"""Fail-closed paper execution. Live MT5 submission is deliberately not enabled here."""
from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from uuid import uuid4

@dataclass(frozen=True)
class Intent:
    intent_id: str; symbol: str; side: str; entry: float; stop: float; target: float; volume: float

class PaperExecutor:
    def __init__(self, directory="ProjectMayhem/logs"):
        self.path = Path(directory) / "order_intents.jsonl"; self.path.parent.mkdir(parents=True, exist_ok=True)
    def submit(self, symbol, side, entry, stop, target, volume):
        intent = Intent(uuid4().hex, symbol, side, entry, stop, target, volume)
        with self.path.open("a", encoding="utf-8") as f: f.write(json.dumps(asdict(intent), sort_keys=True) + "\n")
        return intent

def taketrade(*args, **kwargs):
    raise RuntimeError("live execution is disabled; use PaperExecutor")

def main(*args, **kwargs):
    return None
