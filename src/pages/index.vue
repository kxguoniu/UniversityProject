<template>
    <div>
        <el-menu
            :default-active="'1'"
            :class="{'html-header':true, 'html-bind':status}"
            id="searchBar"
            mode="horizontal"
            background-color="#0b445b"
            text-color="#fff"
            active-text-color="#ffd04b"
            router
            >
            <el-menu-item :index="'/categroay/' + item.id" :key="index" v-for="(item,index) in headers">{{ item.name }}</el-menu-item>
        </el-menu>
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
                status: false
            }
        },
        mounted(){
            window.addEventListener('scroll', this.handleScroll)
        },
        created(){
            if (this.GLOBAL.INDEX == 0){
                var counturl = this.HOST + 'countview'
                this.$axios({
                    method: 'get',
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
            window.removeEventListener('scroll', this.handleScroll)
        }
    }
</script>

<style type="text/css" scoped>
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
    }
    .html-header li{
        font-size: 15px;
        line-height: 54px;
        width: 11%;
        text-align: center;
    }
</style>