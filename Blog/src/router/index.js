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
import Line from '@/components/page/Line.vue'
import Icon from '@/components/page/Icon.vue'
import Form from '@/components/page/BaseForm.vue'
import Upload from '@/components/page/Upload.vue'
import Charts from '@/components/page/BaseCharts.vue'
import Drag from '@/components/page/DragList.vue'
import Permission from '@/components/page/Permission.vue'
import NotFount from '@/components/page/404.vue'
import Errors from '@/components/page/403.vue'

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
                {
                    path: '/admin/line',
                    name: 'Line',
                    component: Line,
                    meta: { title: 'line' }
                },
                {
                    path: '/admin/icon',
                    name: 'Icon',
                    component: Icon,
                    meta: { title: '自定义图标' }
                },
                {
                    path: '/admin/form',
                    name: 'Form',
                    component: Form,
                    meta: { title: '基本表单' }
                },
                {
                    path: '/admin/upload',
                    name: 'Upload',
                    component: Upload,
                    meta: { title: '文件上传' }
                },
                {
                    path: '/admin/charts',
                    name: 'Charts',
                    component: Charts,
                    meta: { title: 'schart图表' }
                },
                {
                    path: '/admin/drag',
                    name: 'Drag',
                    component: Drag,
                    meta: { title: '拖拽列表' }
                },
                {
                    path: '/admin/permission',
                    name: 'Permission',
                    component: Permission,
                    meta: { title: '权限测试', permission: true }
                },
                {
                    path: '/admin/404',
                    name: 'NotFount',
                    component: NotFount,
                    meta: { title: '404' }
                },
                {
                    path: '/admin/403',
                    name: 'Errors',
                    component: Errors,
                    meta: { title: '403' }
                }
            ]
        },
        {
            path: '*',
            redirect: '/admin/404'
        }
    ]
})