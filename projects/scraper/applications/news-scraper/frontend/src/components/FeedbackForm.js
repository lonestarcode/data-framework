import React, { useState } from 'react';
import axios from 'axios';

const FeedbackForm = ({ summaryId }) => {
    const [feedback, setFeedback] = useState({
        type: '',
        comment: ''
    });

    const handleDownvote = async () => {
        try {
            await axios.post('/api/feedback', {
                summary_id: summaryId,
                feedback_type: 'downvote',
                comment: feedback.comment
            });
            // Handle success (e.g., hide summary, show confirmation)
        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    };

    const feedbackCategories = [
        'Irrelevant Content',
        'Poor Summary',
        'Incorrect Source',
        'Other'
    ];

    return (
        <div className="feedback-form">
            <button 
                onClick={handleDownvote}
                className="downvote-button"
            >
                Downvote
            </button>
            
            <select 
                value={feedback.type}
                onChange={(e) => setFeedback({...feedback, type: e.target.value})}
            >
                <option value="">Select Feedback Type</option>
                {feedbackCategories.map(category => (
                    <option key={category} value={category}>
                        {category}
                    </option>
                ))}
            </select>
            
            <textarea
                placeholder="Additional comments..."
                value={feedback.comment}
                onChange={(e) => setFeedback({...feedback, comment: e.target.value})}
            />
        </div>
    );
};

export default FeedbackForm;
