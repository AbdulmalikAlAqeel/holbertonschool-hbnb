"""Review API endpoints."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import facade

api = Namespace('reviews', description='Review operations')

# Define input models for Swagger UI documentation and payload validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})


@api.route('/')
class ReviewList(Resource):

    def get(self):
        """Public: Retrieve all reviews."""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    def post(self):
        """Protected: Create a new review with ownership & duplicate checks."""
        current_user_id = get_jwt_identity()
        data = api.payload
        place_id = data.get('place_id')

        # 1. Check if the target place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # 2. Constraint: Users cannot review their own places
        if place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        # 3. Constraint: Users cannot submit multiple reviews for the same place
        existing_reviews = facade.get_reviews_by_place(place_id)
        for rev in existing_reviews:
            if rev.user_id == current_user_id:
                return {'error': 'You have already reviewed this place'}, 400

        data['user_id'] = current_user_id
        try:
            new_review = facade.create_review(data)
            return new_review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<review_id>')
class ReviewResource(Resource):

    def get(self, review_id):
        """Public: Retrieve a specific review by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_update_model)
    def put(self, review_id):
        """Protected: Update a review (Only the author or admin can update)."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Validate ownership: only the review author or administrator is allowed
        if review.user_id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload
        try:
            updated_review = facade.update_review(review_id, data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, review_id):
        """Protected: Delete a review (Only the author or admin can delete)."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Validate ownership: only the review author or administrator is allowed
        if review.user_id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
