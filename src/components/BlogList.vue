<template lang="html">
        <div class="body-left">
            <div class="blog" v-for="blog in blogs">
                <div class="blog-head">
                    <h1>
                        <a href="">{{ blog.title }}</a>
                    </h1>
                </div>
                <div class="blog-info">
                    <span class="span-info"><a href="#">&nbsp;{{ blog.category }} &nbsp;   </a></span>
                    <span class="span-info"><a href="#">&nbsp;{{ blog.author }} &nbsp;   </a></span>
                    <span class="span-info">&nbsp;{{ blog.create_time }} &nbsp;    </span>
                    <span class="span-info">&nbsp;{{ blog.views }} 阅读&nbsp;</span>
                </div>
                <div class="blog-execrpt"><span>{{ blog.digested }}     </span></div>
                <div class="blog-link"><span><a href="#">阅读全文</a></span></div>
            </div>
        </div>
</template>

<script type="text/javascript">
    export default{
        name:"list",
        data(){
            return{
                blogs:[],
            }
        },
        props:{
            CategoryId:String,
        },
        methods:{
            GetBlog(){
                //var url = "/static/Category" + this.CategoryId + ".json";
                //this.$axios.get(url)
                var url = this.HOST + "category";
                this.$axios.get(url, {
                    params:{
                        flag: this.CategoryId
                    }
                })
                .then(res => {
                    this.blogs =  res.data.data;
                    console.log(res);
                })
                .catch(error => {
                    console.log(error);
                })
            }
        },
        watch:{
            CategoryId(val){
                this.CategoryId = val;
                this.GetBlog();
            }
        },
        created(){
            this.GetBlog();
        }
    }
</script>

<style type="text/css">
    .body-left{
        float: left;
        width: 65%;
    }
    .blog {
        background-color: #FFFFFF;
        width: 100%;
        margin-bottom: 35px;
    }
    .blog-head {
        padding-top: 20px;
        padding-bottom: 10px;
    }
    .blog-head h1 {
        text-align: center;
    }
    .blog-head h1 a{
        text-decoration:none;
        color: #0b445b;
    }
    .blog-info {
        text-align: center;
        padding-top: 10px;
        padding-bottom:20px;
    }
    .blog-info span{
        background-color: #3D4450;
        color: #FFFFFF;
    }
    .blog-info span a{
        text-decoration:none;
        color: #FFFFFF;
    }
    .blog-execrpt {
        margin:0 30px;
        padding: 10px 20px;
        height: auto;
        background-color: #EEEEEE;
        font-size: 14px;
        line-height: 1.428571429;
    }
    .blog-execrpt span{

    }
    .blog-link {
        text-align: center;
        padding-top: 20px;
        padding-bottom: 20px;
    }
    .blog-link a{
        text-decoration:none;
    }
</style>