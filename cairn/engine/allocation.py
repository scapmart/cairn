class AllocationEngine:

    def compute_weights(self, ranked_traders):

        raw = []

        for r in ranked_traders:

            score = (r["score"] + 1) / 2   # squash [-1,1] → [0,1]
            confidence = r["confidence"]
            risk = r["risk"]

            weight = score * confidence * (1 - risk)

            raw.append({
                "trader_id": r["trader_id"],
                "weight": weight
            })

        # normalize
        total = sum(w["weight"] for w in raw) or 1

        for w in raw:
            w["allocation_pct"] = w["weight"] / total

        # diversification smoothing
        for w in raw:
            w["allocation_pct"] = max(w["allocation_pct"], 0.1)

        # renormalize again
        total2 = sum(w["allocation_pct"] for w in raw)

        for w in raw:
            w["allocation_pct"] = round(w["allocation_pct"] / total2, 4)

        return raw