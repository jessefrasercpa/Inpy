from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RateDTO:


    rateType: str
    params: Dict[str, Any]


@dataclass
class DiscountDTO:


    discountType: str
    params: Dict[str, Any]


@dataclass
class AddOnDTO:


    id: str
    name: str
    rate: RateDTO


@dataclass
class RoomDTO:


    id: str
    name: str
    rate: RateDTO
    addOns: List[AddOnDTO]


@dataclass
class InvoiceableDTO:


    rooms: List[RoomDTO]
    addOns: List[AddOnDTO]
    t: float


@dataclass
class InvoiceDTO:


    invoiceNum: int
    payee: str
    dateCreated: str
    dateDue: str
    invoiceable: InvoiceableDTO
    discounts: List[DiscountDTO]
