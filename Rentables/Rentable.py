from dataclasses import dataclass
from .utils import Rate


@dataclass(frozen=True)
class Rentable:
    """
    Encapsulates a generic rentable entity which has a name and a pricing function.

    Attributes
    ----------
    id : str
        A unique identifier.
        
    name : str
        A Human-readable identifier.

    rate : Rate
        A Rate object which is used to calculate the subtotal of this rentable.

    Methods
    -------
    subtotal(t: float) -> float
        Computes the subtotal of this rentable.
    """


    id: str
    name: str
    rate: Rate


    def subtotal(self, t: float) -> float:
        """
        Computes the subtotal of this rentable.

        Parameters
        ----------
        t : float
            The duration of time for which the entity is rented.

        Returns
        -------
        float
            The subtotal.
        """

        return self.rate.calculate(t)
