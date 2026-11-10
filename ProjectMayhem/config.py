"""Side-effect-free configuration for the demo model."""
from __future__ import annotations
from dataclasses import dataclass
import os


def _bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)).strip())


def _float(name: str, default: float) -> float:
    return float(os.getenv(name, str(default)).strip())


@dataclass(frozen=True)
class Config:
    login: int | None
    password: str | None
    server: str | None
    live_trading: bool
    data_dir: str
    log_dir: str
    symbols: tuple[str, ...]
    h1_bars: int
    m15_bars: int
    max_spread_points: int
    max_quote_age_seconds: int
    risk_percent: float
    target_r: float
    stop_buffer_points: int
    signal_expiry_minutes: int
    session_start_utc: str
    session_end_utc: str


def load_config() -> Config:
    raw_login = os.getenv("MT5_LOGIN", "").strip()
    return Config(
        login=int(raw_login) if raw_login else None,
        password=os.getenv("MT5_PASSWORD") or None,
        server=os.getenv("MT5_SERVER") or None,
        live_trading=_bool("PM5_LIVE_TRADING"),
        data_dir=os.getenv("PM5_DATA_DIR", "ProjectMayhem/data"),
        log_dir=os.getenv("PM5_LOG_DIR", "ProjectMayhem/logs"),
        symbols=tuple(x.strip().upper() for x in os.getenv("PM5_SYMBOLS", "GBPJPY,USDJPY").split(",") if x.strip()),
        h1_bars=_int("PM5_H1_BARS", 250), m15_bars=_int("PM5_M15_BARS", 500),
        max_spread_points=_int("PM5_MAX_SPREAD_POINTS", 50), max_quote_age_seconds=_int("PM5_MAX_QUOTE_AGE_SECONDS", 30),
        risk_percent=_float("PM5_RISK_PERCENT", 2.0), target_r=_float("PM5_TARGET_R", 2.0),
        stop_buffer_points=_int("PM5_STOP_BUFFER_POINTS", 5), signal_expiry_minutes=_int("PM5_SIGNAL_EXPIRY_MINUTES", 60),
        session_start_utc=os.getenv("PM5_SESSION_START_UTC", "07:00"), session_end_utc=os.getenv("PM5_SESSION_END_UTC", "17:00"),
    )


def validate_config(c: Config) -> list[str]:
    errors = []
    for name, value in (("MT5_LOGIN", c.login), ("MT5_PASSWORD", c.password), ("MT5_SERVER", c.server)):
        if value in (None, ""): errors.append(f"missing {name}")
    if set(c.symbols) != {"GBPJPY", "USDJPY"}: errors.append("PM5_SYMBOLS must contain GBPJPY and USDJPY")
    if not 0 < c.risk_percent <= 2: errors.append("PM5_RISK_PERCENT must be between 0 and 2")
    if c.target_r <= 0 or c.stop_buffer_points < 0: errors.append("invalid risk geometry")
    return errors
