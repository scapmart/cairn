from .client import OKXClient
from .parser import OKXParser
from .endpoints import COPY_LEAD_TRADERS


class OKXAdapter:

    def __init__(self):
        self.client = OKXClient()
        self.parser = OKXParser()

    def fetch_top_traders(self, limit=100):
        per_page = 20
        pages = (limit + per_page - 1) // per_page

        all_traders = []
        seen = set()

        for page in range(1, pages + 1):
            raw = self.client.get(
                COPY_LEAD_TRADERS,
                params={
                    "limit": per_page,
                    "page": page,
                }
            )

            if raw.get("code") != "0":
                raise RuntimeError(
                    f'OKX API Error {raw.get("code")} : {raw.get("msg")}'
                )

            data = raw.get("data", [])

            if not data:
                continue

            ranks = data[0].get("ranks", [])

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