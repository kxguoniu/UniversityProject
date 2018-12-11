<template lang="html">
    <div>
        <div class="hot">
            <span class="hot-name">最新文章</span>
        </div>
        <div class="hot1" v-for="(newblog,index) in newblogs" :key="index">
            <router-link :to="'/blogdetail/'+ newblog.id">
                <a><span class="hot-name1">{{ newblog.title }}</span></a>
            </router-link>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"news",
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
        },
        methods:{
            ShowDetail(Id){
                var url = this.HOST + "detail";
                this.$axios.get(url, {
                    params:{
                        id:Id
                    }
                })
                .then(res => {
                    if (res.data.status == 0){
                        var blog = res.data.data;
                        var result = blog.body.match(/(<div class="toc">(?:.|\n)*<\/ul>\n<\/div>)/);
                        if (result != null){
                            result = result[0];
                            this.bus.$emit('toc', result, toc_status);
                        } else{
                            this.bus.$emit('toc', '', false);
                        }
                        blog.body = blog.body.replace(/(<div class="toc">(?:.|\n)*<\/ul>\n<\/div>)/, "");
                        this.bus.$emit('blogdetail', true, blog);
                    }
                })
                .catch(error => {
                    console.log(error);
                })
            }
        },
    }
</script>

<style type="text/css" scoped>
    .hot {
        background-color: #3D4450;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
    }
    .hot1 {
        background-color: #a7a7a7;
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