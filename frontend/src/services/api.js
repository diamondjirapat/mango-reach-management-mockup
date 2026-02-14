import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export default {
    getAds() {
        return apiClient.get('/ads');
    },
    getDashboardStats() {
        return apiClient.get('/dashboard');
    },
    createAd(ad) {
        return apiClient.post('/ads', ad);
    }
};
