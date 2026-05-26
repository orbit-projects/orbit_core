"""
Orbit Routing System

Provides route registration and route lookup utilities
for Orbit applications.
"""

from .types import RouteDefinition


class RouteRegistry:
    """
    Stores and manages registered application routes.
    """

    def __init__(self):
        """
        Initialize an empty route registry.
        """

        self._routes: list[RouteDefinition] = []

    def add_route(self, route: RouteDefinition) -> None:
        """
        Register a new route definition.

        Args:
            route:
                Route definition to register.

        Raises:
            ValueError:
                If a duplicate route already exists.
        """

        existing = self.find_route(
            method=route.method,
            path=route.path,
        )

        if existing is not None:
            raise ValueError(f"Route already exists: " f"{route.method} {route.path}")

        self._routes.append(route)

    def find_route(
        self,
        method: str,
        path: str,
    ) -> RouteDefinition | None:
        """
        Find a route matching method and path.

        Args:
            method:
                HTTP method.

            path:
                Route path.

        Returns:
            Matching route definition if found,
            otherwise None.
        """

        for route in self._routes:
            if route.method == method and route.path == path:
                return route

        return None

    def get_routes(self) -> list[RouteDefinition]:
        """
        Retrieve all registered routes.

        Returns:
            List of registered route definitions.
        """

        return self._routes
