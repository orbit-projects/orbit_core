"""
Orbit Core Types

Shared type definitions and structured metadata models
used throughout the Orbit core runtime.
"""

from dataclasses import dataclass
from collections.abc import Callable
from typing import Any


@dataclass
class RouteDefinition:
    """
    Represents a registered application route.

    A route definition contains all metadata required
    to register and execute an application endpoint.

    Attributes:
        path:
            URL path for the route.

        method:
            HTTP method associated with the route.

        handler:
            Route handler function.

        request_model:
            Optional request model extracted from the
            handler signature.

        response_model:
            Optional response model extracted from the
            handler return annotation.
    """

    path: str
    method: str
    handler: Callable[..., Any]

    request_model: type | None = None
    response_model: type | None = None
