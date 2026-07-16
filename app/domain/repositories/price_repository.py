from abc import ABC
from abc import abstractmethod

import pandas as pd


class PriceRepository(ABC):

    @abstractmethod
    def get_history(self, ticker: str) -> pd.DataFrame:
        """Return historical market data."""
        pass