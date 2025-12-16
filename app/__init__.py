"""Application Flask pour l'auto-évaluation du TDAH adulte."""

from flask import Flask


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = 'dev-key-change-in-production'

    from . import routes
    app.register_blueprint(routes.bp)

    return app
