class Trade:
    id: str

    asset: Asset

    side: str  # "buy" / "sell"

    size: float
    price: float

    fee: float

    realized_pnl: float

    opened_at: str
    closed_at: str | None

    source: str