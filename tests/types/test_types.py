"""
Tests for Orbit core type definitions.

This module validates the shared framework
contracts and metadata models used throughout
Orbit Core.
"""

from orbit_core.types import (
    DependencyProvider,
    Handler,
    LifecycleHook,
    Middleware,
    RouteDefinition,
)


def example_handler() -> dict:
    """
    Example route handler.
    """

    return {
        "message": "orbit",
    }


def test_route_definition_creation() -> None:
    """
    Verify route definitions can be created.
    """

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    assert route.path == "/users"

    assert route.method == "GET"

    assert route.handler is example_handler


def test_route_definition_request_model_default() -> None:
    """
    Verify request model defaults to None.
    """

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    assert route.request_model is None


def test_route_definition_response_model_default() -> None:
    """
    Verify response model defaults to None.
    """

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    assert route.response_model is None


def test_route_definition_custom_models() -> None:
    """
    Verify custom request and response
    models can be stored.
    """

    class Request:
        pass

    class Response:
        pass

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
        request_model=Request,
        response_model=Response,
    )

    assert route.request_model is Request

    assert route.response_model is Response


def test_route_definition_is_frozen() -> None:
    """
    Verify route definitions are immutable.
    """

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    try:
        route.path = "/posts"

        mutation_succeeded = True

    except Exception:
        mutation_succeeded = False

    assert not mutation_succeeded


def test_handler_contract_exists() -> None:
    """
    Verify handler contract is exposed.
    """

    assert Handler is not None


def test_middleware_contract_exists() -> None:
    """
    Verify middleware contract is exposed.
    """

    assert Middleware is not None


def test_dependency_provider_contract_exists() -> None:
    """
    Verify dependency provider contract
    is exposed.
    """

    assert DependencyProvider is not None


def test_lifecycle_hook_contract_exists() -> None:
    """
    Verify lifecycle hook contract is
    exposed.
    """

    assert LifecycleHook is not None
