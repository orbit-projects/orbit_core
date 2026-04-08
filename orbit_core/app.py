from .types import RouteDefinition
from .container import Container
import inspect
from orbit_types import RequestModel


class App:
    def __init__(self):
        self.routes = []
        self.container = Container()
        self.middlewares = []
        self.debug = True

    def route(self, path: str, method: str = "GET", ssg: bool = False):
        def decorator(func):
            sig = inspect.signature(func)

            request_model = None
            response_model = sig.return_annotation

            for param in sig.parameters.values():
                if issubclass_safe(param.annotation, RequestModel):
                    request_model = param.annotation

            route_def = RouteDefinition(
                path=path,
                method=method,
                handler=func,
                request_model=request_model,
                response_model=response_model,
            )

            route_def.ssg = ssg
            
            self.routes.append(route_def)

            return func

        return decorator

    def get_routes(self):
        return self.routes

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)


def issubclass_safe(cls, base):
    try:
        return issubclass(cls, base)
    except Exception:
        return False
