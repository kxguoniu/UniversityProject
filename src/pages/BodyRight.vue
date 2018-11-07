<template lang="html">
    <div class="body-right">
        <Login v-if="status1"></Login>
        <Search v-if="status2"></Search>
        <NewBlog v-if="status2"></NewBlog>
        <TimeGroup v-if="status2"></TimeGroup>
        <BlogTag v-if="status2"></BlogTag>
    </div>
</template>

<script type="text/javascript">
    import Login from '../components/Login'
    import Search from '../components/Search'
    import NewBlog from '../components/NewBlog'
    import TimeGroup from '../components/TimeGroup'
    import BlogTag from '../components/BlogTag'
    export default{
        name:"bodyright",
        components:{
            Login,
            Search,
            NewBlog,
            TimeGroup,
            BlogTag
        },
        data(){
            return{
                status1:true,
                status2:true,
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