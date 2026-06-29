from .models import Trader


class TraderMetrics:

    def winrate(self, trader: Trader):
        if not trader.trades:
            return 0
        return sum(t.is_win for t in trader.trades) / len(trader.trades)

    def avg_pnl(self, trader: Trader):
        if not trader.trades:
            return 0
        return sum(t.pnl_pct for t in trader.trades) / len(trader.trades)

    def max_drawdown(self, trader: Trader):
        return min((t.pnl_pct for t in trader.trades), default=0)

    def leverage_risk(self, trader: Trader):
        if not trader.trades:
            return 0
        return sum(t.leverage for t in trader.trades) / len(trader.trades)

    def consistency(self, trader: Trader):
        pnls = [t.pnl_pct for t in trader.trades]
        if len(pnls) < 2:
            return 0
        spread = max(pnls) - min(pnls)
        return max(0.0, 1.0 - spread / 25)