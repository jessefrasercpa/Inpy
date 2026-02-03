from typing import List
from Invoiceables import Invoiceable
from Discounts import Discount
from .InvoiceLine import InvoiceLine
from .DiscountLine import DiscountLine


class PricingEngine:
    """
    Encapsulates the pricing logic for generating invoice line items,
    applying discounts, and computing totals from an Invoiceable object.
    """


    def getInvoiceLines(self, invoiceable: Invoiceable) -> List[InvoiceLine]:
        """
        Generates invoice line items for each room and add-on in the given Invoiceable entity.

        Parameters
        ----------
        invoiceable : Invoiceable
            The invoiceable entity containing the selected rooms, add-ons,
            and rental duration.

        Returns
        -------
        List[InvoiceLine]
            A list of the generated invoice line items.
        """

        invoiceLines: List[InvoiceLine] = []

        for room in invoiceable.rooms:

            subtotal = room.subtotal(invoiceable.t)

            invoiceLines.append(
                InvoiceLine(
                    name=room.name,
                    rate=room.rate.name,
                    quantity=invoiceable.t,
                    subtotal=subtotal
                )
            )

        for addOn in invoiceable.addOns:

            subtotal = addOn.subtotal(invoiceable.t)

            invoiceLines.append(
                InvoiceLine(
                    name=addOn.name,
                    rate=addOn.rate.name,
                    quantity=invoiceable.t,
                    subtotal=subtotal
                )
            )

        return invoiceLines


    def calculateSubtotal(self, invoiceLines: List[InvoiceLine]) -> float:
        """
        Computes the final, summed-subtotal of a given list of invoice line items.

        Parameters
        ----------
        invoiceLines : List[InvoiceLine]
            A list of invoice line items.

        Returns
        -------
        float
            The final, summed-subtotal of the given list of invoice line items.
        """

        return sum(invoiceLine.subtotal for invoiceLine in invoiceLines)


    def getDiscountLines(
            self,
            invoiceable: Invoiceable,
            subtotal: float,
            discounts: List[Discount]
    ) -> List[DiscountLine]:
        """
        Determines which discounts apply to the given Invoiceable entity
        and then generates corresponding discount line items.

        Parameters
        ----------
        invoiceable : Invoiceable
            The invoiceable entity on which the given discounts are applied.

        subtotal : float
            The subtotal from which the applicable discounted amounts will be subtracted.

        discounts : List[Discount]
            A list of discounts.

        Returns
        -------
        List[DiscountLine]
            A list of discount line items.
        """

        discountLines: List[DiscountLine] = []

        for discount in discounts:

            if discount.applies(invoiceable):

                amount = discount.rate(subtotal)
                
                discountLines.append(
                    DiscountLine(
                        name=discount.name,
                        amount=amount
                    )
                )

        return discountLines


    def calculateTotal(self, subtotal: float, discountLines: List[DiscountLine]) -> float:
        """
        Computes the final, summed-total of a given list of invoice line items
        less a given list of discount line items.

        Parameters
        ----------
        subtotal : float
            The subtotal from which the applicable discounted amounts will be subtracted.

        discountLines : List[DiscountLine]
            A list of discount line items.

        Returns
        -------
        float
            The final, summed-total of the given list of invoice line items
            less the given list of discount line items.
        """

        discountTotal = sum(discount.amount for discount in discountLines)

        return subtotal - discountTotal
