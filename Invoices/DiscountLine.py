from dataclasses import dataclass


@dataclass(frozen=True)
class DiscountLine:
    """
    Encapsulates a generic discount line item which has
    a name and the discounted amount.

    Attributes
    ----------
    name : str
        A Human-readable identifier.

    amount : float
        The discounted amount.
    """


    name: str
    amount: float
