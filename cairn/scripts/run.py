from cairn.adapters.csv_adapter import CSVAdapter
from cairn.ingestion.collector import Collector
from cairn.engine.metrics import MetricsEngine


def main():

    adapter = CSVAdapter("data/raw/portfolio.csv")
    collector = Collector(adapter)

    portfolio = collector.collect_portfolio()

    engine = MetricsEngine()

    metrics = {
        "total_value": engine.compute_total_value(portfolio),
        "exposure": engine.compute_exposure(portfolio)
    }

    print(metrics)


if __name__ == "__main__":
    main()