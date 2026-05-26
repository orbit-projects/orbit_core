"""
Orbit Core Types

Shared type definitions and structured metadata
models used throughout the Orbit core runtime.

This module provides foundational contracts used
by routing, dependency injection, middleware,
and application orchestration components.

The types defined here are intentionally lightweight
and implementation-agnostic to ensure they can be
shared throughout Orbit Core without introducing
unnecessary coupling.

Exports:
    Handler:
        Generic application handler callable.

    Middleware:
        Generic middleware callable.

    DependencyProvider:
        Dependency injection provider callable.

    LifecycleHook:
        Application lifecycle hook callable.

    RouteDefinition:
        Structured route metadata definition.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

__all__ = [
    "DependencyProvider",
    "Handler",
    "LifecycleHook",
    "Middleware",
    "RouteDefinition",
]


# ---------------------------------------------------------------------------
# Shared Framework Contracts
# ---------------------------------------------------------------------------

Handler = Callable[..., Any]
"""
Generic application handler callable.
"""

Middleware = Callable[..., Any]
"""
Generic middleware callable.
"""

DependencyProvider = Callable[..., Any]
"""
Dependency injection provider callable.
"""

LifecycleHook = Callable[..., Any]
"""
Application lifecycle hook callable.
"""


# ---------------------------------------------------------------------------
# Route Metadata Models
# ---------------------------------------------------------------------------


@dataclass(
    slots=True,
    frozen=True,
)
class RouteDefinition:
    """
    Represents a registered application route.

    A route definition contains all metadata
    required to register and execute an
    application endpoint.

    Attributes:
        path:
            URL path associated with the route.

        method:
            HTTP method associated with the route.

        handler:
            Route handler callable.

        request_model:
            Optional request model extracted from
            handler annotations.

        response_model:
            Optional response model extracted from
            handler annotations.
    """

    path: str
    method: str

    handler: Handler

    request_model: type | None = None
    response_model: type | None = None
