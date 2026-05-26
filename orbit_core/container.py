"""
Orbit Dependency Injection Container

Provides dependency registration, dependency
resolution, and lifecycle management utilities
for Orbit applications.

The dependency injection container serves as the
central mechanism for constructing and managing
application services.

Features:
    - Dependency registration
    - Automatic constructor injection
    - Singleton scope
    - Request scope
    - Transient scope
    - Circular dependency detection

Examples:
    Register a dependency::

        container.register(Database)

    Resolve a dependency::

        database = container.resolve(
            Database,
        )

    Automatic dependency injection::

        class Repository:
            def __init__(
                self,
                database: Database,
            ):
                self.database = database

        repository = container.resolve(
            Repository,
        )
"""

from __future__ import annotations

from enum import Enum
from inspect import signature

from orbit_types import DependencyError

__all__ = [
    "Container",
    "Scope",
]


class Scope(Enum):
    """
    Supported dependency lifecycle scopes.

    Attributes:
        SINGLETON:
            Single shared application instance.

        REQUEST:
            Single instance per request.

        TRANSIENT:
            New instance for every resolution.
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
    - Dependency lifecycle management
    - Constructor dependency injection

    Notes:
        Dependencies are resolved recursively
        using constructor annotations.
    """

    def __init__(self) -> None:
        """
        Initialize a dependency container.
        """

        self._singletons: dict[type, object] = {}

        self._providers: dict[
            type,
            Scope,
        ] = {}

    def register(
        self,
        dependency: type,
        scope: Scope = Scope.SINGLETON,
    ) -> None:
        """
        Register a dependency.

        Args:
            dependency:
                Dependency type.

            scope:
                Dependency lifecycle scope.
        """

        self._providers[dependency] = scope

    def resolve(
        self,
        dependency: type,
        request_cache: (dict[type, object] | None) = None,
    ) -> object:
        """
        Resolve a dependency instance.

        Args:
            dependency:
                Dependency type.

            request_cache:
                Optional request-scoped cache.

        Returns:
            Resolved dependency instance.

        Raises:
            DependencyError:
                If dependency resolution fails.
        """

        return self._resolve(
            dependency=dependency,
            request_cache=request_cache,
            resolving=set(),
        )

    def _resolve(
        self,
        dependency: type,
        request_cache: (dict[type, object] | None),
        resolving: set[type],
    ) -> object:
        """
        Internal dependency resolution.

        Args:
            dependency:
                Dependency type.

            request_cache:
                Request-scoped cache.

            resolving:
                Currently resolving dependencies.

        Returns:
            Resolved dependency instance.

        Raises:
            DependencyError:
                If resolution fails.
        """

        if dependency in resolving:
            raise DependencyError(
                f"Circular dependency detected for {dependency.__name__}"
            )

        scope = self._providers.get(
            dependency,
            Scope.SINGLETON,
        )

        if scope == Scope.SINGLETON:
            if dependency not in self._singletons:
                self._singletons[dependency] = self._create_instance(
                    dependency,
                    request_cache,
                    resolving,
                )

            return self._singletons[dependency]

        if scope == Scope.REQUEST:
            if request_cache is None:
                request_cache = {}

            if dependency not in request_cache:
                request_cache[dependency] = self._create_instance(
                    dependency,
                    request_cache,
                    resolving,
                )

            return request_cache[dependency]

        return self._create_instance(
            dependency,
            request_cache,
            resolving,
        )

    def _create_instance(
        self,
        dependency: type,
        request_cache: (dict[type, object] | None),
        resolving: set[type],
    ) -> object:
        """
        Create a dependency instance.

        Constructor dependencies are resolved
        automatically using type annotations.

        Args:
            dependency:
                Dependency type.

            request_cache:
                Request cache.

            resolving:
                Active resolution chain.

        Returns:
            Constructed dependency instance.

        Raises:
            DependencyError:
                If construction fails.
        """

        resolving.add(
            dependency,
        )

        try:
            constructor = signature(
                dependency.__init__,
            )

            parameters = []

            for parameter in constructor.parameters.values():
                if parameter.name == "self":
                    continue

                if parameter.kind in (
                    parameter.VAR_POSITIONAL,
                    parameter.VAR_KEYWORD,
                ):
                    continue

                annotation = parameter.annotation

                if annotation is parameter.empty:
                    raise DependencyError(
                        f"Dependency "
                        f"{dependency.__name__} "
                        f"contains an "
                        f"unannotated "
                        f"parameter: "
                        f"{parameter.name}"
                    )

                resolved = self._resolve(
                    dependency=annotation,
                    request_cache=request_cache,
                    resolving=resolving,
                )

                parameters.append(
                    resolved,
                )

            return dependency(
                *parameters,
            )

        except DependencyError:
            raise

        except Exception as error:
            raise DependencyError(
                f"Unable to resolve {dependency.__name__}"
            ) from error

        finally:
            resolving.discard(
                dependency,
            )

    def clear_singletons(
        self,
    ) -> None:
        """
        Clear singleton instances.

        Primarily intended for testing.
        """

        self._singletons.clear()
