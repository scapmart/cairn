from cairn.scoring.metrics import TraderMetrics
from cairn.scoring.cognitive import detect_biases, why_it_might_be_wrong
from cairn.scoring.equity_curve import EquityCurveBuilder
from cairn.scoring.risk_engine import EquityRiskEngine


class TraderScorer:

    def __init__(self):
        self.m = TraderMetrics()
        self.curve_builder = EquityCurveBuilder()
        self.risk_engine = EquityRiskEngine()

    # -------------------------
    # RISK
    # -------------------------
    def compute_risk(self, metrics):

        leverage_risk = min(metrics["leverage"] / 20, 1.0)
        dd_risk = min(abs(metrics["max_dd"]) / 20, 1.0)
        vol_risk = min(metrics["volatility"], 1.0)

        return 0.4 * leverage_risk + 0.4 * dd_risk + 0.2 * vol_risk

    # -------------------------
    # SCORE
    # -------------------------
    def compute_score(self, metrics, risk):

        sharpe = max(-1, min(metrics["sharpe"], 1))
        dd = min(abs(metrics["max_dd"]) / 20, 1.0)
        vol = min(metrics["volatility"], 1.0)
        streak = min(metrics["streak"] / 3, 1.0)

        score = (
            metrics["winrate"] * 0.25 +
            (metrics["avg_pnl"] / 10) * 0.10 +
            metrics["consistency"] * 0.15 +
            sharpe * 0.25 -
            risk * 0.20 -
            dd * 0.10 -
            vol * 0.10 -
            streak * 0.05
            + metrics["activity"] * 0.10
        )

        return max(-1, min(score, 1))

    # -------------------------
    # CONFIDENCE
    # -------------------------
    def compute_confidence(self, metrics, risk, score):

        stability = metrics["consistency"]

        performance_signal = max(0, (score + 1) / 2)  # normalize -1..1 → 0..1

        confidence = (
            0.5 * stability +
            0.3 * performance_signal +
            0.2 * (1 - risk)
        )

        return max(0.05, min(confidence, 0.95))

    # -------------------------
    # MAIN
    # -------------------------
    def score(self, trader):

        curve = self.curve_builder.build(trader)
        risk_metrics = self.risk_engine.all(curve)

        metrics = {
            "winrate": self.m.winrate(trader),
            "avg_pnl": self.m.avg_pnl(trader),
            "max_dd": self.m.max_drawdown(trader),
            "leverage": self.m.leverage_risk(trader),
            "consistency": self.m.consistency(trader),
            "sharpe": risk_metrics["sharpe"],
            "volatility": risk_metrics["volatility"],
            "streak": risk_metrics["streak"],
            "activity": self.m.activity_score(trader),
        }

        risk = self.compute_risk(metrics)
        score = self.compute_score(metrics, risk)
        confidence = self.compute_confidence(metrics, risk, score)

        return {
            "trader_id": trader.id,
            "score": round(score, 3),
            "risk": round(risk, 3),
            "confidence": round(confidence, 3),
            "metrics": metrics,
            "biases": detect_biases(metrics),
            "why_it_might_be_wrong": why_it_might_be_wrong(metrics),
        }