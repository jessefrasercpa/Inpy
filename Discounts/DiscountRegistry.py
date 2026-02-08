from typing import List, Dict, Callable, Any
from Rentables.utils import Param
from .Discount import Discount


class DiscountRegistry:

    
    def __init__(self):

        self._builders: Dict[str, Callable[[Dict[str, Any]], Discount]] = {}
        self._params: Dict[str, List[Param]] = {}

    
    def registerDiscount(self, name: str, params: List[Param]):

        def decorator(func: Callable[[Dict[str, Any]], Discount]):

            self._builders[name] = func
            self._params[name]   = params

            return func
        
        return decorator
    

    def getDiscount(self, name: str, params: Dict[str, Any]) -> Discount:

        if name not in self._builders:

            raise ValueError(f"Unknown discount type: {name}")
        
        return self._builders[name](params)
    

    def getDiscountParams(self, name: str) -> List[Param]:

        if name not in self._params:
            
            raise ValueError(f"Unknown discount type: {name}")
        
        return self._params[name]
    

    def listDiscounts(self) -> List[str]:

        return list(self._builders.keys())
