from flask import Blueprint, request, jsonify
from src.api.source_manager import SourceManager
from src.logging.logger import get_logger
from src.auth.middleware import require_auth
from src.database.models import UserRole

logger = get_logger('api.sources')
source_bp = Blueprint('sources', __name__)

@source_bp.route('/sources', methods=['GET'])
def get_sources():
    try:
        source_type = request.args.get('type')
        sources = SourceManager.get_sources(source_type)
        return jsonify(sources)
    except Exception as e:
        logger.error(f"Error fetching sources: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch sources'}), 500

@source_bp.route('/sources', methods=['POST'])
@require_auth([UserRole.ADMIN, UserRole.EDITOR])
def add_source():
    try:
        source_data = request.get_json()
        result = SourceManager.add_source(source_data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error adding source: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to add source'}), 500 