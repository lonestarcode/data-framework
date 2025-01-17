import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const SearchBar: React.FC = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [category, setCategory] = useState('all');
    const navigate = useNavigate();

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        navigate(`/search?q=${searchTerm}&category=${category}`);
    };

    return (
        <form onSubmit={handleSearch} className="search-bar">
            <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search summaries..."
                className="search-input"
            />
            <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="category-select"
            >
                <option value="all">All Categories</option>
                <option value="news">News</option>
                <option value="blogs">Blogs</option>
                <option value="social">Social Media</option>
            </select>
            <button type="submit" className="search-button">
                Search
            </button>
        </form>
    );
}; 