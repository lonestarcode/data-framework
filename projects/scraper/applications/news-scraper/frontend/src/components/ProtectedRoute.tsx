import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { authService } from '../services/auth';

interface ProtectedRouteProps {
    element: React.ReactElement;
    requiredRole?: string;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
    element,
    requiredRole
}) => {
    if (!authService.isAuthenticated()) {
        return <Navigate to="/login" replace />;
    }

    if (requiredRole) {
        const token = authService.getToken();
        const payload = JSON.parse(atob(token!.split('.')[1]));
        if (payload.role !== requiredRole) {
            return <Navigate to="/unauthorized" replace />;
        }
    }

    return element;
}; 