"""
Orbit Core Package

Core runtime abstractions and foundational
primitives used throughout the Orbit framework.

Orbit Core provides the application runtime,
routing system, dependency injection container,
and framework contracts used by higher-level
Orbit components.

This package exposes the public API for:

- Application lifecycle management
- Route registration and matching
- Dependency injection
- Route metadata definitions
- Framework type contracts

Exports:
    App:
        Main application abstraction.

    Container:
        Dependency injection container.

    Scope:
        Dependency lifecycle scope definition.

    RouteRegistry:
        Route registration and lookup system.

    RouteMatch:
        Successful route match result.

    RouteDefinition:
        Registered route metadata definition.

    Handler:
        Generic route handler contract.

    Middleware:
        Generic middleware contract.

    DependencyProvider:
        Dependency provider contract.

    LifecycleHook:
        Application lifecycle hook contract.
"""

from .app import App
from .container import (
    Container,
    Scope,
)
from .routing import (
    RouteMatch,
    RouteRegistry,
)
from .types import (
    DependencyProvider,
    Handler,
    LifecycleHook,
    Middleware,
    RouteDefinition,
)

__all__ = [
    "App",
    "Container",
    "Scope",
    "RouteRegistry",
    "RouteMatch",
    "RouteDefinition",
    "Handler",
    "Middleware",
    "DependencyProvider",
    "LifecycleHook",
]
