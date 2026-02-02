from dataclasses import dataclass
from typing import List
from Rentables import (
    AddOn,
    Room
)


@dataclass
class Invoiceable:


    addOns: List[AddOn]
    rooms: List[Room]
    t: float


    def approve(self):

        for addOn in self.addOns:

            if not any(room.supports(addOn) for room in self.rooms):

                raise ValueError(f"Add-On '{addOn.name}' is not supported for current room selection.")
