from flask_restx import Namespace, Resource, fields

from app import facade


api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "text": fields.String(required=True, description="Text of the review"),
    "rating": fields.Integer(required=True, description="Rating of the place (1-5)"),
    "user_id": fields.String(required=True, description="ID of the user"),
    "place_id": fields.String(required=True, description="ID of the place"),
})


def serialize_review(review):
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "user_id": review.user_id,
        "place_id": review.place_id,
    }


@api.route("/")
class ReviewList(Resource):

    @api.expect(review_model, validate=True)
    def post(self):
        """Register a new review."""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400
        return serialize_review(new_review), 201

    def get(self):
        """Retrieve a list of all reviews."""
        reviews = facade.get_all_reviews()
        return [serialize_review(r) for r in reviews], 200


@api.route("/<string:review_id>")
class ReviewResource(Resource):

    def get(self, review_id):
        """Get review details by ID."""
        review = facade.get_review(review_id)
        if review is None:
            return {"error": "Review not found"}, 404
        return serialize_review(review), 200

    @api.expect(review_model, validate=True)
    def put(self, review_id):
        """Update a review's information."""
        review = facade.get_review(review_id)
        if review is None:
            return {"error": "Review not found"}, 404
        review_data = api.payload
        try:
            facade.update_review(review_id, review_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400
        return {"message": "Review updated successfully"}, 200

    def delete(self, review_id):
        """Delete a review."""
        review = facade.get_review(review_id)
        if review is None:
            return {"error": "Review not found"}, 404
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
