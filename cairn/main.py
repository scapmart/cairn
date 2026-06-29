from cairn.brokers.factory import BrokerFactory
from cairn.scoring.scorer import TraderScorer
from cairn.scoring.ranking import TraderRanking
from cairn.decision.tagging import DecisionTagger


def main():
    broker = "bitget"

    adapter = BrokerFactory.create("bitget")
    traders = adapter.fetch_top_traders(1000)

    print(f"RAW TRADERS: {len(traders)}")

    scorer = TraderScorer()
    ranking = TraderRanking(scorer)

    results = ranking.rank(traders)

    print(f"\n===== CAIRN {broker.upper()} TOP 20 =====\n")

    for i, r in enumerate(results[:20], start=1):
        m = r["metrics"]

        print(f"#{i}")
        print("ID:", r["trader_id"])
        print("Score:", r["score"])
        print("Risk:", r["risk"])
        print("Confidence:", r["confidence"])
        print("Winrate:", round(m["winrate"], 4))
        print("PnL ratio:", round(m["avg_pnl"], 4))
        print("Sharpe:", round(m["sharpe"], 4))
        print("Volatility:", round(m["volatility"], 4))
        print("Consistency:", round(m["consistency"], 4))
        print("Biases:", r["biases"])
        print("-" * 40)
        print("Decision :", DecisionTagger.tag(r))
    
    watchlist = []

    for r in results:
        decision = DecisionTagger.tag(r)

        if decision in ["STRONG_WATCH", "WATCH", "LOW_CONFIDENCE"]:
            watchlist.append({
                "id": r["trader_id"],
                "decision": decision,
                "score": r["score"],
                "risk": r["risk"],
                "confidence": r["confidence"],
                "winrate": r["metrics"]["winrate"],
                "pnl_ratio": r["metrics"]["avg_pnl"],
                "sharpe": r["metrics"]["sharpe"],
                "volatility": r["metrics"]["volatility"],
                "consistency": r["metrics"]["consistency"],
            })

    print("\n===== CAIRN WATCHLIST =====\n")

    for w in watchlist[:10]:
        print(w)


if __name__ == "__main__":
    main()