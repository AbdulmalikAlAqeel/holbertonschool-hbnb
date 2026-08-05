"""Amenity API endpoints."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Input models for Swagger UI documentation and request validation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):

    def get(self):
        """Public: Retrieve all amenities."""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def post(self):
        """Admin Only: Create a new amenity."""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin access required'}, 403

        data = api.payload
        try:
            new_amenity = facade.create_amenity(data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<amenity_id>')
class AmenityResource(Resource):

    def get(self, amenity_id):
        """Public: Retrieve an amenity by ID."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def put(self, amenity_id):
        """Admin Only: Update an amenity."""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin access required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            return updated_amenity.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, amenity_id):
        """Admin Only: Delete an amenity."""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin access required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully'}, 200
