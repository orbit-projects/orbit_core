"""
Orbit Dependency Injection Container

Provides lightweight dependency registration and
resolution utilities for Orbit applications.
"""

from enum import Enum


class Scope(Enum):
    """
    Supported dependency lifecycle scopes.
    """

    SINGLETON = "singleton"
    REQUEST = "request"
    TRANSIENT = "transient"


class Container:
    """
    Lightweight dependency injection container.

    The container is responsible for:
    - Dependency registration
    - Dependency resolution
    - Scope management
    """

    def __init__(self):
        """
        Initialize a new dependency container.
        """

        self._singletons = {}
        self._providers = {}

    def register(
        self,
        cls,
        scope: Scope = Scope.SINGLETON,
    ) -> None:
        """
        Register a dependency provider.

        Args:
            cls:
                Dependency class.

            scope:
                Dependency lifecycle scope.
        """

        self._providers[cls] = scope

    def resolve(
        self,
        cls,
        request_cache=None,
    ):
        """
        Resolve a dependency instance.

        Args:
            cls:
                Dependency class.

            request_cache:
                Optional request-scoped cache.

        Returns:
            Resolved dependency instance.
        """

        scope = self._providers.get(
            cls,
            Scope.SINGLETON,
        )

        if scope == Scope.SINGLETON:
            if cls not in self._singletons:
                self._singletons[cls] = cls()

            return self._singletons[cls]

        if scope == Scope.REQUEST:
            if request_cache is None:
                request_cache = {}

            if cls not in request_cache:
                request_cache[cls] = cls()

            return request_cache[cls]

        return cls()
