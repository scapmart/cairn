class TraderRanking:

    def __init__(self, scorer):
        self.scorer = scorer

    def rank(self, traders):

        scored = []

        for t in traders:
            scored.append(self.scorer.score(t))

        scored.sort(key=lambda x: x["score"], reverse=True)

        return scored