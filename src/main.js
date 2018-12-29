// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import Axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueAwesomeSwiper from 'vue-awesome-swiper'
import 'swiper/dist/css/swiper.css'
import App from './App'
import '../static/js/Dynamic_line.js'
import _global from './Global'

Vue.config.productionTip = false
Vue.prototype.$axios  = Axios
//Vue.prototype.HOST = './local'
//Vue.prototype.HOST = './server'
Vue.prototype.HOST = '/'
Vue.prototype.GLOBAL = _global
Vue.use(ElementUI)


// 添加请求拦截器
Axios.interceptors.request.use(function(config){
    // 在发送之前做些什么
    if(config.method === "post" || config.method === "put" || config.method === "delete"){
        var pattern = /(.+; *)?_xsrf *= *([^;" ]+)/;
        var xsrf = pattern.exec(document.cookie)
        if (xsrf) {
            config.headers['X-Xsrftoken'] = xsrf[2]
        }
    }
    console.log('cookie',document.cookie)
    return config;
}, function(error) {
    // 对请求错误做些什么
    return Promise.reject(error)
});



/* eslint-disable no-new */
let bus = new Vue()
Vue.prototype.bus = bus

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
