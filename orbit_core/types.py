from typing import Callable, Type


class RouteDefinition:
    def __init__(
        self,
        path: str,
        method: str,
        handler: Callable,
        request_model: Type | None,
        response_model: Type | None,
    ):
        self.path = path
        self.method = method
        self.handler = handler
        self.request_model = request_model
        self.response_model = response_model
