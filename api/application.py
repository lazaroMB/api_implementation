from flask import Flask

from .containers import Container
from . import views


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.container = container
    app.add_url_rule("/api/v1/shopping/statistics", "index", views.index)

    return app
