<template lang="html">
    <div>
        <div class="guidang">
            <span class="guidang-name">归档</span>
        </div>
        <div class="guidang1" v-for="item in bloggroup">
            <router-link :to="{ path:'/categroay/1', query:{time:item.time} }">
                <a><span class="guidang-name1">{{ item.flag }}({{ item.nums }})</span></a>
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
            var url = this.HOST + 'timegroup'
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

<style type="text/css" scoped>
    .guidang {
        background-color: #3D4450;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
        margin-top: 40px;
    }
    .guidang1 {
        background-color: #a7a7a7;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
        border: 1px solid #dddddd;
    }
    .guidang-name {
        color: #FFFFFF;
    }
    .guidang-name1 {
        color: #000000;
    }
    .guidang1 a{
        text-decoration:none;
    }
</style>