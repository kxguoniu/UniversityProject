<template lang="html">
    <div>
        <div class="guidang">
            <span class="guidang-name">归档</span>
        </div>
        <div class="guidang1" v-for="item in bloggroup">
            <router-link :to="{ path:'/blog/1', query:{time:item.time,search:'group'} }">
                <span id="group" class="guidang-name1">{{ item.flag }}({{ item.nums }})</span>
            </router-link>
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
            var url = this.HOST + 'bloglist'
            this.$axios({
                method: 'get',
                url: url,
                params:{
                    search: 'group',
                    flag: '1'
                }
            })
            .then(res => {
                this.bloggroup = res.data.data;
            })
            .catch(error => {
                console.log(error);
            })
        }
    }
</script>

<style type="text/css" scoped>
    .guidang {
        background-color: #3D4450;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
        margin-top: 40px;
    }
    .guidang1 {
        background-color: #d6d8d5;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
        border: 1px solid #fff;
    }
    .guidang-name {
        color: #FFFFFF;
    }
    .guidang1 a{
        text-decoration:none;
        color: #000;
    }
    .guidang1 a:hover{
        color: #f31717;
    }
</style>