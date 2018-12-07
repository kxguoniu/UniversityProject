<template>
    <div>
        <div class="html-header">
            <ul>
                <li :key="index" v-for="(item,index) in headers">
                    <router-link tag="a" :to="{name:'BlogPage', params:{id:item.id}}" >{{ item['name'] }}</router-link>
                </li>
            </ul>
        </div>
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
    }
</script>

<style type="text/css">
    .html-header{
        background-color: #0b445b !important;
        min-width: 800px;
        margin-bottom: 20px;
    }
    .html-header ul{
        width: 90%;
        padding: 0 5%;
    }
    .html-header ul li{
        display:inline-block;
        width: 11%;
        line-height: 54px;
        text-align: center;
    }
    .html-header ul li a{
        width: 100%;
        color: #FFFFFF;
        text-decoration:none;
    }
    .html-header ul li a.active{
        color: red;
    }


    .html-body{
        margin: 0 3%;
        padding: 0 1%;
    }
</style>