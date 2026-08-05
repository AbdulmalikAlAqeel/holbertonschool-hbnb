"""User API endpoints with admin-level constraints."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user'),
    'password': fields.String(required=True, description='Password for the user account'),
    'is_admin': fields.Boolean(description='Admin status flag', default=False)
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address (Admin only)'),
    'password': fields.String(description='Password (Admin only)'),
    'is_admin': fields.Boolean(description='Admin privileges status (Admin only)')
})


@api.route('/')
class UserList(Resource):

    def get(self):
        """Public: Retrieve all registered users."""
        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200

    @api.expect(user_model, validate=True)
    def post(self):
        """Public / Admin: Register user (Non-admins cannot create admin accounts)."""
        data = api.payload

        # Restriction: Regular users cannot create admin accounts directly
        if data.get('is_admin', False):
            try:
                claims = get_jwt()
                if not claims.get('is_admin', False):
                    return {'error': 'Admin access required to create an admin user'}, 403
            except Exception:
                return {'error': 'Admin access required to create an admin user'}, 403

        # Validate unique email
        existing_user = facade.get_user_by_email(data.get('email'))
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<user_id>')
class UserResource(Resource):

    @jwt_required()
    def get(self, user_id):
        """Protected: Retrieve user details by ID."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(user_update_model)
    def put(self, user_id):
        """Protected: Modify user details (Admins can update email and password)."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # 1. Authorization check: Account owner or Administrator
        if current_user_id != user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        # 2. Verify target user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = api.payload

        # 3. Restriction: Non-admin users cannot alter sensitive fields
        if not is_admin:
            if 'email' in data or 'password' in data or 'is_admin' in data:
                return {'error': 'Updating email or password is not allowed here'}, 400

        # 4. Admin uniqueness check when updating email
        if 'email' in data and data['email'] != user.email:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, user_id):
        """Protected / Admin: Delete a user account."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Deletion permitted only for the user themselves or an administrator
        if current_user_id != user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200
