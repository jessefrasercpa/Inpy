from typing import List, Dict, Callable, Any
from .Discount import Discount


class DiscountRegistry:

    
    def __init__(self):

        self._builders: Dict[str, Callable[[Dict[str, Any]], Discount]] = {}

    
    def registerDiscount(self, name: str):

        def decorator(func: Callable[[Dict[str, Any]], Discount]):

            self._builders[name] = func

            return func
        
        return decorator
    

    def getDiscount(self, name: str, params: Dict[str, Any]) -> Discount:

        if name not in self._builders:

            raise ValueError(f"Unknown discount type: {name}")
        
        return self._builders[name](params)
    

    def listDiscounts(self) -> List[str]:

        return list(self._builders.keys())
