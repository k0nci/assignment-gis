import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import {API_URL} from '@/common/config';

const ApiService = {
    init() {
        Vue.use(VueAxios, axios);
        Vue.axios.defaults.baseURL = API_URL;
    },

    get(resource, slug = '') {
        return Vue.axios.get(`${resource}/${slug}`).catch(error => {
            throw new Error(`[RWV] ApiService ${error}`);
        });
    },

    query(resource, params) {
        return Vue.axios.get(resource, params).catch(error => {
            throw new Error(`[RWV] ApiService ${error}`);
        });
    }
};

export const HurricaneService = {
    query(type, params) {
        return ApiService.query(`hurricanes/${type}`, {
            params: params
        });
    }
};

export const CountryService = {
    get(slug = '') {
        return ApiService.get('countries', slug);
    }
};

export default ApiService;
