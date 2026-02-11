from typing import TYPE_CHECKING, Dict, Any
from .Rate import Rate
from .Param import Param


if TYPE_CHECKING:

    from API import API


def registerDefaultRates(api: API):


    @api.registerRate(
            "Fixed Rate",
            [
                Param(
                    name="Rate",
                    type="float",
                    description="Cost per unit time"
                )
            ]
    )
    def buildFixedRate(params: Dict[str, Any]) -> Rate:

        rate = float(params["Rate"])

        return Rate(
            name="Fixed Rate",
            rateFunc=lambda t: rate * t
        )


    @api.registerRate(
            "Flat Rate",
            [
                Param(
                    name="Rate",
                    type="float",
                    description="Flat cost"
                )
            ]
    )
    def buildFlatRate(params: Dict[str, Any]) -> Rate:

        rate = float(params["Rate"])

        return Rate(
            name="Flat Rate",
            rateFunc=lambda t: rate
        )
