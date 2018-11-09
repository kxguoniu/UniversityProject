<template lang="html">
    <div>
        <div class="hot">
            <span class="hot-name">最新文章</span>
        </div>
        <div class="hot1" v-for="newblog in newblogs">
            <a href="#"><span class="hot-name1">{{ newblog.title }}</span></a>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"",
        data(){
            return{
                newblogs:[],
            }
        },
        created(){
            //var url = "/static/new.json";
            //this.$axios.get(url)
            var url = this.HOST + "newblog";
            this.$axios.get(url)
            .then(res => {
                this.newblogs = res.data.data;
            })
            .catch(error => {
                console.log(error);
            })
        }
    }
</script>

<style type="text/css">
    .hot {
        background-color: #3D4450;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
    }
    .hot1 {
        background-color: #FFFFFF;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
        border: 1px solid #dddddd;
    }
    .hot-name {
        color: #FFFFFF;
    }
    .hot-name1 {
        color: #000000;
    }
    .hot1 a{
        text-decoration:none;
    }
</style>