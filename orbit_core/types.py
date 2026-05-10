from typing import Callable, Type


class RouteDefinition:
    """
    Represents a route configuration in the application.

    This class encapsulates all necessary metadata required to define
    an HTTP route, including its path, method, handler function,
    and optional request/response models.
    """

    def __init__(
        self,
        path: str,
        method: str,
        handler: Callable,
        request_model: Type | None,
        response_model: Type | None,
    ):
        """
        Initialize a route definition.

        Args:
            path (str): The URL path for the route.
            method (str): The HTTP method (e.g., GET, POST).
            handler (Callable): The function that handles the request.
            request_model (Type | None): The expected request data model (if any).
            response_model (Type | None): The expected response data model (if any).
        """
        self.path = path
        self.method = method
        self.handler = handler
        self.request_model = request_model
        self.response_model = response_model
