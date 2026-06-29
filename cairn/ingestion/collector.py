from ..adapters.base import ExchangeAdapter


class Collector:

    def __init__(self, adapter: ExchangeAdapter):
        self.adapter = adapter

    def collect_portfolio(self):
        return self.adapter.get_portfolio()