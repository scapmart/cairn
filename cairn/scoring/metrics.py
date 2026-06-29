class TraderMetrics:

    def winrate(self, trader):
        if hasattr(trader, "winrate"):
            return trader.winrate

        if not trader.trades:
            return 0

        return sum(t.is_win for t in trader.trades) / len(trader.trades)

    def avg_pnl(self, trader):
        if hasattr(trader, "pnl_ratio"):
            return trader.pnl_ratio

        if not trader.trades:
            return 0

        return sum(t.pnl_pct for t in trader.trades) / len(trader.trades)

    def max_drawdown(self, trader):
        if trader.equity_curve:
            return min(trader.equity_curve)

        if not trader.trades:
            return 0

        return min(t.pnl_pct for t in trader.trades)

    def leverage_risk(self, trader):
        if not trader.trades:
            return 5

        return sum(t.leverage for t in trader.trades) / len(trader.trades)

    def consistency(self, trader):
        curve = getattr(trader, "equity_curve", None)

        if curve and len(curve) >= 3:
            returns = []

            for i in range(1, len(curve)):
                prev = curve[i - 1]
                curr = curve[i]

                if prev <= 0:
                    continue

                returns.append((curr - prev) / prev)

            if not returns:
                return 0

            mean = sum(returns) / len(returns)
            variance = sum((r - mean) ** 2 for r in returns) / len(returns)
            volatility = variance ** 0.5

            # 0.20 = seuil très volatile pour une série périodique OKX
            consistency = 1 - min(volatility / 0.20, 1)

            return max(0.0, min(consistency, 1.0))

        if not trader.trades:
            return 0

        pnls = [t.pnl_pct for t in trader.trades]
        spread = max(pnls) - min(pnls)

        return max(0.0, min(1.0, 1 - spread / 25))
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