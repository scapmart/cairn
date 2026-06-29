from cairn.engine.cognitive_layer import CognitiveLayer
from cairn.decision.journal import DecisionJournal


class RecommendationEngine:

    def __init__(self):
        self.cognitive = CognitiveLayer()
        self.journal = DecisionJournal()

    def generate(self, portfolio, metrics):

        recommendations = []

        allocation = metrics["allocation"]
        worst = metrics["worst"]
        best = metrics["best"]

        btc_weight = allocation.get("BTC", 0)

        # ------------------------
        # RULE 1
        # ------------------------
        if btc_weight > 0.7:

            rec = {
                "type": "risk",
                "title": "Concentration BTC élevée",
                "severity": "warning",
                "action": "Réduire exposition BTC"
            }

            cognitive = self.cognitive.analyze(portfolio, rec, metrics)

            rec["why_wrong"] = cognitive.why_it_might_be_wrong
            rec["confidence"] = cognitive.confidence
            rec["biases"] = cognitive.bias_flags

            self.journal.record(portfolio, rec, decision="suggested")

            recommendations.append(rec)

        # ------------------------
        # RULE 2
        # ------------------------
        if worst.pnl_pct < -5:

            rec = {
                "type": "performance",
                "title": f"Sous-performance: {worst.asset.symbol}",
                "severity": "warning",
                "action": "Surveiller ou réduire position"
            }

            cognitive = self.cognitive.analyze(portfolio, rec, metrics)

            rec["why_wrong"] = cognitive.why_it_might_be_wrong
            rec["confidence"] = cognitive.confidence
            rec["biases"] = cognitive.bias_flags

            self.journal.record(portfolio, rec, decision="suggested")

            recommendations.append(rec)

        # ------------------------
        # RULE 3
        # ------------------------
        if best.pnl_pct > 5:

            rec = {
                "type": "opportunity",
                "title": f"Position forte: {best.asset.symbol}",
                "severity": "info",
                "action": "Éviter sur-optimisation émotionnelle"
            }

            cognitive = self.cognitive.analyze(portfolio, rec, metrics)

            rec["why_wrong"] = cognitive.why_it_might_be_wrong
            rec["confidence"] = cognitive.confidence
            rec["biases"] = cognitive.bias_flags

            self.journal.record(portfolio, rec, decision="suggested")

            recommendations.append(rec)

        return recommendations