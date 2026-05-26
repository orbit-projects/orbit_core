"""
Orbit Application Core

This module provides the main App class used to
create and configure Orbit applications.

The application core is responsible for:

- Route registration
- Middleware management
- Dependency injection access
- Application-level configuration

Example:
    app = App()

    @app.get("/")
    def home():
        return {"message": "Hello Orbit"}
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any

from orbit_kit.typing import (
    issubclass_safe,
)
from orbit_types import RequestModel

from .container import Container
from .routing import RouteRegistry
from .types import (
    Middleware,
    RouteDefinition,
)

__all__ = [
    "App",
]


class App:
    """
    Core application class for the Orbit framework.

    Responsibilities:
        - Route registration
        - Middleware management
        - Application lifecycle coordination
        - Dependency injection access

    Attributes:
        routes:
            Registered application routes.

        container:
            Dependency injection container.

        middlewares:
            Registered middleware handlers.

        debug:
            Debug mode flag.
    """

    def __init__(
        self,
        debug: bool = False,
    ) -> None:
        """
        Initialize a new Orbit application.

        Args:
            debug:
                Enable debug mode.
        """

        self.routes = RouteRegistry()

        self.container = Container()

        self.middlewares: list[Middleware] = []

        self.debug = debug

    @property
    def route_count(self) -> int:
        """
        Retrieve the number of registered routes.

        Returns:
            Total registered route count.
        """

        return self.routes.route_count

    def route(
        self,
        path: str,
        method: str = "GET",
    ) -> Callable[..., Any]:
        """
        Register a route with the application.

        Args:
            path:
                Route URL path.

            method:
                HTTP method associated with
                the route.

        Returns:
            Route decorator.
        """

        def decorator(
            func: Callable[..., Any],
        ) -> Callable[..., Any]:
            """
            Route registration decorator.

            Args:
                func:
                    Route handler function.

            Returns:
                Original handler function.
            """

            signature = inspect.signature(
                func,
            )

            request_model = None

            response_model = (
                None
                if (signature.return_annotation is inspect.Signature.empty)
                else signature.return_annotation
            )

            for parameter in signature.parameters.values():
                if issubclass_safe(
                    parameter.annotation,
                    RequestModel,
                ):
                    request_model = parameter.annotation

                    break

            route_definition = RouteDefinition(
                path=path,
                method=method.upper(),
                handler=func,
                request_model=request_model,
                response_model=response_model,
            )

            self.routes.add_route(
                route_definition,
            )

            return func

        return decorator

    def get(
        self,
        path: str,
    ) -> Callable[..., Any]:
        """
        Register a GET route.

        Args:
            path:
                Route URL path.

        Returns:
            Route decorator.
        """

        return self.route(
            path=path,
            method="GET",
        )

    def post(
        self,
        path: str,
    ) -> Callable[..., Any]:
        """
        Register a POST route.

        Args:
            path:
                Route URL path.

        Returns:
            Route decorator.
        """

        return self.route(
            path=path,
            method="POST",
        )

    def put(
        self,
        path: str,
    ) -> Callable[..., Any]:
        """
        Register a PUT route.

        Args:
            path:
                Route URL path.

        Returns:
            Route decorator.
        """

        return self.route(
            path=path,
            method="PUT",
        )

    def delete(
        self,
        path: str,
    ) -> Callable[..., Any]:
        """
        Register a DELETE route.

        Args:
            path:
                Route URL path.

        Returns:
            Route decorator.
        """

        return self.route(
            path=path,
            method="DELETE",
        )

    def patch(
        self,
        path: str,
    ) -> Callable[..., Any]:
        """
        Register a PATCH route.

        Args:
            path:
                Route URL path.

        Returns:
            Route decorator.
        """

        return self.route(
            path=path,
            method="PATCH",
        )

    def get_routes(
        self,
    ) -> list[RouteDefinition]:
        """
        Retrieve all registered routes.

        Returns:
            Copy of registered route definitions.
        """

        return self.routes.get_routes()

    def add_middleware(
        self,
        middleware: Middleware,
    ) -> None:
        """
        Register application middleware.

        Args:
            middleware:
                Middleware callable.
        """

        self.middlewares.append(
            middleware,
        )

    def get_middlewares(
        self,
    ) -> list[Middleware]:
        """
        Retrieve registered middleware.

        Returns:
            Copy of registered middleware.
        """

        return list(
            self.middlewares,
        )
