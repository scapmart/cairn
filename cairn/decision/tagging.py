class DecisionTagger:

    @staticmethod
    def tag(result):
        metrics = result["metrics"]
        biases = result.get("biases", [])

        if metrics["avg_pnl"] <= 0:
            return "IGNORE"

        if "luck_based_returns" in biases:
            return "WATCH"

        if metrics["sharpe"] < 0 and result["score"] < 0.40:
            return "WATCH"

        if metrics["avg_pnl"] <= 0:
            return "IGNORE"

        if (
            result["score"] >= 0.25
            and result["risk"] <= 0.52
            and result["confidence"] >= 0.70
        ):
            return "STRONG_WATCH"

        if (
            result["score"] >= 0.20
            and result["risk"] <= 0.50
            and result["confidence"] >= 0.70
        ):
            return "INVEST"

        if (
            result["score"] >= 0.10
            and result["confidence"] >= 0.55
        ):
            return "WATCH"

        if result["risk"] >= 0.60:
            return "HIGH_RISK"

        if result["confidence"] <= 0.30:
            return "LOW_CONFIDENCE"

        return "IGNORE"