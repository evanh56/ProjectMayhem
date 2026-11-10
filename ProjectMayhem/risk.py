"""Pure sizing and geometry guards; broker-specific calls remain in the adapter."""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class TradePlan:
    symbol: str; side: str; entry: float; stop: float; target: float; volume: float; risk_amount: float


def make_plan(symbol, side, entry, liquidity, point, equity, tick_value, tick_size, volume_min, volume_max, volume_step, risk_percent=2.0, target_r=2.0, buffer_points=5):
    if side not in {"buy", "sell"} or entry <= 0 or point <= 0 or tick_value <= 0 or tick_size <= 0: raise ValueError("invalid trade inputs")
    stop = liquidity - buffer_points * point if side == "buy" else liquidity + buffer_points * point
    distance = entry - stop if side == "buy" else stop - entry
    if distance <= 0: raise ValueError("stop is on the wrong side of entry")
    target = entry + target_r * distance if side == "buy" else entry - target_r * distance
    risk_amount = equity * min(risk_percent, 2.0) / 100
    loss_per_lot = distance / tick_size * tick_value
    volume = math.floor((risk_amount / loss_per_lot) / volume_step) * volume_step
    volume = round(min(volume, volume_max), 8)
    if volume < volume_min: raise ValueError("calculated volume below broker minimum")
    return TradePlan(symbol, side, entry, stop, target, volume, volume * loss_per_lot)
