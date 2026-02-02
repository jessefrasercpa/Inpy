from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, TYPE_CHECKING
from .Rentable import Rentable


if TYPE_CHECKING:

    from .AddOn import AddOn


@dataclass(frozen=True)
class Room(Rentable):


    addOns: Tuple["AddOn", ...] = ()


    def supports(self, addOn: "AddOn") -> bool:

        return addOn in self.addOns
