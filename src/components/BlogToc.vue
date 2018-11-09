<template lang="html">
    <div v-if="status" class="blogtoc">
        <p><strong class="toc-title">文章目录</strong></p>
        <div class="entity" v-html="toc"></div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"blogtoc",
        data(){
            return{
                toc:"",
                status:false,
            }
        },
        mounted(){
            var _this = this;
            this.bus.$on('toc', function(val1,val2){
                _this.toc = val1;
                _this.status = val2;
            })
        }
    }
</script>

<style type="text/css">
    .blogtoc{
        border: 1px solid #efefef;
        margin-bottom: 30px;
    }
    .blogtoc a{
        text-decoration:none;
        color: #999;
    }
    .blogtoc p{
        display: block;
        -webkit-margin-before: 1em;
        -webkit-margin-after: 1em;
        -webkit-margin-start: 0px;
        -webkit-margin-end: 0px;
    }
    .blogtoc strong{
        border-left: 5px solid #999;
        padding: 2px 5px 2px 15px;
        color: #999;
    }
    .entity{
        margin-bottom: 15px;
    }
    .entity li{
        display: list-item;
        list-style: none;
    }
    .entity ul{
        margin-left: 20px;
    }
</style>