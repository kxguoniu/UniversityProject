import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/pages/index'
import BlogList from '@/pages/BlogList'
import BlogDetail from '@/pages/BlogDetail'

import Home from '@/components/common/Home.vue'
import Dashboard from '@/components/page/Dashboard.vue'
import BaseTable from '@/components/page/BaseTable.vue'
import Tabs from '@/components/page/Tabs.vue'
import Monitor from '@/components/page/monitor.vue'
import Create from '@/components/page/Create.vue'
import Edit from '@/components/page/Edit.vue'
import Login from '@/components/page/Login.vue'

Vue.use(Router)

export default new Router({
    //mode: 'history',
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
                },
            ]
        },
        {
            path: '/login',
            name: 'Login',
            component: Login,
        },
        {
            path: '/admin',
            name: 'Admin',
            component: Home,
            redirect: "/admin/dashboard",
            children:[
                {
                    path: '/admin/dashboard',
                    name: 'Dashboard',
                    component: Dashboard,
                    meta: { title: '系统首页', needlogin: true }
                },
                {
                    path: '/admin/table',
                    name: 'BaseTable',
                    component: BaseTable,
                    meta: { title: '博文列表', needlogin: true }
                },
                {
                    path: '/admin/message',
                    name: 'Tabs',
                    component: Tabs,
                    meta: { title: '系统消息', needlogin: true }
                },
                {
                    path: '/admin/monitor',
                    name: 'Monitor',
                    component: Monitor,
                    meta: { title: 'monitor', needlogin: true }
                },
                {
                    path: '/admin/markdown',
                    name: 'Create',
                    component: Create,
                    meta: { title: '创作博文', needlogin: true }
                },
                {
                    path: '/admin/edit/:id',
                    name: 'Edit',
                    component: Edit,
                    meta: { title: '编辑博文', needlogin: true }
                },
            ]
        }
    ]
})