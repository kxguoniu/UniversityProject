// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Axios from 'axios'
import ElementUI from 'element-ui'
import VueAwesomeSwiper from 'vue-awesome-swiper'
import "babel-polyfill"
import _global from './Global'
import 'element-ui/lib/theme-chalk/index.css'
//import '../static/js/Dynamic_line.js'
import 'swiper/dist/css/swiper.css'
import '../static/css/icon.css'


Vue.config.productionTip = false
Vue.prototype.$axios  = Axios
//Vue.prototype.HOST = './local'
//Vue.prototype.HOST = './server/api/'
Vue.prototype.HOST = '/api/'
Vue.prototype.GLOBAL = _global
Vue.use(ElementUI, { size: 'small' })


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
    //console.log('cookie',document.cookie)
    return config;
}, function(error) {
    // 对请求错误做些什么
    return Promise.reject(error)
});


// 添加响应拦截器
Axios.interceptors.response.use(function(response){
    // 对相应数据做些什么
    if(response.data.status == 1001){
        router.push({
            path: '/login',
            query: {redirect: location.hostname}
        })
    }
    return response
}, function(error){
    // 对相应错误做些什么
    return Promise.reject(error);
});

router.beforeEach((to, from, next) => {
    to.matched.some((route) =>{
        if (route.meta.needlogin) {
            console.log(localStorage)
            if (localStorage.getItem('nkx_username')) {
                next()
            } else {
                next({ name: 'Login', params: { path: route.path } })
                //next({ path: "/login", query: {redirect: location.host} })
            }
        } else {
            next()
        }
    });
});

let bus = new Vue()
Vue.prototype.bus = bus

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
