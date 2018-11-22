import {FIND_CLOSEST_H} from './actions.type';
import {ADD_GEO_LAYERS, SET_MARKER} from "./mutations.type";
import {HurricaneService} from "@/common/api.service";

const state = {
    geojson_layers: [],
    marker: {
        lat: undefined,
        lon: undefined
    }
};

const getters = {
    geojson_layers(state) {
        return state.geojson_layers;
    },
    marker(state) {
        return state.marker
    }
};

const actions = {
    [FIND_CLOSEST_H]({commit}, params) {
        return HurricaneService.query('point', params)
            .then(response => {
                commit(ADD_GEO_LAYERS, response.data);
            });
    }
};

const mutations = {
    [ADD_GEO_LAYERS](state, data) {
        state.geojson_layers = state.geojson_layers.concat(data);
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