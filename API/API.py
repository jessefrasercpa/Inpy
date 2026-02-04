"""
TODO
----

 - Fix type: ignore(s).
"""

from datetime import date
from dataclasses import fields
from typing import Dict, Any, Type, TypeVar
from Rentables import (
    AddOn,
    Room
)
from Rentables.utils import (
    Rate,
    RateRegistry,
)
from Discounts import (
    Discount,
    DiscountRegistry
)
from Invoiceables import Invoiceable
from Invoices import (
    PricingEngine,
    InvoiceBuilder,
    Invoice
)
from .Exceptions import (
    RegistryError,
    ValidationError
)
from .DTOs import (
    RateDTO,
    DiscountDTO,
    AddOnDTO,
    RoomDTO,
    InvoiceableDTO,
    InvoiceDTO
)


DTO = TypeVar("DTO")


class API:

    
    def __init__(self):

        self._rateRegistry     = RateRegistry()
        self._discountRegistry = DiscountRegistry()
        self._pricingEngine    = PricingEngine()
        self._invoiceBuilder   = InvoiceBuilder(self._pricingEngine)

        self._DTOMap: Dict[str, Type[Any]] = {
            "rate": RateDTO,
            "discounts": DiscountDTO,
            "addOns": AddOnDTO,
            "rooms": RoomDTO,
            "invoiceable": InvoiceableDTO
        }


    def listRate(self):

        return self._rateRegistry.listRates()
    

    def listDiscount(self):

        return self._discountRegistry.listDiscounts()
    

    def _jsonToDTO(self, DTOCls: Type[DTO], json: Dict[str, Any]) -> DTO:

        kwargs: Dict[str, Any] = {}

        for field in fields(DTOCls): # type: ignore

            key = field.name

            if key not in json:

                continue

            val = json[key]

            if key in self._DTOMap:

                cls = self._DTOMap[key]

                if isinstance(val, list):

                    kwargs[key] = [self._jsonToDTO(cls, item) for item in val] # type: ignore

                else:

                    kwargs[key] = self._jsonToDTO(cls, val)

            else:

                kwargs[key] = val

        return DTOCls(**kwargs)
    

    def _buildRate(self, rateDTO: RateDTO) -> Rate:

        try:

            return self._rateRegistry.getRate(rateDTO.rateType, rateDTO.params)
        
        except Exception as e:

            raise RegistryError(f"Invalid rate definition: {rateDTO}") from e
        

    def buildRateFromJSON(self, rateJSON: Dict[str, Any]) -> Rate:

        rateDTO = self._jsonToDTO(RateDTO, rateJSON)

        return self._buildRate(rateDTO)
        

    def _buildDiscount(self, discountDTO: DiscountDTO) -> Discount:

        try:

            return self._discountRegistry.getDiscount(discountDTO.discountType, discountDTO.params)
        
        except Exception as e:

            raise RegistryError(f"Invalid discount definition: {discountDTO}") from e
        

    def buildDiscountFromJSON(self, discountJSON: Dict[str, Any]) -> Discount:

        discountDTO = self._jsonToDTO(DiscountDTO, discountJSON)

        return self._buildDiscount(discountDTO)
        
    
    def _buildAddOn(self, addOnDTO: AddOnDTO) -> AddOn:

        try:

            rate = self._buildRate(addOnDTO.rate)

            return AddOn(name=addOnDTO.name, rate=rate)
        
        except Exception as e:

            raise ValidationError(f"Invalid Add-On: {addOnDTO}") from e
        

    def buildAddOnFromJSON(self, addOnJSON: Dict[str, Any]) -> AddOn:

        addOnDTO = self._jsonToDTO(AddOnDTO, addOnJSON)

        return self._buildAddOn(addOnDTO)
        

    def _buildRoom(self, roomDTO: RoomDTO) -> Room:

        try:

            rate   = self._buildRate(roomDTO.rate)
            addOns = [self._buildAddOn(addOn) for addOn in roomDTO.addOns]

            return Room(name=roomDTO.name, rate=rate, addOns=tuple(addOns))
        
        except Exception as e:

            raise ValidationError(f"Invalid Room: {roomDTO}") from e
        

    def buildRoomFromJSON(self, roomJSON: Dict[str, Any]) -> Room:

        roomDTO = self._jsonToDTO(RoomDTO, roomJSON)

        return self._buildRoom(roomDTO)
        

    def _buildInvoiceable(self, invoiceableDTO: InvoiceableDTO) -> Invoiceable:

        try:

            rooms       = [self._buildRoom(room) for room in invoiceableDTO.rooms]
            addOns      = [self._buildAddOn(addOn) for addOn in invoiceableDTO.addOns]
            invoiceable = Invoiceable(rooms=rooms, addOns=addOns, t=invoiceableDTO.t)

            return invoiceable
        
        except Exception as e:

            raise ValidationError(f"Invalid Invoiceable: {invoiceableDTO}") from e
        

    def _buildInvoice(self, invoiceDTO: InvoiceDTO) -> Invoice:

        try:

            invoiceable = self._buildInvoiceable(invoiceDTO.invoiceable)
            discounts   = [self._buildDiscount(discount) for discount in invoiceDTO.discounts]

            return self._invoiceBuilder.build(
                invoiceNum=invoiceDTO.invoiceNum,
                payee=invoiceDTO.payee,
                dateCreated=date.fromisoformat(invoiceDTO.dateCreated),
                dateDue=date.fromisoformat(invoiceDTO.dateDue),
                invoiceable=invoiceable,
                discounts=discounts
            )
        
        except Exception as e:

            raise ValidationError(f"Failed to build invoice: {invoiceDTO}") from e


    def buildInvoiceFromJSON(self, invoiceJSON: Dict[str, Any]) -> Invoice:

        invoiceDTO = self._jsonToDTO(InvoiceDTO, invoiceJSON)

        return self._buildInvoice(invoiceDTO)
