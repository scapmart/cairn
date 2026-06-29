from .metrics import TraderMetrics
from .cognitive import detect_biases, why_it_might_be_wrong
from .config import *


class TraderScorer:

    def __init__(self):
        self.m = TraderMetrics()

    def score(self, trader):

        metrics = {
            "winrate": self.m.winrate(trader),
            "avg_pnl": self.m.avg_pnl(trader),
            "max_dd": self.m.max_drawdown(trader),
            "leverage": self.m.leverage_risk(trader),
            "consistency": self.m.consistency(trader),
        }

        score = (
            metrics["winrate"] * WINRATE_WEIGHT
            + (metrics["avg_pnl"] / 10) * PNL_WEIGHT
            + metrics["consistency"] * CONSISTENCY_WEIGHT
            - abs(metrics["max_dd"]) / 50 * RISK_WEIGHT
            - metrics["leverage"] / 50 * RISK_WEIGHT
        )

        confidence = max(0.05, min(score, 0.95))

        return {
            "trader_id": trader.id,
            "score": round(score, 3),
            "confidence": round(confidence, 3),
            "metrics": metrics,
            "biases": detect_biases(metrics),
            "why_it_might_be_wrong": why_it_might_be_wrong(metrics),
        }