from flask import Blueprint, request, jsonify
from src.pipeline.feedback_handler import FeedbackHandler
from src.logging.logger import get_logger
from src.monitoring.metrics import DOWNVOTES, FEEDBACK_CATEGORIES

logger = get_logger('api.feedback')
feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    try:
        feedback_data = request.get_json()
        handler = FeedbackHandler(db.session)
        result = handler.handle_feedback(
            summary_id=feedback_data['summary_id'],
            feedback_type=feedback_data['feedback_type'],
            comment=feedback_data.get('comment')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to submit feedback'}), 500 