class EquityCurveBuilder:

    def build(self, trader, initial_capital=100.0):
        if trader.equity_curve:
            return trader.equity_curve

        curve = [initial_capital]
        capital = initial_capital

        for trade in trader.trades:
            capital *= 1 + trade.pnl_pct / 100
            curve.append(capital)

        return curve