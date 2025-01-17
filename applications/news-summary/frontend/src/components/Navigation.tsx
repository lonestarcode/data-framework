import React from 'react';
import { Link } from 'react-router-dom';
import { authService } from '../services/auth';

export const Navigation: React.FC = () => {
    const isAuthenticated = authService.isAuthenticated();

    return (
        <nav className="navigation">
            <Link to="/" className="nav-link">Home</Link>
            {isAuthenticated && (
                <Link to="/sources" className="nav-link">Manage Sources</Link>
            )}
            {!isAuthenticated ? (
                <Link to="/login" className="nav-link">Login</Link>
            ) : (
                <button 
                    onClick={() => authService.logout()}
                    className="nav-link"
                >
                    Logout
                </button>
            )}
        </nav>
    );
}; 