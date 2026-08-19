"""Flask application factory."""

from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.extensions import bcrypt, db
from app.services.facade import HBnBFacade

# Initialize the main facade instance for business logic access
facade = HBnBFacade()

# Instantiate JWTManager extension
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)
    # Load configuration settings from the specified config object/string
    app.config.from_object(config_class)

    # Initialize extensions with the application instance
    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    # Disable Swagger payload masking
    app.config["RESTX_MASK_SWAGGER"] = False

    # Initialize Flask-RESTx API
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Evolution backend RESTful API",
        doc="/api/v1/doc"
    )

    # Import and register application namespaces
    from app.api.v1.users import api as users_ns
    api.add_namespace(users_ns, path="/api/v1/users")

    from app.api.v1.amenities import api as amenities_ns
    api.add_namespace(amenities_ns, path="/api/v1/amenities")

    from app.api.v1.places import api as places_ns
    api.add_namespace(places_ns, path="/api/v1/places")

    from app.api.v1.reviews import api as reviews_ns
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    from app.api.v1.auth import api as auth_ns
    api.add_namespace(auth_ns, path="/api/v1/auth")

    return app
