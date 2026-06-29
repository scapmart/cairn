class MetricSnapshot:
    date: str

    portfolio_value: float
    exposure: dict[str, float]

    risk_score: float

    volatility: float

    drawdown: float