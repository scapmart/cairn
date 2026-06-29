from cairn.core.models import Trader


class BitgetParser:

    def parse(self, traders_raw):
        traders = []

        for t in traders_raw:
            ordered = sorted(
                t.get("dailyProfitRateList", []),
                key=lambda x: int(x.get("cTime", 0))
            )

            equity_curve = []
            for x in ordered:
                rate = float(x.get("rate", 0))
                equity_curve.append(100 * (1 + rate / 100))

            trader = Trader(
                id=f'{t.get("traderName", "unknown")}_{t.get("traderId", "unknown")}',
                trades=[],
                equity_curve=equity_curve,
            )

            trader.broker = "bitget"
            trader.nickname = t.get("traderName", "unknown")
            trader.unique_code = t.get("traderId")
            trader.winrate = self._to_float(t.get("averageWinRate", 0)) / 100
            trader.pnl_ratio = self._extract_column(t, "ROI") / 100
            roi = self._extract_column(t, "ROI")

            if roi == 0:
                roi = self._to_float(t.get("roi", 0))

            trader.pnl_ratio = roi / 100
            if trader.pnl_ratio > 20 or trader.pnl_ratio < -5:
                print("PNL_RATIO_DEBUG", trader.id, t.get("columnList"))
            trader.pnl = self._extract_money_column(t, "Total PnL")

            trader.followers = int(self._to_float(t.get("followCount", 0)))
            trader.total_followers = int(self._to_float(t.get("totalFollowers", 0)))
            trader.aum = self._extract_money_column(t, "AUM")
            trader.lead_days = None

            trader.instruments = t.get("currentTradingList", [])
            trader.trade_count = int(self._to_float(t.get("tradeCount", 0)))
            trader.profit_count = int(self._to_float(t.get("profitCount", 0)))
            trader.loss_count = int(self._to_float(t.get("lossCount", 0)))
            trader.max_drawdown_raw = self._to_float(t.get("maxCallbackRate", 0))

            traders.append(trader)

        return traders

    def _extract_column(self, trader, name):
        for item in trader.get("columnList", []):
            if item.get("describe") == name:
                return self._to_float(item.get("value", 0))
        return 0

    def _extract_money_column(self, trader, name):
        for item in trader.get("columnList", []):
            if item.get("describe") == name:
                return self._to_float(item.get("value", 0))
        return 0

    def _to_float(self, value):
        if value is None:
            return 0.0

        value = str(value)
        value = value.replace("$", "")
        value = value.replace(",", "")
        value = value.replace("%", "")
        value = value.strip()

        try:
            return float(value)
        except ValueError:
            return 0.0