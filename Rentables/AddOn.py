from dataclasses import dataclass
from .Rentable import Rentable


@dataclass(frozen=True)
class AddOn(Rentable):
    """
    Encapsulates an optional rentable add-on.
    """

    pass
