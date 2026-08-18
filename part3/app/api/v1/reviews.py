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
        current_user = get_jwt_identity()
        current_user_id = current_user['id']
        data = api.payload

        place = facade.get_place(data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404

        
        place_owner_id = getattr(place, 'owner_id', None) or (place.owner.id if getattr(place, 'owner', None) else None)

        
        if place_owner_id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        
        existing_reviews = facade.get_reviews_by_place(place.id) if hasattr(facade, 'get_reviews_by_place') else facade.get_all_reviews()

        
        for rev in existing_reviews:
            rev_place_id = getattr(rev, 'place_id', None) or (rev.place.id if getattr(rev, 'place', None) else None)
            rev_user_id = getattr(rev, 'user_id', None) or (rev.user.id if getattr(rev, 'user', None) else None)

            if str(rev_place_id) == str(place.id) and str(rev_user_id) == str(current_user_id):
                return {'error': 'You have already reviewed this place'}, 400

        
        review_data = {
            'text': data['text'],
            'rating': data['rating'],
            'place_id': place.id,
            'user_id': current_user_id
        }
        new_review = facade.create_review(review_data)
        return new_review, 201


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
        identity = get_jwt_identity()
        claims = get_jwt()

        
        if isinstance(identity, dict):
            current_user_id = identity.get('id')
            is_admin = identity.get('is_admin', claims.get('is_admin', False))
        else:
            current_user_id = identity
            is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        
        author_id = getattr(review, 'user_id', None) or (review.user.id if getattr(review, 'user', None) else None)

        
        if str(author_id) != str(current_user_id) and not is_admin:
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
