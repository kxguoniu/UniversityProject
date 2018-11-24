<template lang="html">
    <div class="body-right">
        <Search></Search>
        <BlogToc></BlogToc>
        <NewBlog></NewBlog>
        <TimeGroup></TimeGroup>
        <BlogTag></BlogTag>
    </div>
</template>

<script type="text/javascript">
    import Login from '../components/Login'
    import Search from '../components/Search'
    import NewBlog from '../components/NewBlog'
    import TimeGroup from '../components/TimeGroup'
    import BlogTag from '../components/BlogTag'
    import BlogToc from '../components/BlogToc'
    export default{
        name:"bodyright",
        components:{
            Login,
            Search,
            NewBlog,
            TimeGroup,
            BlogTag,
            BlogToc,
        },
        mounted(){
            var _this = this
            this.bus.$on('add', function(val){
                //_this.status1 = val;
            })
        },
        data(){
            return{
            }
        }
    }
</script>

<style type="text/css">
    .body-right{
        float: right;
        width: 31%;
    }
</style>