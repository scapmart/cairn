from cairn.core.models import Trader


class OKXParser:

    def parse(self, traders_raw):
        traders = []

        for t in traders_raw:
            pnl_ratios = t.get("pnlRatios", [])

            # OKX donne souvent du plus récent au plus ancien.
            # On remet dans l'ordre chronologique.
            ordered = sorted(
                pnl_ratios,
                key=lambda x: int(x.get("beginTs", 0))
            )

            # pnlRatio = rendement cumulé.
            # On le transforme en equity index.
            equity_curve = []
            for x in ordered:
                ratio = float(x.get("pnlRatio", 0))
                equity = 100 * (1 + ratio)
                equity_curve.append(equity)

            trader = Trader(
                id=f'{t.get("nickName", "unknown")}_{t.get("uniqueCode", "unknown")}',
                trades=[],
                equity_curve=equity_curve,
            )

            trader.broker = "okx"
            trader.nickname = t.get("nickName", "unknown")
            trader.unique_code = t.get("uniqueCode")

            trader.winrate = float(t.get("winRatio", 0))
            trader.pnl_ratio = float(t.get("pnlRatio", 0))
            trader.pnl = float(t.get("pnl", 0))

            trader.followers = int(t.get("copyTraderNum", 0))
            trader.total_followers = int(t.get("accCopyTraderNum", 0))
            trader.aum = float(t.get("aum", 0))
            trader.lead_days = int(t.get("leadDays", 0))
            trader.instruments = t.get("traderInsts", [])

            traders.append(trader)

        return traders