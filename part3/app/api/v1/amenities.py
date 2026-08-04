from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# 1. Request Input Model (Payload for POST and PUT)
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# 2. Response Output Model (Success Response Payload)
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity unique identifier'),
    'name': fields.String(description='Name of the amenity')
})

# 3. Error Output Model (Standard Error Payload for 400, 404, etc.)
error_model = api.model('ErrorResponse', {
    'error': fields.String(description='Error description message')
})


def serialize_amenity(amenity):
    """Helper function to format amenity instance into JSON output."""
    return {
        'id': amenity.id,
        'name': amenity.name
    }


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created', amenity_response_model)
    @api.response(400, 'Invalid input data', error_model)
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return serialize_amenity(new_amenity), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully', [amenity_response_model])
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [serialize_amenity(amenity) for amenity in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully', amenity_response_model)
    @api.response(404, 'Amenity not found', error_model)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return serialize_amenity(amenity), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully', amenity_response_model)
    @api.response(400, 'Invalid input data', error_model)
    @api.response(404, 'Amenity not found', error_model)
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return serialize_amenity(updated_amenity), 200
        except ValueError as e:
            return {'error': str(e)}, 400
