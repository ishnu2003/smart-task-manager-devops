"""Application factory for the Smart Task Manager API."""

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    PrometheusMetrics(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
