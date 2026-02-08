from typing import List, Callable
from dataclasses import dataclass
from Invoiceables import Invoiceable
from .Discount import Discount


RateFunc = Callable[[float], float]


@dataclass(frozen=True)
class RoomBundleDiscount(Discount):


    roomBundleNames: List[str]


    def applies(self, invoiceable: Invoiceable) -> bool:

        selectedNames = {room.name for room in invoiceable.rooms}

        return set(self.roomBundleNames).issubset(selectedNames)
