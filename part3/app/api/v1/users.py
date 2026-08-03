from flask_restx import Namespace, Resource, fields

from app import facade


api = Namespace("users", description="User operations")


user_model = api.model(
    "User",
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)


def serialize_user(user):
    """Convert a user object to a dictionary without the password."""
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }


@api.route("/")
class UserList(Resource):

    @api.expect(user_model, validate=True)
    def post(self):
        """Create a new user."""
        user_data = api.payload

        if facade.get_user_by_email(user_data["email"]):
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

        return serialize_user(new_user), 201

    def get(self):
        """Retrieve all users."""
        users = facade.get_all_users()
        return [serialize_user(user) for user in users], 200


@api.route("/<string:user_id>")
class UserResource(Resource):

    def get(self, user_id):
        """Retrieve one user by ID."""
        user = facade.get_user(user_id)

        if user is None:
            return {"error": "User not found"}, 404

        return serialize_user(user), 200

    @api.expect(user_model, validate=True)
    def put(self, user_id):
        """Update an existing user."""
        user = facade.get_user(user_id)

        if user is None:
            return {"error": "User not found"}, 404

        user_data = api.payload

        if "email" in user_data:
            existing_user = facade.get_user_by_email(user_data["email"])

            if existing_user and existing_user.id != user_id:
                return {"error": "Email already registered"}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

        return serialize_user(updated_user), 200
