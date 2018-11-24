<template>
    <div>
        <el-menu
            :default-active="'/categroay/1'"
            class="html-header"
            mode="horizontal"
            @select="handleSelect"
            background-color="#0b445b"
            text-color="#fff"
            active-text-color="#ffd04b"
            router
            >
            <el-menu-item :index="'/categroay/' + item.id" :key="index" v-for="(item,index) in headers">{{ item.name }}</el-menu-item>
        </el-menu>
        <div class="html-body">
            <router-view></router-view>
            <BodyRight></BodyRight>
        </div>
        <div class="footer html-bottom"></div>
    </div>
</template>

<script type="text/javascript">
    import BodyRight from './BodyRight'
    export default{
        name:"index",
        components:{
            BodyRight,
        },
        data(){
            return{
                headers:[],
            }
        },
        created(){
            //var url = this.HOST;
            var url = "/static/index.json";
            this.$axios.get(url)
            .then(res => {
                this.headers = res.data.data;
            })
            .catch(error =>{
                console.log(error);
            })
        },
        methods: {
            handleSelect(key, keyPath){
                console.log(key, keyPath)
            }
        }
    }
</script>

<style type="text/css">
    .html-header{
        background-color: #0b445b !important;
        min-width: 800px;
        margin-bottom: 20px;
        width: 90%;
        padding: 0 5%;
    }
    .html-header li{
        font-size: 15px;
        line-height: 54px;
        width: 11%;
        text-align: center;
    }

    .html-body{
        margin: 0 3%;
        padding: 0 1%;
    }
</style>