from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING
from .Rentable import Rentable


if TYPE_CHECKING:

    from .AddOn import AddOn


@dataclass(frozen=True)
class Room(Rentable):


    addOns: List["AddOn"] = field(default_factory=list) # type: ignore


    def supports(self, addOn: "AddOn") -> bool:

        return addOn in self.addOns
