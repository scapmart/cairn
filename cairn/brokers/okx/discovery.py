import json
from typing import Any, Dict, List, Optional

from cairn.brokers.okx.client import OKXClient
from cairn.brokers.okx.endpoints import COPY_LEAD_TRADERS


class OKXDiscovery:
    def __init__(self):
        self.client = OKXClient()

    def fetch_lead_traders_raw(self, limit: int = 20) -> Dict[str, Any]:
        safe_limit = min(limit, 20)

        return self.client.get(
            COPY_LEAD_TRADERS,
            params={"limit": safe_limit},
        )

    def extract_ranks(self, raw: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = raw.get("data", [])

        if not data:
            return []

        first_block = data[0]

        if isinstance(first_block, dict):
            return first_block.get("ranks", [])

        return []

    def inspect_keys(self, traders: List[Dict[str, Any]]) -> List[str]:
        keys = set()

        for trader in traders:
            keys.update(trader.keys())

        return sorted(keys)

    def inspect_sample(self, traders: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not traders:
            return None

        return traders[0]

    def summarize_trader(self, trader: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "uniqueCode": trader.get("uniqueCode"),
            "nickName": trader.get("nickName"),
            "aum": trader.get("aum"),
            "copyTraderNum": trader.get("copyTraderNum"),
            "accCopyTraderNum": trader.get("accCopyTraderNum"),
            "leadDays": trader.get("leadDays"),
            "winRatio": trader.get("winRatio"),
            "pnlRatio": trader.get("pnlRatio"),
            "pnl": trader.get("pnl"),
            "pnlRatios_count": len(trader.get("pnlRatios", [])),
            "instruments_count": len(trader.get("traderInsts", [])),
            "instruments_sample": trader.get("traderInsts", [])[:10],
        }

    def discover_top_traders(self, limit: int = 20) -> Dict[str, Any]:
        raw = self.fetch_lead_traders_raw(limit=limit)
        traders = self.extract_ranks(raw)

        return {
            "raw_code": raw.get("code"),
            "raw_msg": raw.get("msg"),
            "trader_count": len(traders),
            "keys": self.inspect_keys(traders),
            "sample_summary": self.summarize_trader(traders[0]) if traders else None,
            "sample_raw": self.inspect_sample(traders),
        }

    def print_discovery(self, limit: int = 20, show_raw_sample: bool = False) -> None:
        result = self.discover_top_traders(limit=limit)

        print("\n========== OKX DISCOVERY ==========\n")
        print("API code:", result["raw_code"])
        print("API msg:", result["raw_msg"])
        print("Trader count:", result["trader_count"])

        print("\n--- Fields discovered ---")
        for key in result["keys"]:
            print("-", key)

        print("\n--- Sample summary ---")
        print(json.dumps(result["sample_summary"], indent=2, ensure_ascii=False))

        if show_raw_sample:
            print("\n--- Raw sample ---")
            print(json.dumps(result["sample_raw"], indent=2, ensure_ascii=False))

        print("\n===================================\n")
    
    def test_pagination(self):
        tests = [
            {"limit": 20},
            {"limit": 20, "page": 1},
            {"limit": 20, "page": 2},
            {"limit": 20, "offset": 20},
            {"limit": 20, "after": 20},
        ]

        for params in tests:
            print("\nPARAMS:", params)

            raw = self.client.get(
                COPY_LEAD_TRADERS,
                params=params,
            )

            print("code:", raw.get("code"))
            data = raw.get("data", [])
            ranks = data[0].get("ranks", []) if data else []

            print("count:", len(ranks))

            if ranks:
                print("first:", ranks[0].get("nickName"), ranks[0].get("uniqueCode"))


    def fetch_top_traders(self, limit=100):
        per_page = 20
        pages = (limit + per_page - 1) // per_page

        all_traders = []
        seen = set()

        for page in range(1, pages + 1):
            raw = self._request(
                COPY_LEAD_TRADERS,
                {
                    "limit": per_page,
                    "page": page,
                }
            )

            if not raw:
                continue

            ranks = raw[0].get("ranks", [])

            for trader in ranks:
                uid = trader.get("uniqueCode")

                if uid and uid not in seen:
                    seen.add(uid)
                    all_traders.append(trader)

                if len(all_traders) >= limit:
                    break

            if len(all_traders) >= limit:
                break

        return self.parser.parse(all_traders)