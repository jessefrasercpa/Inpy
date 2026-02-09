from typing import TYPE_CHECKING, Dict, Any
from Rentables.utils import Param
from Discounts import Discount
from Invoiceables import Invoiceable


if TYPE_CHECKING:

    from API import API


def registerDefaultDiscounts(api: API):

    @api.registerDiscount(
        "Room Bundle Discount",
        [
            Param(
                name="room bundle names",
                type="list[str]",
                description="Names of the rooms in the bundle"
            ),
            Param(
                name="rate",
                type="float",
                description="Discount factor (%)"
            )
        ]
    )
    def buildRoomBundleDiscount(params: Dict[str, Any]) -> Discount:

        roomBundleNames = params["room bundle names"]
        rate            = float(params["rate"])


        class _RoomBundleDiscount(Discount):


            def applies(self, invoiceable: Invoiceable) -> bool:

                selectedNames = {room.name for room in invoiceable.rooms}

                return set(roomBundleNames).issubset(selectedNames)
            

        return _RoomBundleDiscount(
            name="Room Bundle Discount",
            rateFunc=lambda subtotal: subtotal * rate
        )
