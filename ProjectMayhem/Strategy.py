"""Legacy strategy helpers retained without broker side effects."""
from __future__ import annotations
from datetime import datetime, time


def check_trading_time(start_time_str: str, end_time_str: str, now: datetime | None = None) -> bool:
    current = (now or datetime.now()).time()
    start, end = time.fromisoformat(start_time_str), time.fromisoformat(end_time_str)
    return start <= current <= end if start <= end else current >= start or current <= end
