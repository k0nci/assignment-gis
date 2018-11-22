import BootstrapVue from 'bootstrap-vue'
import {L} from 'vue2-leaflet';
import App from './App.vue'
import ApiService from "@/common/api.service";
import store from './store'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

Vue.use(BootstrapVue);
Vue.config.productionTip = false;

ApiService.init();

new Vue({
    store,
    render: h => h(App),
}).$mount('#app');
