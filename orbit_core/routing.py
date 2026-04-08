from typing import List
from .types import RouteDefinition


class RouteRegistry:
    def __init__(self):
        self.routes: List[RouteDefinition] = []

    def add(self, route: RouteDefinition):
        self.routes.append(route)

    def get_all(self):
        return self.routes
