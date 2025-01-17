import axios from 'axios';

export interface LoginCredentials {
    email: string;
    password: string;
}

export const authService = {
    async login(credentials: LoginCredentials) {
        const response = await axios.post('/api/auth/login', credentials);
        const { access_token } = response.data;
        localStorage.setItem('token', access_token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        return response.data;
    },

    logout() {
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
    },

    getToken() {
        return localStorage.getItem('token');
    },

    isAuthenticated() {
        return !!this.getToken();
    }
}; 