from .models import Trader, Trade


class TraderParser:

    def clean_trader(self, trader: Trader):

        cleaned_trades = []

        for t in trader.trades:

            # filtre données invalides
            if t.duration_hours <= 0:
                continue

            if abs(t.leverage) > 200:
                continue

            cleaned_trades.append(t)

        trader.trades = cleaned_trades
        return trader

    def validate(self, trader: Trader):
        return len(trader.trades) >= 2