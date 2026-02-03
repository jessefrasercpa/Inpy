from dataclasses import dataclass


@dataclass(frozen=True)
class InvoiceLine:
    """
    Encapsulates a generic invoice line item which has
    a name, a description of the rate applied,
    the quantity of time rented, and the rental cost subtotal.

    Attributes
    ----------
    name : str
        A Human-readable identifier.

    rate : str
        A description of the rate applied.

    quantity : float
        The quantity of time rented.

    subtotal : float
        The rental cost subtotal.
    """


    name: str
    rate: str
    quantity: float
    subtotal: float
