from flask import Blueprint, request, jsonify
from src.database.models import Summary, Article
from src.logging.logger import get_logger
from src.auth.middleware import require_auth

logger = get_logger('api.summaries')
summary_bp = Blueprint('summaries', __name__)

@summary_bp.route('/summaries', methods=['GET'])
def get_summaries():
    try:
        category = request.args.get('category')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        query = Summary.query.join(Article)
        if category and category != 'all':
            query = query.filter(Article.source == category)
            
        summaries = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'items': [s.to_dict() for s in summaries.items],
            'total': summaries.total,
            'pages': summaries.pages
        })
    except Exception as e:
        logger.error(f"Error fetching summaries: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch summaries'}), 500

@summary_bp.route('/summaries/search', methods=['GET'])
def search_summaries():
    try:
        query = request.args.get('q', '')
        summaries = Summary.query.filter(
            Summary.summary_text.ilike(f'%{query}%')
        ).all()
        return jsonify([s.to_dict() for s in summaries])
    except Exception as e:
        logger.error(f"Error searching summaries: {str(e)}", exc_info=True)
        return jsonify({'error': 'Search failed'}), 500 