from collections import defaultdict
from ..domain.portfolio import Portfolio


class MetricsEngine:

    def compute_allocation(self, portfolio: Portfolio):
        allocation = defaultdict(float)

        for p in portfolio.positions:
            value = p.size * p.current_price
            allocation[p.asset.symbol] += value

        total = sum(allocation.values())

        return {
            k: v / total for k, v in allocation.items()
        }

    def rank_positions(self, portfolio: Portfolio):
        return sorted(
            portfolio.positions,
            key=lambda p: p.pnl_pct,
            reverse=True
        )

    def worst_position(self, portfolio: Portfolio):
        return min(portfolio.positions, key=lambda p: p.pnl_pct)

    def best_position(self, portfolio: Portfolio):
        return max(portfolio.positions, key=lambda p: p.pnl_pct)

    def portfolio_risk_hint(self, portfolio: Portfolio):
        losses = [p.pnl_pct for p in portfolio.positions if p.pnl_pct < 0]

        if not losses:
            return 0

        return abs(sum(losses) / len(losses))
    def activity_score(self, trader):
        trade_count = getattr(trader, "trade_count", None)

        if trade_count is None:
            return 0.7

        if trade_count < 20:
            return 0.1

        if trade_count < 50:
            return 0.35

        if trade_count < 100:
            return 0.65

        if trade_count < 500:
            return 1.0

        if trade_count < 1500:
            return 0.85

        return 0.6