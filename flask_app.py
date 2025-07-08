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
from backend.services.authentication_service import AuthenticationService
import os
import logging

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)
app.config['JSON_SORT_KEYS'] = False 

service = CatalogueService()
auth_service = AuthenticationService()

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/catalogue.log"),
        logging.StreamHandler() 
    ]
)
@app.route('/')
def home():
    logging.info("Serving login page")
    return send_from_directory('frontend', 'login.html')

@app.route('/catalogue.html')
def catalogue_page():
    logging.info("Serving catalogue page")
    return send_from_directory('frontend', 'catalogue.html')

@app.route('/login', methods=['POST'])
def login():
    logging.info("Login attempt received")
    if not request.is_json:
        logging.warning("Login failed: Invalid content-type")
        return jsonify({
            'status': 'error',
            'message': 'Error to login'
        }), 415
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logging.warning("Login failed: Missing credentials")
            return jsonify({'status': 'error', 'message': 'Username and password required'}), 400

        if auth_service.login(username, password):
            logging.info(f"Login successful for user: {username}")
            return jsonify({'status': 'success', 'message': 'Login successful'}), 200
        else:
            logging.warning(f"Login failed: Invalid credentials for user: {username}")
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

    except Exception as e:
        logging.error(f"Login failed: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Login failed: {str(e)}'}), 500

@app.route('/api/catalogues', methods=['GET'])
def get_all_catalogues():
    logging.info("Fetching all catalogues")
    try:
        catalogues = service.get_all_catalogue_json()
        logging.info(f"Fetched {len(catalogues)} catalogues")
        return jsonify({
            'status': 'success',
            'data': catalogues,
            'count': len(catalogues)
        })
    except DatabaseConnectorError as e:
        logging.error(f"DatabaseConnectorError: {str(e)}")
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 500
    except Exception as e:
        logging.error(f"Failed to fetch catalogues: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch catalogues: {str(e)}'
        }), 500

@app.route('/api/catalogues/<int:catalogue_id>', methods=['GET'])
def get_catalogue(catalogue_id):
    logging.info(f"Fetching catalogue with ID: {catalogue_id}")
    try:
        catalogue = service.get_catalogue_json(catalogue_id)
        logging.info(f"Fetched catalogue: {catalogue}")
        return jsonify({
            'status': 'success',
            'data': catalogue
        })
    except CatalogueNotFoundError as e:
        logging.warning(f"Catalogue not found: {str(e)}")
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 404
    except Exception as e:
        logging.error(f"Failed to fetch catalogue: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch catalogue: {str(e)}'
        }), 500

@app.route('/api/catalogues', methods=['POST'])
def create_catalogue():
    logging.info("Create catalogue request received")
    try:
        data = request.get_json()
        logging.debug(f"Create catalogue data: {data}")
        required_fields = ['name', 'description', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                msg = f"Missing required field: {field}"
                logging.warning(msg)
                return jsonify({
                    'status': 'error',
                    'message': msg
                }), 400

        if not isinstance(data['name'], str) or data['name'].strip() == '' or data['name'].isdigit():
            logging.warning("Invalid name")
            return jsonify({
                'status': 'error',
                'message': 'Catalogue name must be a non-empty string and not all digits.'
            }), 400

        if not isinstance(data['description'], str) or data['description'].strip() == '' or data['description'].isdigit():
            logging.warning("Invalid description")
            return jsonify({
                'status': 'error',
                'message': 'Catalogue description must be a non-empty string and not all digits.'
            }), 400

        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            if end_date < start_date:
                logging.warning("End date is before start date")
                return jsonify({
                    'status': 'error',
                    'message': 'End date must not be before start date.'
                }), 400
        
        except Exception:
            logging.warning("Invalid date format")
            return jsonify({
                'status': 'error',
                'message': 'Invalid date format. Use YYYY-MM-DD.'
            }), 400

        new_id=service.create_catalogue(
            data['name'],
            data['description'],
            data['start_date'],
            data['end_date'],
            data.get('active', True)
        )
        logging.info(f"Catalogue  created successfully. ID={new_id}")
        return jsonify({
            'status': 'success',
            'message': 'Catalogue created successfully',
            'data': {
                'ID' : new_id,
                'name': data['name'],
                'description': data['description'],
                'start_date': data['start_date'],
                'end_date': data['end_date'],
                'active': data.get('active', True)}
        }), 201
    
    except CatalogueDateExpired as e:
        logging.warning(f"CatalogueDateExpired: {str(e)}")
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 400
    
    except Exception as e:
        logging.error(f"Failed to create catalogue: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to create catalogue: {str(e)}'
        }), 500

@app.route('/api/catalogues/<int:catalogue_id>', methods=['PUT'])
def update_catalogue(catalogue_id):
    logging.info(f"Update request for catalogue ID {catalogue_id}")
    try:
        data = request.get_json()
        logging.debug(f"Update data: {data}")
        required_fields = ['name', 'description', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                msg = f"Missing required field: {field}"
                logging.warning(msg)
                return jsonify({
                    'status': 'error',
                    'message': msg
                }), 400

        if not isinstance(data['name'], str) or data['name'].strip() == '' or data['name'].isdigit():
            logging.warning("Invalid name")
            return jsonify({
                'status': 'error',
                'message': 'Catalogue name must be a non-empty string and not all digits.'
            }), 400

        if not isinstance(data['description'], str) or data['description'].strip() == '' or data['description'].isdigit():
            logging.warning("Invalid description")
            return jsonify({
                'status': 'error',
                'message': 'Catalogue description must be a non-empty string and not all digits.'
            }), 400

        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            if end_date < start_date:
                logging.warning("End date is before start date")
                return jsonify({
                    'status': 'error',
                    'message': 'End date must not be before start date.'
                }), 400
        except Exception:
            logging.warning("Invalid date format")
            return jsonify({
                'status': 'error',
                'message': 'Invalid date format. Use YYYY-MM-DD.'
            }), 400

        service.update_catalogue(
            catalogue_id,
            data['name'],
            data['description'],
            data['start_date'],
            data['end_date'],
            data.get('active', True)
        )
        logging.info(f"Catalogue ID {catalogue_id} updated successfully")
        return jsonify({
            'status': 'success',
            'message': 'Catalogue updated successfully'
        })
    except CatalogueNotFoundError as e:
        logging.warning(f"CatalogueNotFoundError: {str(e)}")
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 404
    except CatalogueUpdateError as e:
        logging.warning(f"CatalogueUpdateError: {str(e)}")
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 400
    except Exception as e:
        logging.error(f"Failed to update catalogue: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to update catalogue: {str(e)}'
        }), 500

@app.route('/api/catalogues/<int:catalogue_id>', methods=['DELETE'])
def delete_catalogue(catalogue_id):
    logging.info(f"Delete request for catalogue ID {catalogue_id}")
    try:
        service.delete_catalogue(catalogue_id)
        logging.info(f"Catalogue ID {catalogue_id} deleted successfully")
        return jsonify({
            'status': 'success',
            'message': 'Catalogue deleted successfully'
        })
    except CatalogueNotFoundError as e:
        logging.warning(f"CatalogueNotFoundError: {str(e)}")
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 404
    except CatalogueDeleteError as e:
        logging.warning(f"CatalogueDeleteError: {str(e)}")
        return jsonify({
            'status': 'error',
            'error_code': e.error_code,
            'message': str(e)
        }), 400
    except Exception as e:
        logging.error(f"Failed to delete catalogue: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to delete catalogue: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    logging.warning("404 Error encountered")
    return jsonify({
        'status': 'error',
        'message': 'Catalogue Not found this id .Please Exist valid id'
    }), 404

@app.errorhandler(500)
def server_error(error):
    logging.error(f"500 Error encountered: {error}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    logging.info("Starting Flask app")
    app.run(debug=True, host='0.0.0.0', port=5000)
