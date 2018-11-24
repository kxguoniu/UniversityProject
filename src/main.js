// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueAwesomeSwiper from 'vue-awesome-swiper'
import 'swiper/dist/css/swiper.css'
import '../static/js/Dynamic_line.js'


Vue.config.productionTip = false
Vue.prototype.$axios  = Axios
Vue.prototype.HOST = './local'
//Vue.prototype.HOST = 'http://123.206.95.123:8080/'

Vue.use(ElementUI)


/* eslint-disable no-new */
let bus = new Vue()
Vue.prototype.bus = bus

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
