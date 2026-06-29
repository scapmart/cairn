import os
import requests
from urllib.parse import urlencode

from cairn.brokers.bitget.endpoints import BASE_URL
from cairn.brokers.bitget.auth import BitgetAuth


class BitgetClient:
    def __init__(self):
        self.base_url = BASE_URL

        self.auth = BitgetAuth(
            api_key=os.getenv("BITGET_API_KEY", ""),
            api_secret=os.getenv("BITGET_API_SECRET", ""),
            passphrase=os.getenv("BITGET_API_PASSPHRASE", ""),
        )

    def get(self, endpoint, params=None, auth=False):
        params = params or {}

        query = urlencode(params)
        request_path = endpoint + (f"?{query}" if query else "")
        url = self.base_url + request_path

        headers = None
        if auth:
            headers = self.auth.headers(
                method="GET",
                request_path=request_path,
            )

        response = requests.get(
            url,
            headers=headers,
            timeout=20,
        )

        return {
            "status_code": response.status_code,
            "url": response.url,
            "text": response.text,
            "json": self._safe_json(response),
        }

    def _safe_json(self, response):
        try:
            return response.json()
        except Exception:
            return None