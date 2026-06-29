from cairn.brokers.bitget.client import BitgetClient
from cairn.brokers.bitget.parser import BitgetParser
from cairn.brokers.bitget.endpoints import V2_MIX_BROKER_TRADERS


class BitgetAdapter:

    def __init__(self):
        self.client = BitgetClient()
        self.parser = BitgetParser()

    def fetch_top_traders(self, limit=100):
        per_page = 20
        pages = (limit + per_page - 1) // per_page

        all_traders = []
        seen = set()

        for page in range(1, pages + 1):
            result = self.client.get(
                V2_MIX_BROKER_TRADERS,
                params={
                    "pageNo": page,
                    "pageSize": per_page,
                },
                auth=True,
            )

            data = result["json"]

            if data.get("code") != "00000":
                raise RuntimeError(
                    f'Bitget API Error {data.get("code")} : {data.get("msg")}'
                )

            traders = data.get("data", [])

            for trader in traders:
                uid = trader.get("traderId")

                if uid and uid not in seen:
                    seen.add(uid)
                    all_traders.append(trader)

                if len(all_traders) >= limit:
                    break

            if len(all_traders) >= limit:
                break

        return self.parser.parse(all_traders)