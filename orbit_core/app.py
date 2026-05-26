"""
Orbit Application Core

This module provides the main `App` class used to create
and configure Orbit applications.

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

from collections.abc import Callable
from typing import Any
import inspect

from orbit_types import RequestModel

from .container import Container
from .routing import RouteRegistry
from .types import RouteDefinition


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

    def __init__(self, debug: bool = False):
        """
        Initialize a new Orbit application instance.
        """

        self.routes = RouteRegistry()
        self.container = Container()
        self.middlewares: list[Callable[..., Any]] = []
        self.debug = debug

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
                HTTP method used for the route.

        Returns:
            Route decorator.
        """

        def decorator(
            func: Callable[..., Any],
        ) -> Callable[..., Any]:
            sig = inspect.signature(func)

            request_model = None
            response_model = sig.return_annotation

            for param in sig.parameters.values():
                if issubclass_safe(
                    param.annotation,
                    RequestModel,
                ):
                    request_model = param.annotation

            route_def = RouteDefinition(
                path=path,
                method=method,
                handler=func,
                request_model=request_model,
                response_model=response_model,
            )

            self.routes.add_route(route_def)

            return func

        return decorator

    def get(
        self,
        path: str,
    ) -> Callable[..., Any]:
        """
        Register a GET route.
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
        """

        return self.route(
            path=path,
            method="PATCH",
        )

    def get_routes(self) -> list[RouteDefinition]:
        """
        Retrieve all registered routes.

        Returns:
            List of registered route definitions.
        """

        return self.routes.get_routes()

    def add_middleware(
        self,
        middleware: Callable[..., Any],
    ) -> None:
        """
        Register application middleware.

        Args:
            middleware:
                Middleware callable.
        """

        self.middlewares.append(middleware)


def issubclass_safe(
    cls: Any,
    base: type,
) -> bool:
    """
    Safely determine whether a class is a subclass
    of another.
    """

    try:
        return issubclass(cls, base)
    except TypeError:
        return False
