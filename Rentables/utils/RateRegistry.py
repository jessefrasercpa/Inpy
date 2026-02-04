from typing import List, Dict, Callable, Any
from .Rate import Rate


class RateRegistry:

    
    def __init__(self):

        self._builders: Dict[str, Callable[[Dict[str, Any]], Rate]] = {}

    
    def registerRate(self, name: str):

        def decorator(func: Callable[[Dict[str, Any]], Rate]):

            self._builders[name] = func

            return func
        
        return decorator
    

    def getRate(self, name: str, params: Dict[str, Any]) -> Rate:

        if name not in self._builders:

            raise ValueError(f"Unknown rate type: {name}")
        
        return self._builders[name](params)
    

    def listRates(self) -> List[str]:

        return list(self._builders.keys())
