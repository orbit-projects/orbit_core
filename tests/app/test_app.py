"""
Tests for Orbit application core.

This module validates application creation,
route registration, middleware handling,
and route metadata extraction.
"""

from orbit_types import (
    RequestModel,
)

from orbit_core import App


class UserRequest(
    RequestModel,
):
    """
    Example request model.
    """

    user_id: int


def test_app_creation() -> None:
    """
    Verify applications can be created.
    """

    app = App()

    assert isinstance(
        app,
        App,
    )


def test_app_default_debug_value() -> None:
    """
    Verify debug mode defaults to False.
    """

    app = App()

    assert app.debug is False


def test_app_custom_debug_value() -> None:
    """
    Verify debug mode can be configured.
    """

    app = App(
        debug=True,
    )

    assert app.debug is True


def test_route_registration() -> None:
    """
    Verify routes can be registered.
    """

    app = App()

    @app.get("/users")
    def get_users():
        return []

    assert app.route_count == 1


def test_get_route_registration() -> None:
    """
    Verify GET decorators register routes.
    """

    app = App()

    @app.get("/users")
    def get_users():
        return []

    route = app.get_routes()[0]

    assert route.path == "/users"

    assert route.method == "GET"


def test_post_route_registration() -> None:
    """
    Verify POST decorators register routes.
    """

    app = App()

    @app.post("/users")
    def create_user():
        return {}

    route = app.get_routes()[0]

    assert route.method == "POST"


def test_put_route_registration() -> None:
    """
    Verify PUT decorators register routes.
    """

    app = App()

    @app.put("/users")
    def update_user():
        return {}

    route = app.get_routes()[0]

    assert route.method == "PUT"


def test_delete_route_registration() -> None:
    """
    Verify DELETE decorators register routes.
    """

    app = App()

    @app.delete("/users")
    def delete_user():
        return {}

    route = app.get_routes()[0]

    assert route.method == "DELETE"


def test_patch_route_registration() -> None:
    """
    Verify PATCH decorators register routes.
    """

    app = App()

    @app.patch("/users")
    def patch_user():
        return {}

    route = app.get_routes()[0]

    assert route.method == "PATCH"


def test_request_model_detection() -> None:
    """
    Verify request models are detected
    from handler annotations.
    """

    app = App()

    @app.post("/users")
    def create_user(
        request: UserRequest,
    ):
        return {}

    route = app.get_routes()[0]

    assert route.request_model is UserRequest


def test_response_model_detection() -> None:
    """
    Verify response annotations are stored.
    """

    app = App()

    @app.get("/users")
    def get_users() -> list:
        return []

    route = app.get_routes()[0]

    assert route.response_model is list


def test_missing_response_annotation() -> None:
    """
    Verify missing response annotations
    are normalized to None.
    """

    app = App()

    @app.get("/users")
    def get_users():
        return []

    route = app.get_routes()[0]

    assert route.response_model is None


def test_get_routes() -> None:
    """
    Verify registered routes can be
    retrieved.
    """

    app = App()

    @app.get("/users")
    def get_users():
        return []

    routes = app.get_routes()

    assert len(routes) == 1


def test_route_count() -> None:
    """
    Verify route counts are reported.
    """

    app = App()

    @app.get("/users")
    def get_users():
        return []

    @app.get("/posts")
    def get_posts():
        return []

    assert app.route_count == 2


def test_add_middleware() -> None:
    """
    Verify middleware can be registered.
    """

    app = App()

    def middleware():
        pass

    app.add_middleware(
        middleware,
    )

    assert len(app.get_middlewares()) == 1


def test_get_middlewares_returns_copy() -> None:
    """
    Verify middleware collections are
    protected from external mutation.
    """

    app = App()

    def middleware():
        pass

    app.add_middleware(
        middleware,
    )

    middlewares = app.get_middlewares()

    middlewares.clear()

    assert len(app.get_middlewares()) == 1


def test_container_available() -> None:
    """
    Verify dependency injection container
    is available.
    """

    app = App()

    assert app.container is not None


def test_route_registry_available() -> None:
    """
    Verify route registry is available.
    """

    app = App()

    assert app.routes is not None
