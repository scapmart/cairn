import requests


class OKXClient:

    def __init__(self):
        self.base = "https://www.okx.com"

    def get(self, endpoint, params=None):

        r = requests.get(
            self.base + endpoint,
            params=params,
            timeout=20
        )

        r.raise_for_status()

        return r.json()