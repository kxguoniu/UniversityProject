// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Axios from 'axios'
import { Icon, Form, FormItem, Input, Select, Option, Col, DatePicker, TimePicker, Switch, Checkbox, CheckboxGroup, Radio, RadioGroup, Button } from 'element-ui'
import VueAwesomeSwiper from 'vue-awesome-swiper'
import 'swiper/dist/css/swiper.css'
import '../static/js/Dynamic_line.js'


Vue.config.productionTip = false
Vue.prototype.$axios  = Axios
Vue.prototype.HOST = './local'
//Vue.prototype.HOST = 'http://123.206.95.123:8080/'

Vue.use(Icon)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Select)
Vue.use(Option)
Vue.use(Col)
Vue.use(DatePicker)
Vue.use(TimePicker)
Vue.use(Switch)
Vue.use(Checkbox)
Vue.use(CheckboxGroup)
Vue.use(Radio)
Vue.use(RadioGroup)
Vue.use(Button)


/* eslint-disable no-new */
let bus = new Vue()
Vue.prototype.bus = bus

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})