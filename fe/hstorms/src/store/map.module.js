import {
    FIND_BY_POINT,
    COUNT_OCC_BY_COUNTRY,
    CLEAR_LAYERS
} from './actions.type';
import {
    ADD_HUR_LAYERS,
    ADD_OCC_LAYERS,
    CLEAR_HUR_LAYERS,
    CLEAR_OCC_LAYERS,
    SET_MARKER
} from './mutations.type';
import {HurricaneService} from '@/common/api.service';

const state = {
    hurricane_layers: [],
    occurrence_layers: [],
    marker: {
        lat: undefined,
        lon: undefined,
        distance: 0
    }
};

const getters = {
    hurricane_layers(state) {
        return state.hurricane_layers;
    },
    occurrence_layers(state) {
        return state.occurrence_layers;
    },
    marker(state) {
        return state.marker
    }
};

const actions = {
    [FIND_BY_POINT]({commit}, params) {
        return HurricaneService.query('point', params)
            .then(response => {
                commit(ADD_HUR_LAYERS, response.data);
            });
    },
    [COUNT_OCC_BY_COUNTRY]({commit}, params) {
        return HurricaneService.query('occurrence', params)
            .then(response => {
                commit(ADD_OCC_LAYERS, response.data);
            });
    },
    [CLEAR_LAYERS]({commit}) {
        commit(CLEAR_HUR_LAYERS);
        commit(CLEAR_OCC_LAYERS);
    }
};

const mutations = {
    [ADD_HUR_LAYERS](state, data) {
        state.hurricane_layers = state.hurricane_layers.concat(data);
    },
    [ADD_OCC_LAYERS](state, data) {
        state.occurrence_layers = state.occurrence_layers.concat(data);
    },
    [CLEAR_HUR_LAYERS](state) {
        state.hurricane_layers = [];
    },
    [CLEAR_OCC_LAYERS](state) {
        state.occurrence_layers = [];
    },
    [SET_MARKER](state, {lat, lon}) {
        state.marker.lat = lat;
        state.marker.lon = lon;
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};