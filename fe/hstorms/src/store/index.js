import Vue from 'vue';
import Vuex from 'vuex';

import hurricane from './hurricane.module';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    hurricane
  }
});