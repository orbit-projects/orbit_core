"""
Orbit Routing System

Provides route registration, route discovery,
route matching, and path parameter extraction
utilities for Orbit applications.

The routing system acts as the central registry
for application endpoints and is responsible for
maintaining route metadata used during request
dispatch.

Features:
    - Route registration
    - Duplicate route prevention
    - Static route matching
    - Dynamic route matching
    - Path parameter extraction
    - Route enumeration

Examples:
    Register a route::

        registry.add_route(route)

    Match a route::

        match = registry.match_route(
            method="GET",
            path="/users/123",
        )

    Access path parameters::

        user_id = match.path_params["id"]
"""

from __future__ import annotations

from dataclasses import dataclass

from orbit_types import RouteError

from .types import RouteDefinition

__all__ = [
    "RouteMatch",
    "RouteRegistry",
]


@dataclass(
    slots=True,
    frozen=True,
)
class RouteMatch:
    """
    Represents a successful route match.

    Attributes:
        route:
            Matched route definition.

        path_params:
            Extracted route path parameters.
    """

    route: RouteDefinition

    path_params: dict[str, str]


class RouteRegistry:
    """
    Stores and manages registered application routes.

    The route registry serves as the central source
    of truth for route definitions within an Orbit
    application.

    Supports both static and dynamic route matching.
    """

    def __init__(self) -> None:
        """
        Initialize an empty route registry.
        """

        self._routes: list[RouteDefinition] = []

    @property
    def route_count(self) -> int:
        """
        Retrieve the total number of registered
        routes.

        Returns:
            Number of registered routes.
        """

        return len(self._routes)

    def add_route(
        self,
        route: RouteDefinition,
    ) -> None:
        """
        Register a route definition.

        Args:
            route:
                Route definition to register.

        Raises:
            RouteError:
                If a matching route already exists.
        """

        existing_route = self.find_route(
            method=route.method,
            path=route.path,
        )

        if existing_route is not None:
            raise RouteError(
                f"Route already exists: {route.method} {route.path}"
            )

        self._routes.append(route)

    def find_route(
        self,
        method: str,
        path: str,
    ) -> RouteDefinition | None:
        """
        Find a route definition using an exact
        path match.

        Args:
            method:
                HTTP method.

            path:
                Route path.

        Returns:
            Matching route definition if found,
            otherwise None.
        """

        normalized_method = method.upper()

        for route in self._routes:
            if (
                route.method.upper() == normalized_method
                and route.path == path
            ):
                return route

        return None

    def match_route(
        self,
        method: str,
        path: str,
    ) -> RouteMatch | None:
        """
        Match a request path against registered
        routes.

        Supports dynamic route parameters using
        curly brace syntax.

        Example::

            /users/{id}

        Args:
            method:
                HTTP request method.

            path:
                Incoming request path.

        Returns:
            Route match result if successful,
            otherwise None.
        """

        normalized_method = method.upper()

        request_parts = path.strip("/").split("/")

        for route in self._routes:
            if route.method.upper() != normalized_method:
                continue

            route_parts = route.path.strip("/").split("/")

            if len(route_parts) != len(request_parts):
                continue

            path_params: dict[str, str] = {}

            matched = True

            for (
                route_part,
                request_part,
            ) in zip(
                route_parts,
                request_parts,
                strict=True,
            ):
                if route_part.startswith("{") and route_part.endswith("}"):
                    parameter_name = route_part[1:-1]

                    path_params[parameter_name] = request_part

                    continue

                if route_part != request_part:
                    matched = False
                    break

            if matched:
                return RouteMatch(
                    route=route,
                    path_params=path_params,
                )

        return None

    def get_routes(
        self,
    ) -> list[RouteDefinition]:
        """
        Retrieve all registered routes.

        Returns:
            Copy of registered route definitions.
        """

        return list(self._routes)

    def clear(self) -> None:
        """
        Remove all registered routes.
        """

        self._routes.clear()

    def __contains__(
        self,
        route: RouteDefinition,
    ) -> bool:
        """
        Determine whether a route exists.

        Args:
            route:
                Route definition to inspect.

        Returns:
            True if registered.
        """

        return route in self._routes

    def __iter__(self):
        """
        Iterate over registered routes.

        Returns:
            Route iterator.
        """

        return iter(self._routes)

    def __len__(self) -> int:
        """
        Retrieve total registered route count.

        Returns:
            Number of registered routes.
        """

        return self.route_count
