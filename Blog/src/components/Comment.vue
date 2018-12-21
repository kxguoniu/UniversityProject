<template>
    <div>
        <div id="reply" class="reply-input">
            <el-input id="comment_reply" type="textarea" :autosize="{ minRows:2, maxRows:5}" placeholder="说点什么吧..." v-model="reply" maxlength="20" @focus="changebutton" @blur="changebutton"></el-input>
            <div class="reply-button" v-if="button && !login">
                <span>登录才能回复呦</span>
                <el-button id="login_now" style="float: right;" size="mini" type="danger" round @click="loginnow">立马登录</el-button>
            </div>
            <div class="reply-button" v-if="button && login">
                <span>还能输入{{ finallength }}字</span>
                <el-button id="csubmit" style="float: right;" size="mini" type="danger" round @click="review">发表评论</el-button>
            </div>
        </div>
        <div class="comment-list-box">
            <ul class="comment-list" v-for="(info,index) in Info" :key="index">
                <li class="comment-line-box" @mouseover="changebox(index)" @mouseout="changebox(index)">
                    <div class="left-box">
                        <a target="_blank" href="#">
                            <img :src="info.img" class="avatar">
                        </a>
                    </div>
                    <div class="right-box">
                        <div class="info-box">
                            <a href="#">
                                <span class="name">{{ info.user }}：</span>
                            </a>
                            <span class="comment">{{ info.message }}</span>
                            <span class="floor" title="">({{ info.create_time }}  #{{ info.floor }}楼)</span>
                            <span class="opt-box">
                                <span v-if="info.children.length > 0" class="showcomm" @click="showreplay(info.id)">{{ info.look }}回复({{ info.children.length }})</span>
                                <span class="showconn" style="opacity: 0" :ref="'mask' + index">举报</span>
                                <span class="showconn" style="opacity: 0" :ref="'mask' + index" @click="replymessage(info, info, 1)">回复</span>
                            </span>
                        </div>
                    </div>
                </li>
                <li v-if="info.show" class="replay-box" v-for="(child,index2) in info.children">
                    <ul class="comment-list">
                        <li class="" @mouseover="changebox2(index,index2)" @mouseout="changebox2(index,index2)">
                            <div class="left-box">
                                <a href="#">
                                    <img :src="child.img" class="avatar">
                                </a>
                            </div>
                            <div class="right-box reply-box">
                                <div class="info-box">
                                    <a href="#">
                                        <span class="name">{{ child.user }}</span>
                                    </a>
                                    <span class="name1">回复 {{ info.user }}：</span>
                                    <span class="comment">{{ child.message }}</span>
                                    <span class="floor" title="">({{ child.create_time }})</span>
                                    <span class="showconn" style="opacity: 0" :ref="'mask2' + index + index2">举报</span>
                                    <span class="showconn" style="opacity: 0" :ref="'mask2' + index + index2" @click="replymessage(info,child, 2)">回复</span>
                                </div>
                            </div>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"Comment",
        data(){
            return{
                Info: [],
                reply: "",
                button: false,
                login: false,
                status: 0,
                replyid: -1,
                replyuser: '',
            }
        },
        props:{
            blogid:{
                type: String,
            }
        },
        created(){
            this.init()
            this.$nextTick(() => {
                this.getlocal()
            })
        },
        mounted(){
            this.$nextTick(function(){
                window.addEventListener('scroll', this.handleScroll)
            })
        },
        deactivated(){
            window.removeEventListener('scroll', this.handleScroll)
        },
        computed:{
            finallength(){
                return 20 - this.reply.length
            }
        },
        methods:{
            getlocal(){
                let select = localStorage.getItem("anchor")
                let anchorEnement = document.getElementById(select)
                if (select && this.$route.query.floor) {
                    anchorEnement.scrollIntoView()
                }
            },
            // 请求数据
            init(){
                var url = this.HOST + 'comment'
                this.$axios({
                    method: 'get',
                    url: url,
                    params: {
                        id:this.blogid
                    }
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.Info = res.data.data
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            },
            // 输入框焦点
            changebutton(){
                console.log(localStorage.getItem('nkx_username'))
                if (localStorage.getItem('nkx_username')){
                    this.login = true
                } else {
                    this.login = false
                }
                if (this.button){
                    setTimeout(() => {
                        this.button = !this.button
                    }, 300)
                } else {
                    this.button = !this.button
                }
            },
            // 显示/隐藏评论
            showreplay(val){
                for (var i=0; i < this.Info.length; i++){
                    if (this.Info[i].id == val){
                        this.Info[i].show = !this.Info[i].show
                        if (this.Info[i].show){
                            this.Info[i].look = "收起"
                        } else {
                            this.Info[i].look = "查看"
                        }
                        break
                    }
                }
            },
            // 显示/隐藏按钮
            changebox(val){
                var mask = this.$refs['mask' + val]
                if (mask[0].style.opacity == 0){
                    mask[0].style.opacity = 1
                    mask[1].style.opacity = 1
                } else {
                    mask[0].style.opacity = 0
                    mask[1].style.opacity = 0
                }
            },
            // 显示/隐藏按钮
            changebox2(val1,val2){
                var mask = this.$refs['mask2' + val1 + val2]
                if (mask[0].style.opacity == 0){
                    mask[0].style.opacity = 1
                    mask[1].style.opacity = 1
                } else {
                    mask[0].style.opacity = 0
                    mask[1].style.opacity = 0
                }
            },
            replymessage(info, child, val){
                this.reply = '@' + child.user + '\n'
                this.status = val
                this.replyid = info.id
                this.replyuser = child.user
            },
            csrf(){
                console.log(document.cookie)
                console.log(localStorage)
            },
            // 去登陆
            loginnow(){
                console.log('11',location)
                this.$router.push({ path: "/login", query: { redirect: location.hash } })
                localStorage.setItem('anchor', 'reply')
            },
            // 提交评论
            review(){
                // status 1 是楼层回复 2是沙发回复
                var postfrom = {
                    message: this.reply,
                    status: this.status,
                    replyid: this.replyid,
                    blogid: this.blogid,
                    replyuser: this.replyuser
                }
                console.log(postfrom)
                var url = this.HOST + 'comment'
                this.$axios({
                    method: 'post',
                    url: url,
                    data: postfrom,
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.$message.success(res.data.msg)
                        this.init()
                        this.reply = ''
                    } else {
                        this.$message.error(res.data.msg)
                        this.init()
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            },
        }
    }
</script>

<style type="text/css" scoped>
    .reply-input{
        padding: 0 3%;
    }
    .reply-button{

    }
    .comment-list-box{
        padding: 0 3%;
    }
    .comment-list-box ul{
        list-style: none;
    }
    .comment-list-box ul li{
        margin-bottom: 8px;
        display: block;
    }
    .left-box{
        float: left;
    }
    .left-box a{
        color: #333;
    }
    .right-box{
        padding-left: 4%;
        width: 96%;
    }
    .info-box a{
        color: #333;
    }
    .replay-box{
        margin-left: 32px;
        padding-left: 8px;
        border-left: 4px solid #c5c5c5;
    }
    .replay-box ul{
        list-style: none;
    }
    .replay-box ul li{
        display: block;
    }
    .showcomm{
        cursor: pointer;
        color: #79a5e5;
    }
    .showconn{
        cursor: pointer;
        color: #79a5e5;
    }
    .floor{
        color: #999999;
    }
    .name1{
        color: #999999;
    }
    .avatar{
        height: 24px;
        width: 24px;
    }
</style>