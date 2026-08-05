"""Flask application factory."""

from flask import Flask
from flask_restx import Api

from app.extensions import bcrypt
from app.services.facade import HBnBFacade


facade = HBnBFacade()


def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    app.config["RESTX_MASK_SWAGGER"] = False

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Evolution backend RESTful API",
        doc="/api/v1/doc"
    )

    from app.api.v1.users import api as users_ns
    api.add_namespace(users_ns, path="/api/v1/users")

    from app.api.v1.amenities import api as amenities_ns
    api.add_namespace(amenities_ns, path="/api/v1/amenities")

    from app.api.v1.places import api as places_ns
    api.add_namespace(places_ns, path="/api/v1/places")

    from app.api.v1.reviews import api as reviews_ns
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    return app
