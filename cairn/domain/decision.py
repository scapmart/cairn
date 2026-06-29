class Decision:
    id: str

    recommendation_id: str

    decision: str  # "accepted", "rejected", "modified"

    reasoning: str

    timestamp: str

    outcome: str | None  # évalué plus tard

    outcome_notes: str | None