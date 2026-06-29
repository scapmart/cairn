from dataclasses import dataclass
from typing import List
from .position import Position


@dataclass
class Portfolio:
    id: str
    positions: List[Position]

    total_value: float
    total_pnl_abs: float
    total_pnl_pct: float

    exposure: dict

    updated_at: str