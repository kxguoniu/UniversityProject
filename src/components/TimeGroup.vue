<template lang="html">
    <div>
        <div class="guidang">
            <span class="hot-name">归档</span>
        </div>
        <div class="guidang1" v-for="item in bloggroup">
            <a href="#"><span class="hot-name1">{{ item }}</span></a>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"",
        data(){
            return{
                bloggroup:[],
            }
        },
        created(){
            var url = "/static/group.json";
            this.$axios.get(url)
            .then(res => {
                this.bloggroup = res.data.data;
            })
            .catch(error => {
                console.log(error);
            })
        }
    }
</script>

<style type="text/css">
    .guidang {
        background-color: #3D4450;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
        margin-top: 40px;
    }
    .guidang1 {
        background-color: #FFFFFF;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
        border: 1px solid #dddddd;
    }
    .guidang1 a{
        text-decoration:none;
    }
</style>