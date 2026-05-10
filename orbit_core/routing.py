from typing import List
from .types import RouteDefinition


class RouteRegistry:
    """
    A registry for storing and managing route definitions.

    This class maintains a collection of RouteDefinition objects
    and provides methods to add and retrieve them.
    """

    def __init__(self):
        """
        Initialize an empty route registry.

        Attributes:
            routes (List[RouteDefinition]): A list to store registered routes.
        """
        self.routes: List[RouteDefinition] = []

    def add(self, route: RouteDefinition):
        """
        Add a new route to the registry.

        Args:
            route (RouteDefinition): The route definition to be added.
        """
        self.routes.append(route)

    def get_all(self):
        """
        Retrieve all registered routes.

        Returns:
            List[RouteDefinition]: A list of all stored route definitions.
        """
        return self.routes
