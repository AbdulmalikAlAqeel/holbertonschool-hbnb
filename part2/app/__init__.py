from flask import Flask
from flask_restx import Api
from app.services.facade import HBnBFacade

facade = HBnBFacade()


def create_app(config_class=None):
    """Application factory: configure and return the Flask app."""
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'hbnb-temporary-secret-key'
    app.config['RESTX_MASK_SWAGGER'] = False

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='The backend RESTful API for the HBnB Evolution project (Part 2)',
        doc='/api/v1/doc'
    )

    from app.api.v1.users import api as users_ns
    api.add_namespace(users_ns, path='/api/v1/users')

    from app.api.v1.amenities import api as amenities_ns
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    from app.api.v1.places import api as places_ns
    api.add_namespace(places_ns, path='/api/v1/places')

    from app.api.v1.reviews import api as reviews_ns
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
