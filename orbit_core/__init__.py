"""
Orbit Core Package

This module provides the main application interface for the Orbit framework.

It exposes the `App` class, which serves as the central object for:
- Defining routes
- Managing application state
- Integrating with server and SSG systems

Example:
    >>> from orbit_core import App
    >>> app = App()
"""

from .app import App

__all__ = ["App"]
