import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/pages/login'
import Index from '@/pages/index'
import BlogList from '@/pages/BlogList'
import BlogDetail from '@/pages/BlogDetail'

Vue.use(Router)

export default new Router({
    mode: 'history',
    linkActiveClass:"active",
    routes: [
        {
            path: '/',
            name: 'Index',
            component: Index,
            redirect: "/categroay/1",
            children:[
                {
                    path: '/categroay/:id',
                    name: 'BlogList',
                    component: BlogList
                },
                {
                    path: '/blogdetail/:id',
                    name: 'BlogDetail',
                    component: BlogDetail
                }
            ]
        }
    ]
})
