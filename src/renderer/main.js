import Vue from 'vue'
import axios from 'axios'
import ElementUI from 'element-ui';
import '@/assets/css/layout.scss'
import '@/assets/css/reset.scss'
import App from './App'
import router from './router'
import store from './store'
// require('./mock.js')
if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.use(ElementUI);

/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app')
