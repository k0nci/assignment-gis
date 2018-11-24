import Vue from 'vue';
import Vuex from 'vuex';

import map from './map.module';

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        map
    }
});