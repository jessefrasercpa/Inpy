from abc import ABC, abstractmethod
from typing import List, Any


class Repo(ABC):


    @abstractmethod
    def ls(self) -> List[Any]:

        pass


    @abstractmethod
    def add(self, obj: Any):

        pass


    @abstractmethod
    def get(self, objID: str):

        pass


    @abstractmethod
    def delete(self, objID: str):

        pass
