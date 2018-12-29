import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

function loadIndex(view){
    return () => import(/* webpackChunkName: "view-[request]" */ `@/pages/${view}.vue`)
}

function loadHome(view){
    return () => import(/* webpackChunkName: "view-[request]" */ `@/components/common/${view}.vue`)
}

function loadview(view){
    return () => import(/* webpackChunkName: "view-[request]" */ `@/components/page/${view}.vue`)
}

export default new Router({
    mode: 'history',
    linkActiveClass:"active",
    routes: [
        {
            path: '/',
            name: 'Index',
            component: loadIndex('Index'),
            redirect: "/blog/1",
            children:[
                {
                    path: '/blog/:id',
                    name: 'BlogList',
                    component: loadIndex('BlogList')
                },
                {
                    path: '/blogdetail/:id',
                    name: 'BlogDetail',
                    component: loadIndex('BlogDetail')
                },
            ]
        },
        {
            path: '/login',
            name: 'Login',
            component: loadview('Login'),
        },
        {
            path: '/admin',
            name: 'Admin',
            component: loadHome('Home'),
            redirect: "/dashboard",
            children:[
                {
                    path: '/dashboard',
                    name: 'Dashboard',
                    component: loadview('Dashboard'),
                    meta: { title: '系统首页', needlogin: true }
                },
                {
                    path: '/table',
                    name: 'BaseTable',
                    component: loadview('BaseTable'),
                    meta: { title: '博文列表', needlogin: true }
                },
                {
                    path: '/message',
                    name: 'Tabs',
                    component: loadview('Tabs'),
                    meta: { title: '系统消息', needlogin: true }
                },
                {
                    path: '/monitor',
                    name: 'Monitor',
                    component: loadview('Monitor'),
                    meta: { title: 'monitor', needlogin: true }
                },
                {
                    path: '/markdown',
                    name: 'Create',
                    component: loadview('Create'),
                    meta: { title: '创作博文', needlogin: true }
                },
                {
                    path: '/edit/:id',
                    name: 'Edit',
                    component: loadview('Edit'),
                    meta: { title: '编辑博文', needlogin: true }
                },
                {
                    path: '/line',
                    name: 'Line',
                    component: loadview('Line'),
                    meta: { title: 'line' }
                },
                {
                    path: '/icon',
                    name: 'Icon',
                    component: loadview('Icon'),
                    meta: { title: '自定义图标' }
                },
                {
                    path: '/form',
                    name: 'Form',
                    component: loadview('BaseForm'),
                    meta: { title: '基本表单' }
                },
                {
                    path: '/upload',
                    name: 'Upload',
                    component: loadview('Upload'),
                    meta: { title: '文件上传' }
                },
                {
                    path: '/charts',
                    name: 'Charts',
                    component: loadview('BaseCharts'),
                    meta: { title: 'schart图表' }
                },
                {
                    path: '/drag',
                    name: 'Drag',
                    component: loadview('DragList'),
                    meta: { title: '拖拽列表' }
                },
                {
                    path: '/permission',
                    name: 'Permission',
                    component: loadview('Permission'),
                    meta: { title: '权限测试', permission: true }
                },
                {
                    path: '/403',
                    name: 'Errors',
                    component: loadview('403'),
                    meta: { title: '403' }
                }
            ]
        },
        {
            path: '/404',
            name: 'NotFount',
            component: loadIndex('404'),
            meta: { title: '404' }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
})