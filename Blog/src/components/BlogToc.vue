<template lang="html">
    <div id = "TocRight" class="body-right">
        <div id="TocBar" :class="{'blogtoc':true, 'right-bind':status}">
            <p><strong class="toc-title">文章目录</strong></p>
            <div class="entity" v-html="toc"></div>
        </div>
        <div v-if="back" class="break">
            <i class="icon" @click="reback"></i>
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
                status: true,
                back: false,
            }
        },
        mounted(){
            window.addEventListener('scroll', this.scrolTop)
        },
        methods:{
            scrolTop(){
                var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
                if (scrollTop > 500){
                    this.back = true
                } else {
                    this.back = false
                }
            },
            reback(){
                var height = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
                let step = Math.floor(height / 25)
                console.log(step);
                (function jump(){
                    if (height > 0){
                        height -= step
                        window.scrollTo(0,height)
                        setTimeout(jump, 10)
                    }
                })()
            },
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
            window.removeEventListener('scroll', this.scrolTop)
        }
    }
</script>

<style type="text/css">
    .break{
        background-color: #f9f9f9;
        position: fixed;
        right: 30px;
        bottom: 40px;
        width: 40px;
        height: 40px;
        border-radius: 20px;
        cursor: pointer;
        transition: .3s;
        box-shadow: 0 0 6px rgba(0,0,0,.12);
        z-index: 10000;
    }
    .break i{
        color: #883e33;
        display: block;
        line-height: 40px;
        text-align: center;
        font-size: 25px;
    }
    .icon{
        font-family: element-icons!important;
        speak: none;
        font-style: normal;
        font-weight: 400;
        font-variant: normal;
        text-transform: none;
        vertical-align: baseline;
        -webkit-font-smoothing: antialiased;
    }
    .icon:before{
        content: "\E60C"
    }
    @media (min-width: 800px){
        .body-right{
            float: right;
            width: 31%;
        }
        .right-bind{
            position: fixed;
            top: 80px;
            width: 29%;
        }
    }
    @media (max-width: 800px){
        .body-right{
            position: relative;
            margin: 0 auto;
            width: 100%;
            max-width: 600px;
        }
        .right-bind{
            width: 100%;
        }
    }
    .blogtoc{
        border: 0px solid #efefef;
        margin-bottom: 30px;
    }
    .blogtoc a{
        text-decoration:none;
        color: #524d4d;
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