<template lang="html">
    <div>
        <div class="guidang">
            <span class="hot-name">标签云</span>
        </div>
        <div class="biaoqian" v-for="tag in tags">
            <a href="#">{{ tag.name }}</a>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"",
        data(){
            return{
                tags:[],
            }
        },
        created(){
            //var url = "/static/tag.json";
            var url = this.HOST + "taglist";
            this.$axios.get(url)
            .then(res => {
                this.tags = res.data.data.tag;
            })
            .catch(error => {
                console.log(error);
            })
        }
    }
</script>

<style type="text/css">
    .biaoqian {
        float: left;
        background-color: #3D4450;
        padding: 5px 5px;
        margin-top: 10px;
        margin-right: 10px;
    }
    .biaoqian a{
        color: #FFFFFF;
        text-decoration:none;
    }
</style>