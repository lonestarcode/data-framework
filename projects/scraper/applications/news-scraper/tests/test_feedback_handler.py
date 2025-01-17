import pytest
from src.pipeline.feedback_handler import FeedbackHandler
from src.database.models import Summary, UserFeedback

class TestFeedbackHandler:
    @pytest.fixture
    def handler(self, db_session):
        return FeedbackHandler(db_session)

    def test_handle_feedback(self, handler, db_session):
        # Create test summary
        summary = Summary(
            summary_text="Test summary",
            model_used="test-model"
        )
        db_session.add(summary)
        db_session.commit()

        result = handler.handle_feedback(
            summary_id=summary.id,
            feedback_type="downvote",
            comment="Test feedback"
        )

        assert result["status"] == "success"
        feedback = db_session.query(UserFeedback).first()
        assert feedback.summary_id == summary.id
        assert feedback.feedback_type == "downvote"
