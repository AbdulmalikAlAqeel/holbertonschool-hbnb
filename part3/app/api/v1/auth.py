"""Authentication endpoints for HBnB."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Input payload model for login documentation and validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    """Resource for handling user authentication and JWT generation."""

    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT access token."""
        data = api.payload
        email = data.get('email')
        password = data.get('password')

        # Retrieve user by email address via the facade service layer
        user = facade.get_user_by_email(email)

        # Validate user existence and check password hash match
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        # Embed custom claims inside the JWT payload (e.g., administrator status)
        additional_claims = {
            'is_admin': user.is_admin
        }

        # Generate JWT access token using the user's unique identifier as identity
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )

        return {'access_token': access_token}, 200
