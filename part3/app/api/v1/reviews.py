from flask_restx import Namespace, Resource, fields

from app import facade


api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "text": fields.String(
        required=True,
        description="Text of the review"
    ),
    "rating": fields.Integer(
        required=True,
        description="Rating from 1 to 5"
    ),
    "user_id": fields.String(
        required=True,
        description="ID of the user"
    ),
    "place_id": fields.String(
        required=True,
        description="ID of the place"
    ),
})

review_update_model = api.model("ReviewUpdate", {
    "text": fields.String(
        description="Text of the review"
    ),
    "rating": fields.Integer(
        description="Rating from 1 to 5"
    ),
    "user_id": fields.String(
        description="ID of the user"
    ),
    "place_id": fields.String(
        description="ID of the place"
    ),
})


def serialize_review(review):
    """Return a serialized review."""
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "user_id": review.user_id,
        "place_id": review.place_id,
        "created_at": review.created_at.isoformat(),
        "updated_at": review.updated_at.isoformat(),
    }


@api.route("/")
class ReviewList(Resource):
    """Handle review collection operations."""

    @api.expect(review_model, validate=True)
    def post(self):
        """Register a new review."""
        try:
            review = facade.create_review(api.payload)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

        return serialize_review(review), 201

    def get(self):
        """Retrieve all reviews."""
        reviews = facade.get_all_reviews()

        return [
            serialize_review(review)
            for review in reviews
        ], 200


@api.route("/<string:review_id>")
class ReviewResource(Resource):
    """Handle operations for a single review."""

    def get(self, review_id):
        """Retrieve a review by ID."""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        return serialize_review(review), 200

    @api.expect(review_update_model, validate=False)
    def put(self, review_id):
        """Update a review."""
        if not api.payload:
            return {"error": "No data provided for update"}, 400

        try:
            review = facade.update_review(
                review_id,
                api.payload
            )
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

        if not review:
            return {"error": "Review not found"}, 404

        return serialize_review(review), 200

    def delete(self, review_id):
        """Delete a review."""
        deleted = facade.delete_review(review_id)

        if not deleted:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200
