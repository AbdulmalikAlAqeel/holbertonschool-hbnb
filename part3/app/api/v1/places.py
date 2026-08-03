from flask_restx import Namespace, Resource, fields

from app import facade


api = Namespace("places", description="Place operations")

place_model = api.model("Place", {
    "title": fields.String(
        required=True,
        description="Title of the place"
    ),
    "description": fields.String(
        description="Description of the place"
    ),
    "price": fields.Float(
        required=True,
        description="Price per night"
    ),
    "latitude": fields.Float(
        required=True,
        description="Latitude of the place"
    ),
    "longitude": fields.Float(
        required=True,
        description="Longitude of the place"
    ),
    "owner_id": fields.String(
        required=True,
        description="ID of the owner"
    ),
    "amenities": fields.List(
        fields.String,
        description="List of amenity IDs"
    ),
})


def serialize_place_summary(place):
    """Return a short representation of a place."""
    return {
        "id": place.id,
        "title": place.title,
        "latitude": place.latitude,
        "longitude": place.longitude,
    }


def serialize_place(place):
    """Return a detailed representation of a place."""
    owner = {
        "id": place.owner.id,
        "first_name": place.owner.first_name,
        "last_name": place.owner.last_name,
        "email": place.owner.email,
    }

    amenities = [
        {
            "id": amenity.id,
            "name": amenity.name,
        }
        for amenity in place.amenities
    ]

    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner": owner,
        "amenities": amenities,
    }


@api.route("/")
class PlaceList(Resource):
    """Handle place collection operations."""

    @api.expect(place_model, validate=True)
    def post(self):
        """Register a new place."""
        try:
            place = facade.create_place(api.payload)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "amenities": [
                amenity.id for amenity in place.amenities
            ],
        }, 201

    def get(self):
        """Retrieve all places."""
        places = facade.get_all_places()

        return [
            serialize_place_summary(place)
            for place in places
        ], 200


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    """Handle operations for a single place."""

    def get(self, place_id):
        """Retrieve place details by ID."""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        return serialize_place(place), 200

    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """Update a place."""
        if not facade.get_place(place_id):
            return {"error": "Place not found"}, 404

        try:
            updated_place = facade.update_place(
                place_id,
                api.payload
            )
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

        return serialize_place(updated_place), 200


@api.route("/<string:place_id>/reviews")
class PlaceReviewList(Resource):
    """Handle reviews belonging to a place."""

    def get(self, place_id):
        """Retrieve all reviews for a place."""
        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:
            return {"error": "Place not found"}, 404

        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id,
            }
            for review in reviews
        ], 200
