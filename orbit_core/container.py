import inspect
import sys
from enum import Enum


class Scope(Enum):
    SINGLETON = "singleton"
    REQUEST = "request"
    TRANSIENT = "transient"


class Container:
    def __init__(self):
        self._singletons = {}
        self._providers = {} 

    def register(self, cls, scope=Scope.SINGLETON):
        self._providers[cls] = scope

    def resolve(self, cls, request_cache=None):
        print("RESOLVING:", cls)
    
        scope = self._providers.get(cls)
    
        if scope is None:
            scope = Scope.TRANSIENT
    
        print("SCOPE:", scope)
    
        if scope == Scope.SINGLETON:
            ...
        elif scope == Scope.REQUEST:
            ...
        elif scope == Scope.TRANSIENT:
            instance = self._create_instance(cls, request_cache)
            print("CREATED INSTANCE:", instance)
            return instance
            
    def _create_instance(self, cls, request_cache):
        sig = inspect.signature(cls.__init__)
        kwargs = {}
    
        for name, param in sig.parameters.items():
            if name == "self":
                continue
    
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue
    
            param_type = param.annotation
    
            if isinstance(param_type, str):
                module = sys.modules[cls.__module__]
                param_type = getattr(module, param_type)
    
            if param_type == inspect._empty:
                raise Exception(f"Missing type annotation for {name} in {cls}")
    
            if isinstance(param_type, type):
                kwargs[name] = self.resolve(param_type, request_cache)
    
        return cls(**kwargs)
