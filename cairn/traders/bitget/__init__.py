from .adapter import BitgetAdapter
from .ranking import TraderRanking


def run_bitget_analysis():

    adapter = BitgetAdapter()
    traders = adapter.fetch_traders()

    engine = TraderRanking()
    ranking = engine.rank(traders)

    for r in ranking:
        print("\n--- TRADER ---")
        print("ID:", r["trader_id"])
        print("Score:", r["score"])
        print("Confidence:", r["confidence"])
        print("Metrics:", r["metrics"])
        print("Biases:", r["biases"])
        print("Risks:", r["why_it_might_be_wrong"])

    return ranking