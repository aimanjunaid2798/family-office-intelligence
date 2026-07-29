from abc import ABC, abstractmethod
from typing import List


class BaseSearchProvider(ABC):

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def search(self, query: str) -> List[str]:
        """
        Returns a list of candidate URLs.
        """
        pass