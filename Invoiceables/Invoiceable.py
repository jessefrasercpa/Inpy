from dataclasses import dataclass
from typing import List
from Rentables import (
    AddOn,
    Room
)


@dataclass
class Invoiceable:
    """
    Encapsulates an invoiceable entity which has
    a selection of rooms, a list of supported add-ons,
    and a duration of time over which the rooms and add-ons are to be rented.

    Attributes
    ----------
    addOns : List[AddOn]
        A list of supported add-ons.

    rooms : List[Room]
        A selection of rooms.

    t : float
        A duration of time over which the rooms and add-ons are to be rented.
    """


    addOns: List[AddOn]
    rooms: List[Room]
    t: float


    def approve(self):
        """
        Checks whether addOns is fully supported by the current room selection in rooms.
        """

        for addOn in self.addOns:

            if not any(room.supports(addOn) for room in self.rooms):

                raise ValueError(f"Add-On '{addOn.name}' is not supported for current room selection.")
