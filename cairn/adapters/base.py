from abc import ABC, abstractmethod
from ..domain.portfolio import Portfolio


class ExchangeAdapter(ABC):

    @abstractmethod
    def get_portfolio(self) -> Portfolio:
        pass