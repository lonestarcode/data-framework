from src.database.models import UserFeedback, Summary
from src.monitoring.metrics import DOWNVOTES, FEEDBACK_CATEGORIES
from src.logging.logger import get_logger, log_execution_time
from sqlalchemy.orm import Session
from typing import Dict

logger = get_logger('feedback')

class FeedbackHandler:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.logger = logger

    @log_execution_time(logger)
    def handle_feedback(self, summary_id: int, feedback_type: str, comment: str = None) -> Dict:
        try:
            # Verify summary exists
            summary = self.db.query(Summary).filter(Summary.id == summary_id).first()
            if not summary:
                raise ValueError(f"Summary {summary_id} not found")

            # Create feedback record
            feedback = UserFeedback(
                summary_id=summary_id,
                feedback_type=feedback_type,
                comment=comment
            )
            
            # Update metrics
            if feedback_type == 'downvote':
                DOWNVOTES.inc()
            FEEDBACK_CATEGORIES.labels(category=feedback_type).inc()

            self.db.add(feedback)
            self.db.commit()

            self.logger.info(
                f"Feedback recorded for summary {summary_id}",
                extra={
                    "summary_id": summary_id,
                    "feedback_type": feedback_type
                }
            )

            return {"status": "success", "feedback_id": feedback.id}

        except Exception as e:
            self.db.rollback()
            self.logger.error(
                f"Error handling feedback: {str(e)}",
                extra={
                    "summary_id": summary_id,
                    "feedback_type": feedback_type,
                    "error": str(e)
                },
                exc_info=True
            )
            raise
