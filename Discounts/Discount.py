from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable
from Invoiceables import Invoiceable


RateFunc = Callable[[float], float]


@dataclass(frozen=True)
class Discount(ABC):
    """
    Encapsulates a generic discount entity which has a name and a pricing function.

    Attributes
    ----------
    name : str
        A Human-readable identifier.

    rateFunc : Callable[[float], float]
        A function that computes the discounted rental cost over a given duration of time.

    Methods
    -------
    applies(invoiceable: Invoiceable) -> bool
        Checks whether this discount applies to a given invoiceable entity.
    """


    name: str
    rateFunc: RateFunc


    @abstractmethod
    def applies(self, invoiceable: Invoiceable) -> bool:
        """
        Checks whether this discount applies to a given invoiceable entity.

        Parameters
        ----------
        invoiceable : Invoiceable
            The invoice to check.

        Returns
        -------
        bool
            True if this discount applies, False otherwise.
        """

        pass
