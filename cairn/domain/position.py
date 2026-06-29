class Position:
    id: str
    asset: Asset

    size: float
    entry_price: float
    current_price: float

    pnl_abs: float
    pnl_pct: float

    leverage: float | None

    opened_at: str
    updated_at: str

    source: str  # "bitget", "okx", "csv"