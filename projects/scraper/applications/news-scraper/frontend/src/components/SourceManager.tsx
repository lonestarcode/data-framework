import React, { useState } from 'react';
import axios from 'axios';

interface SourceForm {
    name: string;
    url: string;
    type: string;
    interval: string;
}

export const SourceManager: React.FC = () => {
    const [sourceForm, setSourceForm] = useState<SourceForm>({
        name: '',
        url: '',
        type: 'news',
        interval: '1h'
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await axios.post('/api/sources', sourceForm);
            setSourceForm({
                name: '',
                url: '',
                type: 'news',
                interval: '1h'
            });
            // Show success message
        } catch (error) {
            console.error('Error adding source:', error);
            // Show error message
        }
    };

    return (
        <div className="source-manager">
            <h2>Add New Source</h2>
            <form onSubmit={handleSubmit} className="source-form">
                <input
                    type="text"
                    value={sourceForm.name}
                    onChange={(e) => setSourceForm({...sourceForm, name: e.target.value})}
                    placeholder="Source Name"
                    required
                />
                <input
                    type="url"
                    value={sourceForm.url}
                    onChange={(e) => setSourceForm({...sourceForm, url: e.target.value})}
                    placeholder="Source URL"
                    required
                />
                <select
                    value={sourceForm.type}
                    onChange={(e) => setSourceForm({...sourceForm, type: e.target.value})}
                >
                    <option value="news">News</option>
                    <option value="blog">Blog</option>
                    <option value="social">Social Media</option>
                </select>
                <select
                    value={sourceForm.interval}
                    onChange={(e) => setSourceForm({...sourceForm, interval: e.target.value})}
                >
                    <option value="1h">Every Hour</option>
                    <option value="6h">Every 6 Hours</option>
                    <option value="12h">Every 12 Hours</option>
                    <option value="24h">Daily</option>
                </select>
                <button type="submit">Add Source</button>
            </form>
        </div>
    );
}; 