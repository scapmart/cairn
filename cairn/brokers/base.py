from abc import ABC, abstractmethod


class BaseBrokerAdapter(ABC):

    @abstractmethod
    def fetch(self):
        """Fetch raw data from broker API"""
        pass

    @abstractmethod
    def normalize(self, raw):
        """Convert raw broker data → Trader objects"""
        pass

    def load(self):
        raw = self.fetch()
        return self.normalize(raw)