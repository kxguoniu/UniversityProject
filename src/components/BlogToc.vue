<template lang="html">
    <div id = "TocRight" class="body-right">
        <div id="TocBar" :class="{'blogtoc':true, 'right-bind':status}">
            <p><strong class="toc-title">文章目录</strong></p>
            <div class="entity" v-html="toc"></div>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"blogtoc",
        props:{
            toc:{
                type: String,
                default: ""
            }
        },
        data(){
            return{
                status: true
            }
        },
        mounted(){
            //window.addEventListener('scroll', this.handleScroll)
        },
        methods:{
            handleScroll(){
                console.log(this.status)
                var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
                var offsetTop = document.querySelector('#TocBar').offsetTop
                console.log(scrollTop,offsetTop)
                if (scrollTop > offsetTop) {
                    this.status = true
                    console.log(this.status)
                } else {
                    this.status = false
                    console.log(this.status)
                }
            }
        },
        destroyed(){
            //window.removeEventListener('scroll', this.handleScroll)
        }
    }
</script>

<style type="text/css">
    .body-right{
        margin-top: 80;
        overflow-y:scroll;
        float: right;
        width: 31%;
    }
    .right-bind{
        position: fixed;
        top: 80px;
        width: 29%;
    }
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
    .blogtoc p strong{
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