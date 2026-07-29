from abc import ABC, abstractmethod
from typing import List

from app.models.family_office import FamilyOffice


class BaseDiscoverySource(ABC):
    """
    Base interface for all discovery sources.
    Every discovery source must inherit from this class.
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Human-readable name of the discovery source."""
        pass

    @abstractmethod
    def discover(self) -> List[FamilyOffice]:
        """
        Discover potential Family Offices.

        Returns:
            List[FamilyOffice]
        """
        pass