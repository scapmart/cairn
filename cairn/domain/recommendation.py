class Recommendation:
    id: str

    type: str
    # "reduce_exposure", "stop_trader", "rebalance", etc.

    title: str

    description: str

    confidence: float  # 0–1

    severity: str  # "info", "warning", "action"

    rationale: list[str]

    related_entities: list[str]

    created_at: str