import axios from 'axios';

// Create an Axios instance with default configuration
export const api = axios.create({
    // baseURL: 'http://127.0.0.1:8000',
    baseURL: 'https://taskwave.ru',
});
