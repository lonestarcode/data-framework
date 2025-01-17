import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FeedbackForm } from './FeedbackForm';

interface Summary {
    id: number;
    summary_text: string;
    source: string;
    keywords: string[];
    url: string;
}

export const SummaryList: React.FC = () => {
    const [summaries, setSummaries] = useState<Summary[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSummaries = async () => {
            try {
                const response = await axios.get('/api/summaries');
                setSummaries(response.data);
            } catch (error) {
                console.error('Error fetching summaries:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchSummaries();
    }, []);

    return (
        <div className="summary-list">
            {loading ? (
                <div>Loading summaries...</div>
            ) : (
                summaries.map(summary => (
                    <div key={summary.id} className="summary-card">
                        <h3>Source: {summary.source}</h3>
                        <p>{summary.summary_text}</p>
                        <div className="keywords">
                            {summary.keywords.map(keyword => (
                                <span key={keyword} className="keyword-tag">
                                    {keyword}
                                </span>
                            ))}
                        </div>
                        <a href={summary.url} target="_blank" rel="noopener noreferrer">
                            Read original article
                        </a>
                        <FeedbackForm summaryId={summary.id} />
                    </div>
                ))
            )}
        </div>
    );
}; 
import axios from 'axios';
import { FeedbackForm } from './FeedbackForm';

interface Summary {
    id: number;
    summary_text: string;
    source: string;
    keywords: string[];
    url: string;
}

export const SummaryList: React.FC = () => {
    const [summaries, setSummaries] = useState<Summary[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSummaries = async () => {
            try {
                const response = await axios.get('/api/summaries');
                setSummaries(response.data);
            } catch (error) {
                console.error('Error fetching summaries:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchSummaries();
    }, []);

    return (
        <div className="summary-list">
            {loading ? (
                <div>Loading summaries...</div>
            ) : (
                summaries.map(summary => (
                    <div key={summary.id} className="summary-card">
                        <h3>Source: {summary.source}</h3>
                        <p>{summary.summary_text}</p>
                        <div className="keywords">
                            {summary.keywords.map(keyword => (
                                <span key={keyword} className="keyword-tag">
                                    {keyword}
                                </span>
                            ))}
                        </div>
                        <a href={summary.url} target="_blank" rel="noopener noreferrer">
                            Read original article
                        </a>
                        <FeedbackForm summaryId={summary.id} />
                    </div>
                ))
            )}
        </div>
    );
};