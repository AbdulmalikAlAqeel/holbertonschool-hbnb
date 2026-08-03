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
    @api.expect(review_update_model, validate=False)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input')
def put(self, review_id):
        """
        Update an existing review partially and return the updated review data.

        Args:
            review_id (str): The unique identifier of the review to update.

        Returns:
            tuple: A dictionary containing the updated review details and HTTP status 200,
                   or an error payload with status 400/404.
        """
        # Extract request payload
        data = api.payload
        if not data:
            return {'error': 'No data provided for update'}, 400

        try:
            # Delegate update operation to the business logic layer via Facade
            updated_review = facade.update_review(review_id, data)
            if not updated_review:
                return {'error': 'Review not found'}, 404

            # Format and return the full updated review object along with ISO timestamps
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id,
                'created_at': updated_review.created_at.isoformat() if hasattr(updated_review, 'created_at') and updated_review.created_at else None,
                'updated_at': updated_review.updated_at.isoformat() if hasattr(updated_review, 'updated_at') and updated_review.updated_at else None
            }, 200
        except ValueError as err:
            # Handle validation errors (e.g., out-of-range rating)
            return {'error': str(err)}, 400

    def delete(self, review_id):
        """Delete a review."""
        review = facade.get_review(review_id)
        if review is None:
            return {"error": "Review not found"}, 404
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
