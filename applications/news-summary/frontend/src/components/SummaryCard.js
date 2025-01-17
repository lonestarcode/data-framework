import React from 'react';
import FeedbackForm from './FeedbackForm';

const SummaryCard = ({ summary }) => {
    return (
        <div className="summary-card">
            <div className="summary-header">
                <h3>{summary.title}</h3>
                <span className="source-tag">{summary.source}</span>
            </div>
            <p className="summary-text">{summary.summary_text}</p>
            <div className="keywords">
                {summary.keywords.map(keyword => (
                    <span key={keyword} className="keyword-tag">
                        {keyword}
                    </span>
                ))}
            </div>
            <div className="summary-footer">
                <a 
                    href={summary.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="source-link"
                >
                    Read Original
                </a>
                <FeedbackForm summaryId={summary.id} />
            </div>
        </div>
    );
};

export default SummaryCard;
