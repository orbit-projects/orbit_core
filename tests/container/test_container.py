"""
Tests for Orbit dependency injection container.

This module validates dependency registration,
resolution, lifecycle scopes, and constructor
injection behavior.
"""

from orbit_types import (
    DependencyError,
)

from orbit_core.container import (
    Container,
    Scope,
)


class Database:
    """
    Example database service.
    """


class Repository:
    """
    Example repository service.
    """

    def __init__(
        self,
        database: Database,
    ) -> None:
        self.database = database


class Service:
    """
    Example application service.
    """

    def __init__(
        self,
        repository: Repository,
    ) -> None:
        self.repository = repository


class UnannotatedDependency:
    """
    Dependency containing an invalid
    constructor signature.
    """

    def __init__(
        self,
        value,
    ) -> None:
        self.value = value


def test_container_creation() -> None:
    """
    Verify containers can be created.
    """

    container = Container()

    assert isinstance(
        container,
        Container,
    )


def test_register_dependency() -> None:
    """
    Verify dependencies can be registered.
    """

    container = Container()

    container.register(
        Database,
    )

    assert Database in container._providers


def test_resolve_singleton_dependency() -> None:
    """
    Verify singleton dependencies return
    the same instance.
    """

    container = Container()

    container.register(
        Database,
        scope=Scope.SINGLETON,
    )

    first = container.resolve(
        Database,
    )

    second = container.resolve(
        Database,
    )

    assert first is second


def test_resolve_transient_dependency() -> None:
    """
    Verify transient dependencies return
    new instances.
    """

    container = Container()

    container.register(
        Database,
        scope=Scope.TRANSIENT,
    )

    first = container.resolve(
        Database,
    )

    second = container.resolve(
        Database,
    )

    assert first is not second


def test_resolve_request_dependency() -> None:
    """
    Verify request-scoped dependencies
    share a request cache instance.
    """

    container = Container()

    container.register(
        Database,
        scope=Scope.REQUEST,
    )

    request_cache = {}

    first = container.resolve(
        Database,
        request_cache=request_cache,
    )

    second = container.resolve(
        Database,
        request_cache=request_cache,
    )

    assert first is second


def test_request_scope_isolated_between_requests() -> None:
    """
    Verify request-scoped dependencies
    are isolated between requests.
    """

    container = Container()

    container.register(
        Database,
        scope=Scope.REQUEST,
    )

    first = container.resolve(
        Database,
        request_cache={},
    )

    second = container.resolve(
        Database,
        request_cache={},
    )

    assert first is not second


def test_constructor_injection() -> None:
    """
    Verify constructor dependencies are
    resolved automatically.
    """

    container = Container()

    service = container.resolve(
        Service,
    )

    assert isinstance(
        service,
        Service,
    )

    assert isinstance(
        service.repository,
        Repository,
    )

    assert isinstance(
        service.repository.database,
        Database,
    )


def test_nested_dependency_resolution() -> None:
    """
    Verify dependency graphs are resolved
    recursively.
    """

    container = Container()

    repository = container.resolve(
        Repository,
    )

    assert isinstance(
        repository.database,
        Database,
    )


def test_unannotated_dependency_raises_error() -> None:
    """
    Verify unannotated constructor
    parameters raise DependencyError.
    """

    container = Container()

    try:
        container.resolve(
            UnannotatedDependency,
        )

        raised = False

    except DependencyError:
        raised = True

    assert raised


def test_clear_singletons() -> None:
    """
    Verify singleton cache can be cleared.
    """

    container = Container()

    first = container.resolve(
        Database,
    )

    container.clear_singletons()

    second = container.resolve(
        Database,
    )

    assert first is not second


def test_scope_enum_values() -> None:
    """
    Verify supported scope values.
    """

    assert Scope.SINGLETON.value == "singleton"

    assert Scope.REQUEST.value == "request"

    assert Scope.TRANSIENT.value == "transient"
