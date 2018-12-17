<template lang="html">
    <div>
        <div class="biaoqian">
            <span class="biaoqian-name">标签云</span>
        </div>
        <router-link :keys="index" v-for="(tag,index) in tags" :to="{ path:'/categroay/1', query:{id:tag.id} }">
            <div class="biaoqian1" >
                {{ tag.name }}
            </div>
        </router-link>
        
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"Tag",
        data(){
            return{
                tags:[],
            }
        },
        created(){
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

<style type="text/css" scoped>
    .biaoqian {
        background-color: #3D4450;
        padding: 5px 5px;
        margin-right: 10px;
        margin-top: 40px;
    }
    .biaoqian-name {
        color: #FFFFFF;
    }
    .biaoqian-name1 {
        color: #000000;
    }
    .biaoqian1 {
        float: left;
        background-color: #3D4450;
        padding: 5px 5px;
        margin-top: 10px;
        margin-right: 10px;
    }
    .biaoqian1 a{
        color: #FFFFFF;
        text-decoration:none;
    }
</style>