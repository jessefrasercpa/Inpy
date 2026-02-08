from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Param:
    """
    Encapsulates a generic parameter definition for a rate function.

    Attributes
    ----------
    name : str
        A Human-readable identifier.

    type : str
        The parameter type.

    description : str
        A Human-readable description.

    constraints : Dict[str, Any]
        Optional constraints.
    """

    name: str
    type: str
    description: str = ""
    constraints: Dict[str, Any] = field(default_factory=dict)
