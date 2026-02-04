from typing import List, Callable
from Invoiceables import Invoiceable
from .Discount import Discount


RateFunc = Callable[[float], float]


class RoomBundleDiscount(Discount):


    def __init__(self, name: str, rateFunc: RateFunc, roomBundleNames: List[str]):

        super().__init__(name, rateFunc)
        
        self._roomBundleNames = roomBundleNames


    def applies(self, invoiceable: Invoiceable) -> bool:

        selectedNames = {room.name for room in invoiceable.rooms}

        return set(self._roomBundleNames).issubset(selectedNames)
