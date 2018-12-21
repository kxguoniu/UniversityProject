<template lang="html">
    <div class = "html-body">
        <div  class="body-left">
            <div class="blog" v-for="blog in blogs">
                <div class="blog-head">
                    <h1>
                        <router-link :to="'/blogdetail/'+ blog.id">
                            {{ blog.title }}
                        </router-link>
                    </h1>
                </div>
                <div class="blog-info">
                    <span class="span-info"><a href="#">&nbsp;{{ blog.category }}&nbsp;</a></span>
                    <span class="span-info"><a href="#">&nbsp;{{ blog.author }}&nbsp;</a></span>
                    <span class="span-info">&nbsp;{{ blog.create_time }}&nbsp;</span>
                    <span class="span-info">&nbsp;{{ blog.views }} 阅读&nbsp;</span>
                </div>
                <div class="blog-execrpt"><span>{{ blog.digested }}     </span></div>
                <div class="blog-link">
                    <router-link :to="'/blogdetail/'+ blog.id">
                        <a id="readall">阅读全文</a>
                    </router-link>
                </div>
            </div>
            <!-- 底层页数导航 -->
            <div v-if="flash" key="1" class="pagination">
                <el-pagination
                    background
                    class="pagination2"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[3, 5, 10, 15, 20, 50]"
                    :page-size="pagesize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total">
                </el-pagination>
            </div>
            <div v-else key="2" class="pagination">
                <el-pagination
                    background
                    class="pagination2"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[3, 5, 10, 15, 20, 50]"
                    :page-size="pagesize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total">
                </el-pagination>
            </div>
        </div>
        <div class="body-right">
            <Search></Search>
            <NewBlog></NewBlog>
            <TimeGroup></TimeGroup>
            <BlogTag></BlogTag>
        </div>
    </div>
</template>

<script type="text/javascript">
    import Search from '../components/Search'
    import NewBlog from '../components/NewBlog'
    import TimeGroup from '../components/TimeGroup'
    import BlogTag from '../components/BlogTag'
    export default{
        name:"bloglist",
        components:{
            Search,
            NewBlog,
            TimeGroup,
            BlogTag,
        },
        data(){
            return{
                blogs:[],
                CategoryId:"",
                TagId:"",
                GroupId:"",
                flash: false,
                status: false,
                currentPage: 1,
                pagesize: 5,
                listQuery: {
                    page: 1,
                    limit: 5
                },
                total: 0,
                lasturl: "",
            }
        },
        mounted(){
            this.CategoryId = this.$route.params.id
            this.GetBlog()
        },
        watch: {
            $route(){
                this.CategoryId = this.$route.params.id
                this.TagId = this.$route.query.id
                this.GroupId = this.$route.query.time
                this.GetBlog()
            }
        },
        methods:{
            GetBlog(){
                // 加载
                this.status = false
                const loading = this.$loading({
                    lock: true,
                    tagget: 'body-left-list',
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0,0,0,0.7)'
                });
                if (this.TagId){
                    var url = this.HOST + "bloglist";
                    var flag = this.TagId;
                    var search = "tag"
                } else if (this.GroupId){
                    var url = this.HOST + 'bloglist';
                    var flag = this.GroupId;
                    var search = "group"
                } else {
                    var url = this.HOST + "bloglist";
                    var flag = this.CategoryId;
                    var search = "category"
                }
                if (this.lasturl != url + flag) {
                    this.flash = !this.flash
                    this.lasturl = url + flag
                    this.listQuery.limit = 5
                    this.listQuery.page = 1
                }
                this.$axios.get(url, {
                    params:{
                        search: search,
                        flag: flag,
                        page: this.listQuery.page,
                        limit: this.listQuery.limit,
                    }
                })
                .then(res => {
                    if (res.data.status == 0) {
                        this.blogs =  res.data.data;
                        this.total = res.data.total
                        console.log(this.total)
                        loading.close();
                        this.status = true
                    } else {
                        this.$message.error(res.data.msg)
                        loading.close()
                    }
                })
                .catch(error => {
                    console.log(error);
                    loading.close();
                    this.status = true
                })
            },
            // 改变页面显示数
            handleSizeChange(val){
                this.listQuery.limit = val
                this.listQuery.page = 1
                this.GetBlog()
            },
            // 改变页数
            handleCurrentChange(val){
                this.listQuery.page = val
                this.GetBlog()
            },
        }
    }
</script>

<style type="text/css" scoped>
    .html-body{
        padding: 0 3%;
        margin: 0 1%;
        margin-top: 80px;
        margin-bottom: 50px;
        flex: 1;
    }
    @media (min-width: 800px){
        .body-right{
            float: right;
            width: 31%;
        }
        .body-left{
            float: left;
            width: 65%;
        }
    }
    .blog {
        background-color: #bdbdbd73 !important;
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
        background-color: #fff;
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
        cursor: pointer;
        text-decoration:none;
    }
    .pagination{
        text-align: center;
        word-wrap: break-word;
    }
    .pagination2{
        white-space: normal;
    }
    @media (max-width: 800px){
        .body-right{
            position: relative;
            margin: 0 auto;
            width: 100%;
            max-width: 600px;
        }
        .body-left{
            width: 100%;
            margin: 0 auto;
            max-width: 700px;
            padding-bottom: 30px;
        }
    }
</style>