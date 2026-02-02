from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, TYPE_CHECKING
from .Rentable import Rentable


if TYPE_CHECKING:

    from .AddOn import AddOn


@dataclass(frozen=True)
class Room(Rentable):
    """
    Encapsulates a rentable room which may support optional add-ons.

    Attributes
    ----------
    addOns : Tuple[AddOn, ...]
        A tuple of add-ons (possibly empty) which may be supported by this room.

    Methods
    -------
    supports(addOn: AddOn) -> bool
        Checks whether a given add-on is supported by this room.
    """


    addOns: Tuple["AddOn", ...] = ()


    def supports(self, addOn: "AddOn") -> bool:
        """
        Checks whether a given add-on is supported by this room.

        Parameters
        ----------
        addOn : AddOn
            The add-on to check.

        Returns
        -------
        bool
            True if the add-on is in this room's addOns, False otherwise.
        """

        return addOn in self.addOns
