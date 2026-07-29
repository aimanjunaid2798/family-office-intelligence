from abc import ABC, abstractmethod

from app.discovery.candidate import Candidate


class BaseSource(ABC):

    @abstractmethod
    def discover(self) -> list[Candidate]:
        pass