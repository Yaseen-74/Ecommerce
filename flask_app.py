from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from backend.dto.catalogue import Catalogue
from backend.services.catalogue_service import CatalogueService
from backend.exception.exceptions import (
    CatalogueError, CatalogueDateExpired,
    CatalogueDeleteError, CatalogueNotFoundError,
    CatalogueUpdateError, DatabaseConnectorError
)
from datetime import datetime

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)
app.config['JSON_SORT_KEYS'] = False  # Maintain dictionary order in JSON responses
service = CatalogueService()

# Homepage route (serves index.html)
@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

@app.route('/api/catalogues', methods=['GET'])
def get_all_catalogues():
    """Get all catalogues in JSON format"""
    try:
        catalogues = service.get_all_catalogue_json()
        return jsonify({
            'status': 'success',
            'data': catalogues,
            'count': len(catalogues)
        })
    except DatabaseConnectorError as e:
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch catalogues: {str(e)}'
        }), 500

@app.route('/api/catalogues/<int:catalogue_id>', methods=['GET'])
def get_catalogue(catalogue_id):
    """Get a single catalogue by ID"""
    try:
        catalogue = service.get_catalogue_json(catalogue_id)
        return jsonify({
            'status': 'success',
            'data': catalogue
        })
    except CatalogueNotFoundError as e:
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch catalogue: {str(e)}'
        }), 500

@app.route('/api/catalogues', methods=['POST'])
def create_catalogue():
    """Create a new catalogue"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }), 400

        # Additional validation: name and description must be strings and not all digits
        if not isinstance(data['name'], str) or data['name'].strip() == '' or data['name'].isdigit():
            return jsonify({
                'status': 'error',
                'message': 'Catalogue name must be a non-empty string and not all digits.'
            }), 400
        if not isinstance(data['description'], str) or data['description'].strip() == '' or data['description'].isdigit():
            return jsonify({
                'status': 'error',
                'message': 'Catalogue description must be a non-empty string and not all digits.'
            }), 400

        # Create the catalogue
        service.create_catalogue(
            data['name'],
            data['description'],
            data['start_date'],
            data['end_date'],
            data.get('active', True)  # Default to active if not specified
        )

        return jsonify({
            'status': 'success',
            'message': 'Catalogue created successfully'
        }), 201
        
    except CatalogueDateExpired as e:
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to create catalogue: {str(e)}'
        }), 500

@app.route('/api/catalogues/<int:catalogue_id>', methods=['PUT'])
def update_catalogue(catalogue_id):
    """Update an existing catalogue"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Update the catalogue
        service.update_catalogue(
            catalogue_id,
            data['name'],
            data['description'],
            data['start_date'],
            data['end_date'],
            data.get('active', True)
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Catalogue updated successfully'
        })
        
    except CatalogueNotFoundError as e:
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 404
    except CatalogueUpdateError as e:
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to update catalogue: {str(e)}'
        }), 500

@app.route('/api/catalogues/<int:catalogue_id>', methods=['DELETE'])
def delete_catalogue(catalogue_id):
    """Delete a catalogue"""
    try:
        service.delete_catalogue(catalogue_id)
        return jsonify({
            'status': 'success',
            'message': 'Catalogue deleted successfully'
        })
    except CatalogueNotFoundError as e:
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 404
    except CatalogueDeleteError as e:
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to delete catalogue: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Resource not found'
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)