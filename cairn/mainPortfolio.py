from cairn.adapters.csv_adapter import CSVAdapter
from cairn.reporting.builder import ReportBuilder
from cairn.engine.metrics import MetricsEngine
from cairn.engine.recommendation_engine import RecommendationEngine


def main():

    # LOAD DATA
    adapter = CSVAdapter("data/raw/portfolio.csv")
    portfolio = adapter.get_portfolio()

    # METRICS
    metrics_engine = MetricsEngine()

    allocation = metrics_engine.compute_allocation(portfolio)
    best = metrics_engine.best_position(portfolio)
    worst = metrics_engine.worst_position(portfolio)
    risk_hint = metrics_engine.portfolio_risk_hint(portfolio)

    metrics = {
        "allocation": allocation,
        "best": best,
        "worst": worst,
        "risk_hint": risk_hint
    }

    # BASE REPORT
    builder = ReportBuilder()
    report = builder.build(portfolio)

    # ENGINE
    engine = RecommendationEngine()
    recommendations = engine.generate(portfolio, metrics)

    # METRICS SECTION
    report += "\n\n## METRICS\n"
    report += f"Allocation: {allocation}\n"
    report += f"Best: {best.asset.symbol} ({best.pnl_pct:.2f}%)\n"
    report += f"Worst: {worst.asset.symbol} ({worst.pnl_pct:.2f}%)\n"
    report += f"Risk hint: {risk_hint:.2f}\n"

    # SINGLE RECOMMENDATION SECTION (IMPORTANT FIX)
    report += "\n\n## RECOMMANDATIONS\n"

    for r in recommendations:
        report += f"- [{r['severity']}] {r['title']}\n"
        report += f"  → {r['action']}\n"
        report += f"  confidence: {r['confidence']:.2f}\n"

        if r.get("biases"):
            report += f"  biases: {', '.join(r['biases'])}\n"

        if r.get("why_wrong"):
            report += "  why it might be wrong:\n"
            for w in r["why_wrong"]:
                report += f"    - {w}\n"

        report += "\n"

    print(report)

    with open("reports/weekly_report.md", "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()