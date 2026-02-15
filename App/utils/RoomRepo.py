from typing import TYPE_CHECKING, Any
from .Repo import Repo
from .Store import Store


if TYPE_CHECKING:

    from API import API


class RoomRepo(Repo):


    def __init__(self, api: "API"):

        self.api   = api
        self.store = Store("data/rooms.json")


    def ls(self) -> list[Any]:

        data = self.store.load()

        return [self.api.buildRoomFromJSON(room) for room in data]
    

    def add(self, roomJSON: dict[str, Any]) -> Any:

        room = self.api.buildRoomFromJSON(roomJSON)
        data = self.store.load()

        if any(r["id"] == room.id for r in data):

            raise ValueError(f"Room {room} (id: {room.id}) already exists")
        
        data.append(
            {
                "id": room.id,
                "name": room.name,
                "rate": {
                    "rateType": room.rate.name,
                    "params": room.rate.params
                },
                "addOns": [
                    {
                        "id": addOn.id,
                        "name": addOn.name,
                        "rate": {
                            "rateType": addOn.rate.name,
                            "params": addOn.rate.params
                        }
                    }
                    for addOn in room.addOns
                ]
            }
        )

        self.store.save(data)

        return room
    

    def get(self, objID: str) -> Any | None:

        data = self.store.load()

        for room in data:

            if room["id"] == objID:

                return self.api.buildRoomFromJSON(room)
            
        raise ValueError(f"Room with id '{objID}' does not exist")
    

    def delete(self, objID: str):

        self.get(objID)

        data = self.store.load()
        data = [room for room in data if room["id"] != objID]

        self.store.save(data)
