<template>
    <div class="appbody">
        <div style="width: 100%;" :class="{'html-bind':status}">
            <div v-if="width >= 800" :class="{'html-header2':true}">
                <el-menu
                    :default-active="'1'"
                    id="searchBar"
                    mode="horizontal"
                    background-color="#0b445b"
                    text-color="#fff"
                    active-text-color="#ffd04b"
                    router
                    >
                    <el-menu-item id="menuindex" :index="'/blog/' + item.id" :key="index" v-for="(item,index) in headers">{{ item.name }}</el-menu-item>
                </el-menu>
            </div>
            <div v-if="width >= 800" class="heade2">
                <router-link id="houtai" to="/admin">
                    后台管理
                </router-link>
            </div>
            <div v-else class="containernk">
                <button type="button" class="navbar-button" @click="menuClick">
                    <i class="el-icon-menu" style="color: #0b445b; font-size: 28px"></i>
                </button>
                <div style="clear: both;"></div>
                <div v-show="menustatus">
                    <ul>
                        <li :key="indexs" :class="classMenu(items.id)" v-for="(items,indexs) in headers2" @click="menuPush(items.id)">{{ items.name }}</li>
                    </ul>
                </div>
            </div>
        </div>
        <router-view></router-view>
        <Footer></Footer>
    </div>
</template>

<script type="text/javascript">
    import Footer from '../components/Footer'
    export default{
        name:"index",
        components:{
            Footer
        },
        data(){
            return{
                width: window.innerWidth,
                menustatus: false,
                activestatus: 1,
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
            window.addEventListener("resize", this.changeWidth)
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
            // 导航变更
            changeWidth(){
                this.width = window.innerWidth
            },
            // 按钮
            menuClick(){
                this.menustatus = !this.menustatus
            },
            // 导航跳转
            menuPush(val){
                var urls = '/blog/' + val
                this.activestatus = val
                this.menustatus = !this.menustatus
                this.$router.push(urls)
            },
            classMenu(val){
                if (this.activestatus == val){
                    return {
                        'menu-active': true
                    }
                } else {
                    return {
                        '':true
                    }
                }
            },
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
            window.removeEventListener('resize', this.changeWidth)
        }
    }
</script>

<style type="text/css" scoped>
    .appbody{
        display: flex;
        flex-flow: column;
        min-height: 100vh;
    }
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
    .el-submenu__title:hover{
        background-color: #0b445b;
    }
    .html-header2{
        background-color: #0b445b !important;
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

    .containernk{
        margin-left: auto;
        margin-right: auto;
        padding-right: 15px;
        padding-left: 15px;
        background-color: #0b445b;
    }
    .navbar-button{
        float: right;
        margin-right: 15px;
        padding: 2px 3px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .containernk li{
        padding-left: 20px;
        list-style-type: none;
        font-size: 18px;
        color: #fff;
        height: 35px;
    }
    .containernk li:hover{
        color: blue;
    }
    .menu-active{
        color: blue !important;
    }
</style>