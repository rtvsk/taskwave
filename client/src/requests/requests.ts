import axios from 'axios';

// Create an Axios instance with default configuration
export const api = axios.create({
    baseURL: 'http://localhost:8000',
});
