from dataclasses import dataclass
from .Rentable import Rentable


@dataclass(frozen=True)
class AddOn(Rentable):

    pass
