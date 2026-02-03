from dataclasses import dataclass
from typing import Callable


RateFunc = Callable[[float], float]


@dataclass(frozen=True)
class Rate:
    """
    Encapsulates a generic rate entity which has a name and a pricing function.

    Attributes
    ----------
    name : str
        A Human-readable identifier.

    rateFunc : Callable[[float], float]
        A function that computes the rental cost over a given duration of time.

    Methods
    -------
    calculate(t: float) -> float
        Computes the rental cost over a given duration of time.
    """


    name: str
    rateFunc: RateFunc


    def calculate(self, t: float) -> float:
        """
        Computes the rental cost over a given duration of time.

        Parameters
        ----------
        t : float
            The duration of time for which the entity is rented.

        Returns
        -------
        float
            The rental cost.
        """

        return self.rateFunc(t)
