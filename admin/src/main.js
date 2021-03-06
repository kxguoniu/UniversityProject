import Vue from 'vue'
import App from './App'
import router from './router'
import Axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'    // 默认主题
// import '../static/css/theme-green/index.css';       // 浅绿色主题
import '../static/css/icon.css'
//import 'mavon-editor/dist/css/index.css'
import "babel-polyfill"


Vue.use(ElementUI, { size: 'small' });
Vue.prototype.$axios = Axios;
Vue.prototype.HOST = './local'
//Vue.prototype.HOST = './server'
//Vue.prototype.HOST = '/'


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

/*
// 添加响应拦截器
Axios.interceptors.response.use(function(response){
    // 对相应数据做些什么
    if(response.status !== 200){
        return response
    }
    return response
}, function(error){
    // 对相应错误做些什么
    return Promise.reject(error);
});
*/

//使用钩子函数对路由进行权限跳转
/*
router.beforeEach((to, from, next) => {
    const role = localStorage.getItem('ms_username');
    if(!role && to.path !== '/login'){
        next('/login');
    }else if(to.meta.permission){
        // 如果是管理员权限则可进入，这里只是简单的模拟管理员权限而已
        role === 'admin' ? next() : next('/403');
    }else{
        // 简单的判断IE10及以下不进入富文本编辑器，该组件不兼容
        if(navigator.userAgent.indexOf('MSIE') > -1 && to.path === '/editor'){
            Vue.prototype.$alert('vue-quill-editor组件不兼容IE10及以下浏览器，请使用更高版本的浏览器查看', '浏览器不兼容通知', {
                confirmButtonText: '确定'
            });
        }else{
            next();
        }
    }
})
*/
new Vue({
    router,
    render: h => h(App)
}).$mount('#app');