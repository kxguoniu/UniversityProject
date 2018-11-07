import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/pages/login'
import Index from '@/pages/index'
import BlogPage from '@/pages/BlogPage'

Vue.use(Router)

export default new Router({
  linkActiveClass:"active",
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      redirect:"/categroay/1",
      children:[
        {
          path: '/categroay/:id',
          name: 'BlogPage',
          component: BlogPage
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
  ]
})
