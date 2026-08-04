from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define input model for payload validation (User Creation / Update)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user'),
    'password': fields.String(required=False, description='Password of the user')
})

# Define standard success output model (Excludes sensitive data like password)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User unique identifier'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address of the user')
})

# Define standard error response model for status codes (400, 404, etc.)
error_model = api.model('ErrorResponse', {
    'error': fields.String(description='Error description message')
})


def serialize_user(user):
    """Helper function to format user entity to JSON response excluding sensitive data."""
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Email already registered or invalid input data', error_model)
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Check for existing email registration
        existing_user = facade.get_user_by_email(user_data.get('email'))
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return serialize_user(new_user), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully', [user_response_model])
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [serialize_user(user) for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully', user_response_model)
    @api.response(404, 'User not found', error_model)
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return serialize_user(user), 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully', user_response_model)
    @api.response(400, 'Invalid input data or email conflict', error_model)
    @api.response(404, 'User not found', error_model)
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Check for email conflict if email is updated
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

        try:
            if hasattr(facade, 'update_user'):
                updated_user = facade.update_user(user_id, user_data)
            else:
                user.update(user_data)
                updated_user = user

            return serialize_user(updated_user), 200
        except ValueError as e:
            return {'error': str(e)}, 400
