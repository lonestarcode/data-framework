import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navigation } from './components/Navigation';
import HomePage from './pages/HomePage';
import SourcesPage from './pages/SourcesPage';
import { ProtectedRoute } from './components/ProtectedRoute';

const App = () => {
    return (
        <Router>
            <div className="app">
                <Navigation />
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route 
                        path="/sources" 
                        element={
                            <ProtectedRoute>
                                <SourcesPage />
                            </ProtectedRoute>
                        } 
                    />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
