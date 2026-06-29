import json

from cairn.brokers.bitget.client import BitgetClient
from cairn.brokers.bitget.endpoints import (
    V1_TRACE_TRADER_LIST,
    V2_MIX_BROKER_TRADERS,
    V2_MIX_FOLLOWER_TRADERS,
)


class BitgetDiscovery:

    def __init__(self):
        self.client = BitgetClient()

    def test_endpoint(self, name, endpoint, params=None):
        print(f"\n===== {name} =====")

        result = self.client.get(endpoint, params=params, auth=True)

        print("URL:", result["url"])
        print("STATUS:", result["status_code"])

        data = result["json"]

        if data is not None:
            print(json.dumps(data, indent=2, ensure_ascii=False)[:4000])
        else:
            print(result["text"][:4000])

    def discover(self):
        self.test_endpoint(
            "V1 trace traderList",
            V1_TRACE_TRADER_LIST,
            params={"pageNo": 1, "pageSize": 20},
        )

        self.test_endpoint(
            "V2 mix-broker query-traders",
            V2_MIX_BROKER_TRADERS,
            params={"pageNo": 1, "pageSize": 20},
        )

        self.test_endpoint(
            "V2 mix-follower query-traders",
            V2_MIX_FOLLOWER_TRADERS,
            params={},
        )