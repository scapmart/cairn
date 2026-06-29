class Bot:
    id: str

    name: str

    strategy: str

    pnl_30d: float

    max_drawdown: float

    sharpe: float | None

    trade_count: int

    status: str  # "active", "paused", "stopped"

    last_updated: str