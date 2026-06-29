import requests
from typing import List

from cairn.core.models import Trader, Trade


class BitgetLiveAdapter:

    BASE_URL = "https://api.bitget.com"

    # -------------------------
    # PUBLIC ENDPOINT (simplifié)
    # -------------------------
    def fetch_top_traders(self, limit: int = 10) -> List[Trader]:

        url = f"{self.BASE_URL}/api/spot/v1/public/rank-trader"

        try:
            res = requests.get(url, timeout=10)
            data = res.json()
            print(res.status_code)
            print(res.text)

        except Exception as e:
            print("[BITGET ERROR]", e)
            return []
        400
{"code":"30032","msg":"The V1 API has been decommissioned. Please migrate to a newer version.","requestTime":1782735209842,"data":null}

        traders_raw = data.get("data", [])[:limit]

        return [self._normalize(t) for t in traders_raw]


    # -------------------------
    # NORMALISATION
    # -------------------------
    def _normalize(self, t: dict) -> Trader:

        # Bitget data is inconsistent → safe parsing
        trader_id = t.get("traderId") or t.get("userId") or "unknown"

        pnl = float(t.get("pnlRatio", 0)) * 100
        winrate = float(t.get("winRate", 0))

        leverage = float(t.get("leverage", 1))
        trades_count = int(t.get("orderCount", 1))

        # Fake reconstruction of trades (IMPORTANT)
        trades = self._build_synthetic_trades(
            pnl=pnl,
            winrate=winrate,
            leverage=leverage,
            trades_count=trades_count
        )

        return Trader(
            id=trader_id,
            trades=trades
        )


    # -------------------------
    # FALLBACK ENGINE
    # -------------------------
    def _build_synthetic_trades(self, pnl, winrate, leverage, trades_count):

        trades = []

        wins = int(trades_count * winrate)
        losses = trades_count - wins

        # wins
        for _ in range(wins):
            trades.append(
                Trade(
                    pnl_pct=pnl / max(trades_count, 1),
                    duration_hours=12,
                    leverage=leverage,
                    is_win=True
                )
            )

        # losses
        for _ in range(losses):
            trades.append(
                Trade(
                    pnl_pct=-abs(pnl / max(trades_count, 1)),
                    duration_hours=6,
                    leverage=leverage,
                    is_win=False
                )
            )

        return trades