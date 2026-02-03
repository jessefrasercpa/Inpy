from dataclasses import dataclass
from typing import List
from datetime import date
from .InvoiceLine import InvoiceLine
from .DiscountLine import DiscountLine


@dataclass(frozen=True)
class Invoice:
    """
    Encapsulates a generic invoice entity which has
    an invoice number, a person to whom this invoice is payable,
    the date on which this invoice was created,
    the date on which this invoice is due,
    a list of invoice line items, a list of discount line items,
    the final subtotal of all the invoice line items,
    and the invoice total.

    Attributes
    ----------
    invoiceNum : int
        An invoice number.

    payee : str
        A person to whom this invoice is payable to.

    dateCreated : date
        The date on which this invoice was created.

    dateDue : date
        The date on which this invoice is due.

    invoiceItems : List[InvoiceLine]
        A list of invoice line items.

    discountItems : List[DiscountLine]
        A list of discount line items.

    subtotal : float
        The final subtotal of all the invoice line items.

    total : float
        The invoice total.
    """


    invoiceNum: int
    payee: str
    dateCreated: date
    dateDue: date
    invoiceItems: List[InvoiceLine]
    discountItems: List[DiscountLine]
    subtotal: float
    total: float
