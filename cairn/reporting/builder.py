from datetime import datetime


class ReportBuilder:

    def build(self, portfolio):

        lines = []
        lines.append("# CAIRN REPORT")
        lines.append(f"Date: {datetime.utcnow()}\n")

        lines.append("## Portfolio Summary")
        lines.append(f"Total value: {portfolio.total_value:.2f}")
        lines.append(f"Total PnL: {portfolio.total_pnl_abs:.2f} ({portfolio.total_pnl_pct:.2f}%)\n")

        lines.append("## Positions")

        for p in portfolio.positions:
            lines.append(
                f"- {p.asset.symbol}: size={p.size}, "
                f"entry={p.entry_price}, current={p.current_price}, "
                f"PnL={p.pnl_pct:.2f}%"
            )

        return "\n".join(lines)