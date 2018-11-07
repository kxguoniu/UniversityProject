<template lang="html">
    <div class="">
        <BlogList :CategoryId="GetId()"></BlogList>
    </div>
</template>

<script type="text/javascript">
    import BlogList from '../components/BlogList'
    export default{
        name:'blogpage',
        components:{BlogList},
        methods:{
            GetId(){
                console.log(this.$route.params.id);
                return this.$route.params.id;
            }
        },
    }
</script>

<style type="text/css">
</style>