import csv
from datetime import datetime

from ..domain.asset import Asset
from ..domain.position import Position
from ..domain.portfolio import Portfolio


class CSVAdapter:

    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_portfolio(self) -> Portfolio:
        positions = []

        with open(self.filepath, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                asset = Asset(
                    symbol=row["symbol"],
                    name=row["symbol"],
                    asset_type="crypto"
                )

                size = float(row["size"])
                entry = float(row["entry_price"])
                current = float(row["current_price"])

                pnl_abs = (current - entry) * size
                pnl_pct = (current - entry) / entry * 100

                position = Position(
                    id=f"{row['symbol']}_{datetime.utcnow().timestamp()}",
                    asset=asset,
                    size=size,
                    entry_price=entry,
                    current_price=current,
                    pnl_abs=pnl_abs,
                    pnl_pct=pnl_pct,
                    source=row.get("source", "csv"),
                    opened_at=str(datetime.utcnow()),
                    updated_at=str(datetime.utcnow())
                )

                positions.append(position)

        total_value = sum(p.size * p.current_price for p in positions)
        total_pnl = sum(p.pnl_abs for p in positions)

        exposure = {}
        for p in positions:
            exposure[p.asset.symbol] = exposure.get(p.asset.symbol, 0) + (p.size * p.current_price)

        return Portfolio(
            id="csv_portfolio",
            positions=positions,
            total_value=total_value,
            total_pnl_abs=total_pnl,
            total_pnl_pct=(total_pnl / total_value) * 100 if total_value else 0,
            exposure=exposure,
            updated_at=str(datetime.utcnow())
        )