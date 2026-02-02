from dataclasses import dataclass
from typing import Callable


RateFunc = Callable[[float], float]


@dataclass(frozen=True)
class Rentable:


    name: str
    rateFunc: RateFunc


    def rate(self, t: float) -> float:

        return self.rateFunc(t)
