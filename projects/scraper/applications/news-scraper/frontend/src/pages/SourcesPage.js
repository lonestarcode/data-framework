import React, { useState, useEffect } from 'react';
import { SourceManager } from '../components/SourceManager';
import axios from 'axios';

const SourcesPage = () => {
    const [sources, setSources] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSources = async () => {
            try {
                const response = await axios.get('/api/sources');
                setSources(response.data);
            } catch (error) {
                console.error('Error fetching sources:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchSources();
    }, []);

    return (
        <div className="sources-page">
            <h1>Manage News Sources</h1>
            <SourceManager />
            
            <div className="sources-list">
                <h2>Current Sources</h2>
                {loading ? (
                    <p>Loading sources...</p>
                ) : (
                    sources.map(source => (
                        <div key={source.id} className="source-item">
                            <h3>{source.name}</h3>
                            <p>Type: {source.type}</p>
                            <p>Update Interval: {source.interval}</p>
                            <a href={source.url} target="_blank" rel="noopener noreferrer">
                                {source.url}
                            </a>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default SourcesPage;
