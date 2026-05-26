"""
Orbit Core Package

Core runtime abstractions and foundational primitives
used throughout the Orbit framework.

This package exposes the public API for:

- Application lifecycle management
- Dependency injection
- Route registration
- Core routing definitions

Exports:
    App:
        Main application abstraction for Orbit.

    Container:
        Dependency injection container used for service management.

    Scope:
        Defines dependency lifecycle scopes.

    RouteRegistry:
        Stores and manages application routes.

    RouteDefinition:
        Represents a registered route definition.
"""

from .app import App
from .container import Container, Scope
from .routing import RouteRegistry
from .types import RouteDefinition

__all__ = [
    "App",
    "Container",
    "Scope",
    "RouteRegistry",
    "RouteDefinition",
]
