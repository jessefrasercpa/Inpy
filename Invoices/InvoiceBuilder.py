from datetime import date
from typing import List
from Invoiceables import Invoiceable
from Discounts import Discount
from .PricingEngine import PricingEngine
from .Invoice import Invoice


class InvoiceBuilder:
    """
    Constructs Invoice objects from an Invoiceable entity
    together with a PricingEngine entity.
    """

    def __init__(self, pricingEngine: PricingEngine):

        self._pricingEngine = pricingEngine


    def build(
            self,
            invoiceNum: int,
            payee: str,
            dateCreated: date,
            dateDue: date,
            invoiceable: Invoiceable,
            discounts: List[Discount]
    ) -> Invoice:
        """
        Builds an Invoice object from the given Invoiceable entity and discounts.

        Parameters
        ----------
        invoiceNum : int
            The invoice number.

        payee : str
            A person to whom the generated invoice is payable to.

        dateCreated : date
            The date on which the generated invoice was created.

        dateDue : date
            The date on which the generated invoice is due.

        invoiceable : Invoiceable
            An invoiceable entity from which the invoice is to be generated.

        discounts : List[Discount]
            A list of discounts.

        Returns
        -------
        Invoice
            The generated invoice object.

        Raises
        ------
        ValueError
            If the Invoiceable entity fails approval (i.e., unsupported add-ons).
        """
        
        invoiceable.approve()

        invoiceLines  = self._pricingEngine.getInvoiceLines(invoiceable)
        subtotal      = self._pricingEngine.calculateSubtotal(invoiceLines)
        discountLines = self._pricingEngine.getDiscountLines(invoiceable, subtotal, discounts)
        total         = self._pricingEngine.calculateTotal(subtotal, discountLines)

        return Invoice(
            invoiceNum=invoiceNum,
            payee=payee,
            dateCreated=dateCreated,
            dateDue=dateDue,
            invoiceItems=invoiceLines,
            discountItems=discountLines,
            subtotal=subtotal,
            total=total
        )
