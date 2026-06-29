from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Trade:
    pnl_pct: float
    duration_hours: float
    leverage: float
    is_win: bool


@dataclass
class Trader:
    id: str
    trades: List[Trade]
    equity_curve: Optional[list] = None  # futur support