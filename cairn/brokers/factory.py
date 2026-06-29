from cairn.brokers.okx.adapter import OKXAdapter
from cairn.brokers.bitget.adapter import BitgetAdapter


class BrokerFactory:

    @staticmethod
    def create(name):

        if name.lower() == "okx":
            return OKXAdapter()

        if name.lower() == "bitget":
            return BitgetAdapter()

        raise ValueError(name)