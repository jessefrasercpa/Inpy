from typing import TYPE_CHECKING, Any
from .Repo import Repo
from .Store import Store


if TYPE_CHECKING:

    from API import API


class AddOnRepo(Repo):

    
    def __init__(self, api: "API"):

        self.api   = api
        self.store = Store("data/addons.json")


    def ls(self) -> list[Any]:

        data = self.store.load()

        return [self.api.buildAddOnFromJSON(addOn) for addOn in data]
    

    def add(self, addOnJSON: dict[str, Any]) -> Any:

        addOn = self.api.buildAddOnFromJSON(addOnJSON)
        data  = self.store.load()

        if any(a["id"] == addOn.id for a in data):

            raise ValueError(f"Add-On {addOn.name} (id: {addOn.id}) already exists")
        
        data.append({
            "id": addOn.id,
            "name": addOn.name,
            "rate": {
                "rateType": addOn.rate.name,
                "params": addOn.rate.params
            }
        })

        self.store.save(data)

        return addOn

    
    def get(self, objID: str) -> Any | None:

        data = self.store.load()

        for addOn in data:

            if addOn["id"] == objID:

                return self.api.buildAddOnFromJSON(addOn)
            
        raise ValueError(f"Add-On with id '{objID}' does not exist")
    

    def delete(self, objID: str):

        self.get(objID)

        data = self.store.load()
        data = [addOn for addOn in data if addOn["id"] != objID]

        self.store.save(data)
