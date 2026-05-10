from .types import RouteDefinition
from .container import Container
import inspect
from orbit_types import RequestModel


class App:
    """
    Core application class for the Orbit framework.

    The `App` class is responsible for:
    - Registering routes
    - Managing middleware
    - Holding application-level state
    - Acting as the central entry point for Orbit applications

    Example:
        >>> from orbit_core import App
        >>> app = App()
        >>>
        >>> @app.route("/")
        >>> def home():
        >>>     return {"message": "Hello Orbit"}
    """

    def __init__(self):
        """
        Initialize a new Orbit application instance.

        Attributes:
            routes (list): Registered route definitions.
            container (Container): Dependency injection container.
            middlewares (list): List of middleware functions.
            debug (bool): Debug mode flag.
        """
        self.routes = []
        self.container = Container()
        self.middlewares = []
        self.debug = True

    def route(self, path: str, method: str = "GET", ssg: bool = False):
        """
        Register a route with the application.

        This decorator binds a function to a specific route path and HTTP method.
        It also inspects the function signature to automatically detect:

        - Request model (if provided as a parameter)
        - Response model (from return annotation)

        Args:
            path (str): URL path (e.g. "/about").
            method (str, optional): HTTP method. Defaults to "GET".
            ssg (bool, optional): Whether this route should be statically generated.

        Returns:
            Callable: A decorator that registers the route handler.

        Example:
            >>> @app.route("/user")
            >>> def get_user(request: RequestModel):
            >>>     return {"id": 1}

        Example (SSG):
            >>> @app.route("/blog", ssg=True)
            >>> def blog():
            >>>     return {"posts": []}
        """
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
        """
        Retrieve all registered routes.

        Returns:
            list[RouteDefinition]: List of route definitions.
        """
        return self.routes

    def add_middleware(self, middleware):
        """
        Add a middleware to the application.

        Middleware functions are executed during request handling
        and can be used for logging, authentication, etc.

        Args:
            middleware (Callable): Middleware function.
        """
        self.middlewares.append(middleware)


def issubclass_safe(cls, base):
    """
    Safely check if a class is a subclass of another.

    This function prevents runtime errors when dealing with
    annotations that may not be valid classes.

    Args:
        cls: The class to check.
        base: The base class.

    Returns:
        bool: True if `cls` is a subclass of `base`, otherwise False.
    """
    try:
        return issubclass(cls, base)
    except Exception:
        return False
