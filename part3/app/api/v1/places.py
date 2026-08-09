"""Place API endpoints."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import facade

api = Namespace('places', description='Place operations')

# Input models for Swagger UI documentation and validation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude (-90 to 90)'),
    'longitude': fields.Float(required=True, description='Longitude (-180 to 180)'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude (-90 to 90)'),
    'longitude': fields.Float(description='Longitude (-180 to 180)'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})


@api.route('/')
class PlaceList(Resource):

    def get(self):
        """Public: Retrieve all places."""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    def post(self):
        """Protected: Create a new place (owner_id automatically set from JWT identity)."""
        current_user_id = get_jwt_identity()
        data = api.payload

        # Automatically bind the creation of the place to the authenticated user
        data['owner_id'] = current_user_id

        try:
            new_place = facade.create_place(data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        """Public: Retrieve detailed information for a specific place by ID."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @jwt_required()
    @api.expect(place_update_model)
    def put(self, place_id):
        """Protected: Update place details (Only place owner or administrator)."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Validate ownership: strict access control unless current user is the owner or an admin
        if place.owner_id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload
        try:
            updated_place = facade.update_place(place_id, data)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, place_id):
        """Protected: Delete a place (Only place owner or administrator)."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Validate ownership: strict access control unless current user is the owner or an admin
        if place.owner_id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200
