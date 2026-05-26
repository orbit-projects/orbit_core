"""
Tests for Orbit routing utilities.

This module validates route registration,
route discovery, route matching, and route
metadata management.
"""

from orbit_types import RouteError

from orbit_core.routing import (
    RouteMatch,
    RouteRegistry,
)
from orbit_core.types import (
    RouteDefinition,
)


def example_handler() -> dict:
    """
    Example route handler.
    """

    return {
        "message": "orbit",
    }


def test_registry_creation() -> None:
    """
    Verify route registries can be created.
    """

    registry = RouteRegistry()

    assert registry.route_count == 0


def test_add_route() -> None:
    """
    Verify routes can be registered.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    assert registry.route_count == 1


def test_find_route() -> None:
    """
    Verify routes can be located.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    result = registry.find_route(
        method="GET",
        path="/users",
    )

    assert result is route


def test_find_route_missing() -> None:
    """
    Verify missing routes return None.
    """

    registry = RouteRegistry()

    result = registry.find_route(
        method="GET",
        path="/missing",
    )

    assert result is None


def test_duplicate_route_registration() -> None:
    """
    Verify duplicate routes are rejected.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    try:
        registry.add_route(route)

        raised = False

    except RouteError:
        raised = True

    assert raised


def test_method_lookup_is_case_insensitive() -> None:
    """
    Verify route lookup normalizes methods.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    result = registry.find_route(
        method="get",
        path="/users",
    )

    assert result is route


def test_get_routes() -> None:
    """
    Verify registered routes can be retrieved.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    routes = registry.get_routes()

    assert len(routes) == 1

    assert routes[0] is route


def test_get_routes_returns_copy() -> None:
    """
    Verify route collections are protected
    from external mutation.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    routes = registry.get_routes()

    routes.clear()

    assert registry.route_count == 1


def test_clear_routes() -> None:
    """
    Verify registered routes can be cleared.
    """

    registry = RouteRegistry()

    registry.add_route(
        RouteDefinition(
            path="/users",
            method="GET",
            handler=example_handler,
        )
    )

    registry.clear()

    assert registry.route_count == 0


def test_contains_route() -> None:
    """
    Verify membership checks work.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    assert route in registry


def test_registry_length() -> None:
    """
    Verify registry length reporting.
    """

    registry = RouteRegistry()

    registry.add_route(
        RouteDefinition(
            path="/users",
            method="GET",
            handler=example_handler,
        )
    )

    assert len(registry) == 1


def test_registry_iteration() -> None:
    """
    Verify route iteration support.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    routes = list(registry)

    assert len(routes) == 1

    assert routes[0] is route


def test_match_static_route() -> None:
    """
    Verify static routes can be matched.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    match = registry.match_route(
        method="GET",
        path="/users",
    )

    assert isinstance(
        match,
        RouteMatch,
    )

    assert match.route is route

    assert match.path_params == {}


def test_match_dynamic_route() -> None:
    """
    Verify dynamic routes can be matched.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users/{id}",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    match = registry.match_route(
        method="GET",
        path="/users/123",
    )

    assert match is not None

    assert match.path_params == {
        "id": "123",
    }


def test_match_multiple_parameters() -> None:
    """
    Verify multiple path parameters are
    extracted correctly.
    """

    registry = RouteRegistry()

    route = RouteDefinition(
        path="/users/{user_id}/posts/{post_id}",
        method="GET",
        handler=example_handler,
    )

    registry.add_route(route)

    match = registry.match_route(
        method="GET",
        path="/users/1/posts/99",
    )

    assert match is not None

    assert match.path_params == {
        "user_id": "1",
        "post_id": "99",
    }


def test_match_route_missing() -> None:
    """
    Verify unmatched routes return None.
    """

    registry = RouteRegistry()

    match = registry.match_route(
        method="GET",
        path="/missing",
    )

    assert match is None
