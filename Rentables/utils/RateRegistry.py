from typing import List, Dict, Callable, Any
from .Rate import Rate
from .Param import Param


class RateRegistry:

    
    def __init__(self):

        self._builders: Dict[str, Callable[[Dict[str, Any]], Rate]] = {}
        self._params: Dict[str, List[Param]] = {}

    
    def registerRate(self, name: str, params: List[Param]):

        def decorator(func):

            self._builders[name] = func
            self._params[name]   = params

            return func
        
        return decorator
    

    def getRate(self, name: str, params: Dict[str, Any]) -> Rate:

        if name not in self._builders:

            raise ValueError(f"Unknown rate type: {name}")
        
        rate = self._builders[name](params)

        return Rate(name=rate.name, rateFunc=rate.rateFunc, params=params)
    
    
    def getRateParams(self, name: str) -> List[Param]:

        if name not in self._params:

            raise ValueError(f"Unknown rate type: {name}")

        return self._params[name]
    

    def listRates(self) -> List[str]:

        return list(self._builders.keys())
