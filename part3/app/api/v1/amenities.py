from flask_restx import Namespace, Resource, fields

from app import facade


api = Namespace("amenities", description="Amenity operations")


amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(
            required=True,
            description="Amenity name"
        ),
    },
)


def serialize_amenity(amenity):
    """Convert an amenity object to a dictionary."""
    return {
        "id": amenity.id,
        "name": amenity.name,
    }


@api.route("/")
class AmenityList(Resource):
    """Resource for creating and retrieving amenities."""

    @api.expect(amenity_model, validate=True)
    def post(self):
        """Create a new amenity."""
        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

        return serialize_amenity(new_amenity), 201

    def get(self):
        """Retrieve all amenities."""
        amenities = facade.get_all_amenities()

        return [
            serialize_amenity(amenity)
            for amenity in amenities
        ], 200


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    """Resource for retrieving and updating an amenity."""

    def get(self, amenity_id):
        """Retrieve an amenity by ID."""
        amenity = facade.get_amenity(amenity_id)

        if amenity is None:
            return {"error": "Amenity not found"}, 404

        return serialize_amenity(amenity), 200

    @api.expect(amenity_model, validate=True)
    def put(self, amenity_id):
        """Update an existing amenity."""
        amenity = facade.get_amenity(amenity_id)

        if amenity is None:
            return {"error": "Amenity not found"}, 404

        amenity_data = api.payload

        try:
            updated_amenity = facade.update_amenity(
                amenity_id,
                amenity_data
            )
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

        return serialize_amenity(updated_amenity), 200
