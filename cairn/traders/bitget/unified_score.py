from dataclasses import dataclass

@dataclass
class TraderScore:
    trader_id: str
    score: float
    confidence: float
    metrics: dict
    biases: list
    risks: list
    debug: dict = None