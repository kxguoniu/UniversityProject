<template>
    <div class="error-page">
        <div class="error-code">4<span>0</span>4</div>
        <div class="error-desc">啊哦~ 你所访问的页面不存在</div>
        <div class="error-desc">
            <span style="color: #a94747">{{ count }}</span><span>秒后转至首页</span>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:'error',
        data(){
            return {
                count: '',
            }
        },
        created(){
            this.init()
        },
        methods:{
            init(){
                const TIME_COUNT = 3
                if (!this.timer){
                    this.count = TIME_COUNT
                    this.show = false
                    this.timer = setInterval(() => {
                        if (this.count > 0 && this.count <= TIME_COUNT){
                            this.count --
                        } else {
                            this.show = true
                            clearInterval(this.timer)
                            this.timer = null
                            this.$router.push('/')
                        }
                    },1000)
                }
            }
        }
    }
</script>

<style>
    .error-page{
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        width: 100%;
        height: 100%;
        padding-top: 100px;
        box-sizing: border-box;
    }
    .error-code{
        line-height: 1;
        font-size: 250px;
        font-weight: bolder;
        color: #2d8cf0;
    }
    .error-code span{
        color: #00a854;
    }
    .error-desc{
        font-size: 30px;
        color: #777;
    }
</style>
