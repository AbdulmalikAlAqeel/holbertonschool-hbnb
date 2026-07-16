from flask_restx import Namespace, Resource, fields

from app import facade


api = Namespace("places", description="Place operations")

amenity_model = api.model("PlaceAmenity", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(description="Amenity name"),
})

owner_model = api.model("PlaceOwner", {
    "id": fields.String(description="Owner ID"),
    "first_name": fields.String(description="Owner first name"),
    "last_name": fields.String(description="Owner last name"),
    "email": fields.String(description="Owner email"),
})

place_model = api.model("Place", {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude of the place"),
    "longitude": fields.Float(required=True, description="Longitude of the place"),
    "owner_id": fields.String(required=True, description="ID of the owner"),
    "amenities": fields.List(fields.String, description="List of amenity IDs"),
})


def serialize_place_summary(place):
    return {
        "id": place.id,
        "title": place.title,
        "latitude": place.latitude,
        "longitude": place.longitude,
    }


@api.route("/")
class PlaceList(Resource):

    @api.expect(place_model, validate=True)
    def post(self):
        """Register a new place."""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400
        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner_id": new_place.owner_id,
            "amenities": new_place.amenities,
        }, 201

    def get(self):
        """Retrieve a list of all places."""
        places = facade.get_all_places()
        return [serialize_place_summary(p) for p in places], 200


@api.route("/<string:place_id>")
class PlaceResource(Resource):

    def get(self, place_id):
        """Get place details by ID, including owner and amenities."""
        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)
        owner_data = None
        if owner is not None:
            owner_data = {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email,
            }

        amenities_data = []
        for amenity_id in place.amenities:
            amenity = facade.get_amenity(amenity_id)
            if amenity is not None:
                amenities_data.append({"id": amenity.id, "name": amenity.name})

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": owner_data,
            "amenities": amenities_data,
        }, 200

    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """Update a place's information."""
        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404
        place_data = api.payload
        try:
            facade.update_place(place_id, place_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400
        return {"message": "Place updated successfully"}, 200


@api.route("/<string:place_id>/reviews")
class PlaceReviewList(Resource):

    def get(self, place_id):
        """Get all reviews for a specific place."""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return [{
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
        } for review in reviews], 200
