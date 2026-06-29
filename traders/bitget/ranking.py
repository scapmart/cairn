from .scorer import TraderScorer


class TraderRanking:

    def rank(self, traders):

        scorer = TraderScorer()

        results = []

        for t in traders:
            try:
                results.append(scorer.score(t))
            except Exception:
                continue

        return sorted(results, key=lambda x: x["score"], reverse=True)