from flask import Flask
from flask_restx import Api
from app.services.facade import HBnBFacade

# Global instance of the Facade.
# This serves as the single entry point to coordinate the business logic 
# and persistence layers, making it accessible across all API namespaces.
facade = HBnBFacade()

def create_app(config_class=None):
    """
    Application Factory function to configure, initialize, and return 
    the Flask application instance.
    """
    app = Flask(__name__)
    
    # Basic configuration settings for development
    app.config['SECRET_KEY'] = 'hbnb-temporary-secret-key'
    app.config['RESTX_MASK_SWAGGER'] = False  # Disables the default "X-Fields" mask filter in Swagger UI

    # Initialize Flask-RESTx Api instance for documentation and routing
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='The backend RESTful API for the HBnB Evolution project (Part 2)',
        doc='/api/v1/doc'  # Endpoint where Swagger UI documentation will be hosted
    )

    # =========================================================================
    # NAMESPACES REGISTRATION
    # =========================================================================
    # As you implement the API endpoints in Task 1 and onward, import 
    # and register your namespaces here to expose them to the Swagger UI.
    #
    # Example:
    # from app.api.v1.users import api as users_ns
    # api.add_namespace(users_ns, path='/api/v1/users')
    #
    # from app.api.v1.amenities import api as amenities_ns
    # api.add_namespace(amenities_ns, path='/api/v1/amenities')
    #
    # from app.api.v1.places import api as places_ns
    # api.add_namespace(places_ns, path='/api/v1/places')
    #
    # from app.api.v1.reviews import api as reviews_ns
    # api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
