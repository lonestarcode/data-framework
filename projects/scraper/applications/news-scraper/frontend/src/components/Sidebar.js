import React from 'react';
import { useNavigate } from 'react-router-dom';

const Sidebar = () => {
    const navigate = useNavigate();
    
    const categories = [
        { name: 'All', value: 'all' },
        { name: 'News', value: 'news' },
        { name: 'Blogs', value: 'blogs' },
        { name: 'Social Media', value: 'social' }
    ];

    const handleCategoryClick = (category) => {
        navigate(`/?category=${category}`);
    };

    return (
        <div className="sidebar">
            <h3>Categories</h3>
            <ul className="category-list">
                {categories.map(category => (
                    <li 
                        key={category.value}
                        onClick={() => handleCategoryClick(category.value)}
                        className="category-item"
                    >
                        {category.name}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Sidebar;
