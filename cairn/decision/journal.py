import json
from datetime import datetime
from pathlib import Path


class DecisionJournal:

    def __init__(self, path="data/decision_journal.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.path.write_text("[]")

    def load(self):
        return json.loads(self.path.read_text())

    def save(self, entries):
        self.path.write_text(json.dumps(entries, indent=2))

    def record(self, portfolio_snapshot, recommendation, decision="pending"):

        entries = self.load()

        entries.append({
            "timestamp": datetime.utcnow().isoformat(),
            "portfolio_snapshot": self._serialize_portfolio(portfolio_snapshot),
            "recommendation": recommendation,
            "decision": decision,
            "outcome": None
        })

        self.save(entries)

    def update_outcome(self, index, outcome):

        entries = self.load()

        if 0 <= index < len(entries):
            entries[index]["outcome"] = outcome

        self.save(entries)

    def _serialize_portfolio(self, portfolio):

        return {
            "total_value": portfolio.total_value,
            "total_pnl": portfolio.total_pnl_abs,
            "positions": [
                {
                    "symbol": p.asset.symbol,
                    "size": p.size,
                    "pnl_pct": p.pnl_pct
                }
                for p in portfolio.positions
            ]
        }