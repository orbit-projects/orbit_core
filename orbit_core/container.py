import inspect
import sys
from enum import Enum


class Scope(Enum):
    """
    Defines the lifecycle scope of a dependency.

    Attributes:
        SINGLETON: A single instance is created and reused globally.
        REQUEST: A single instance is created per request context.
        TRANSIENT: A new instance is created every time it is resolved.
    """
    SINGLETON = "singleton"
    REQUEST = "request"
    TRANSIENT = "transient"


class Container:
    """
    A simple dependency injection container.

    This container manages class registrations and resolves dependencies
    based on their defined scope (singleton, request, or transient).
    """

    def __init__(self):
        """
        Initialize the container.

        Attributes:
            _singletons (dict): Stores singleton instances.
            _providers (dict): Maps classes to their registered scope.
        """
        self._singletons = {}
        self._providers = {}

    def register(self, cls, scope=Scope.SINGLETON):
        """
        Register a class with a specific scope.

        Args:
            cls (type): The class to register.
            scope (Scope): The lifecycle scope of the class.
        """
        self._providers[cls] = scope

    def resolve(self, cls, request_cache=None):
        """
        Resolve an instance of the given class.

        This method determines the scope of the class and creates or retrieves
        an instance accordingly.

        Args:
            cls (type): The class to resolve.
            request_cache (dict, optional): Cache for request-scoped instances.

        Returns:
            object: An instance of the requested class.
        """
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
        """
        Create an instance of a class by resolving its constructor dependencies.

        This method inspects the __init__ signature of the class and recursively
        resolves all annotated dependencies.

        Args:
            cls (type): The class to instantiate.
            request_cache (dict): Cache for request-scoped instances.

        Returns:
            object: A fully constructed instance of the class.

        Raises:
            Exception: If a constructor parameter lacks a type annotation.
        """
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
