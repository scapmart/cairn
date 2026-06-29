import json
from typing import List
from .models import Trader, Trade


class BitgetAdapter:

    def from_json(self, path: str) -> List[Trader]:
        with open(path, "r") as f:
            raw = json.load(f)

        traders = []

        for t in raw:
            trades = [
                Trade(
                    pnl_pct=trade["pnl_pct"],
                    duration_hours=trade["duration"],
                    leverage=trade["leverage"],
                    is_win=trade["pnl_pct"] > 0,
                )
                for trade in t["trades"]
            ]

            traders.append(Trader(id=t["id"], trades=trades))

        return traders

    def from_api(self, api_client):
        """
        Future: Bitget API connector
        """
        return api_client.get_traders()