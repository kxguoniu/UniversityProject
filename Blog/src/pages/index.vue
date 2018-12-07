<template>
    <div>
        <div style="width: 100%;min-width: 888px;" :class="{'html-bind':status}">
            <div :class="{'html-header2':true}">
                <el-menu
                    :default-active="'1'"
                    class="heade3"
                    id="searchBar"
                    mode="horizontal"
                    background-color="#0b445b"
                    text-color="#fff"
                    active-text-color="#ffd04b"
                    router
                    >
                    <el-menu-item :index="'/categroay/' + item.id" :key="index" v-for="(item,index) in headers">{{ item.name }}</el-menu-item>
                </el-menu>
            </div>
            <div class="heade2">
                <!--
                <a href="http://www.52pyc.cn/login">
                    后台管理
                </a>
                -->
                <router-link to="/admin">
                    后台管理
                </router-link>
            </div>
        </div>
        <router-view></router-view>
        <div class="footer html-bottom"></div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"index",
        data(){
            return{
                headers:[],
                headers2:[
                    {'id':1, 'name':'首页'},
                    {'id':2, 'name':'Linux'},
                    {'id':3, 'name':'Python'},
                    {'id':4, 'name':'Django'},
                    {'id':5, 'name':'Tornado'},
                    {'id':6, 'name':'Machine'},
                    {'id':7, 'name':'生活'},
                    {'id':8, 'name':'资源分享'},
                ],
                status: true
            }
        },
        mounted(){
            //window.addEventListener('scroll', this.handleScroll)
        },
        created(){
            if (this.GLOBAL.INDEX == 0){
                var counturl = this.HOST + 'countview'
                this.$axios({
                    method: 'post',
                    url: counturl,
                    params:{
                        index: 1
                    }
                })
                .then(res => {
                    console.log('主页加一',res.data.status)
                })
                .catch(error => {
                    console.log(error)
                })
            }
            var url = this.HOST + 'taglist'
            this.$axios.get(url)
            .then(res => {
                this.headers = res.data.data.category;
            })
            .catch(error =>{
                console.log(error);
            })
        },
        methods:{
            // 滑动固定
            handleScroll(){
                var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
                var offsetTop = document.querySelector('#searchBar').offsetTop
                if (scrollTop > offsetTop) {
                    this.status = true
                } else {
                    this.status = false
                }
            }
        },
        computed:{
            onRoutes(){
                console.log('route1',this.$route.path)
                return this.$route.path.replace('/','');
                console.log('route2',this.$route.path)
            }
        },
        destroyed(){
            //window.removeEventListener('scroll', this.handleScroll)
        }
    }
</script>

<style type="text/css" scoped>
    .heade2{
        background-color: #0b445b !important;
        float: left;
        width: 11%;
        margin-bottom: 20px;
        padding-right: 5%;
        text-align: center;
        padding-bottom: 5px;
    }
    .heade2 a{
        font-size: 15px;
        line-height: 55px;
        width: 12.5%;
        text-decoration:none;
        color: #fff;
    }
    .html-header2{
        background-color: #0b445b !important;
        min-width: 600px;
        margin-bottom: 20px;
        width: 79%;
        padding-left: 5%;
        height: 60px;
        z-index: 999;
        float: left;
    }
    .html-header2 li{
        font-size: 15px;
        line-height: 54px;
        width: 12.5%;
        text-align: center;
    }
    .html-header{
        background-color: #0b445b !important;
        min-width: 800px;
        margin-bottom: 20px;
        width: 90%;
        padding: 0 5%;
        z-index: 999;
    }
    .html-bind{
        position: fixed;
        top: 0px;
        z-index: 999;
    }
    .html-header li{
        font-size: 15px;
        line-height: 54px;
        width: 11%;
        text-align: center;
    }
</style>