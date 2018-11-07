<template>
    <div :style="{ paddingBottom: paddingBottom}">
        <div id="fixedBar" :class="{ fixedBar: isFixed, 'html-header':true }">
            <ul>
                <li :key="index" v-for="(item,index) in headers">
                    <router-link tag="a" :to="item.url" >{{ item.name }}</router-link>
                </li>
            </ul>
        </div>
        <div :style="{ marginTop: marginTop }" class="html-body">
            <div class="body-left">
                <div class="blog" v-for="item in blogs">
                    <div class="blog-head">
                        <h1>
                            <a href="">测试博客</a>
                        </h1>
                    </div>
                    <div class="blog-info">
                        <span class="span-info"><a href="#">&nbsp;Linux&nbsp;</a></span>
                        <span class="span-info"><a href="#">&nbsp;Admin&nbsp;</a></span>
                        <span class="span-info">&nbsp;2017-09-17 15:50&nbsp;</span>
                        <span class="span-info">&nbsp;99 阅读&nbsp;</span>
                    </div>
                    <div class="blog-execrpt"><span>zabbix（音同 zæbix）是一个基于WEB界面的提供分布式系统监视以及网 络监视功能的企业级的开源解决方案。 zabbix能监视各种网络参数，保证服务器系统的安全运营；并提供&gt;灵活的通知机制以让系统管理员快速定位/解决存在的各种问题。 下...</span></div>
                    <div class="blog-link"><span><a href="#">阅读全文</a></span></div>
                </div>
            </div>
            <div class="body-right">
                <div class="blog-login">
                    <div class="login-hint">请登录</div>
                    <form class="login-form" action="#" method="post">
                        <div class="input-group">
                            <div class="login-text">user</div>
                            <div class="login-name">
                                <input id="user" class="input-user" name="user" value="" size="20" type="text">
                            </div>
                        </div>
                        <div class="input-group">
                            <div class="login-text">pass</div>
                            <div class="login-name">
                                <input id="pwd" class="input-pwd" name="pwd" value="" size="20" type="password">
                            </div>
                        </div>
                        <div class="input-group">
                            <button class="btn" type="submit" name="submit">登录</button>
                            <a class="btn-a" href="#">注册</a>
                        </div>
                    </form>
                </div>
                <div class="search">
                    <form role="search" id="searchform" class="form-search" method="get" action="{% url 'haystack_search' %}">
                        <div class="search-group">
                            <input id="s" class="search-input" name="q" placeholder=" 搜索..." type="search" required>
                        </div>
                        <div class="search-group2">
                            <button class="search-groups" type="submit" name="submit">搜索</button>
                        </div>
                    </form>
                </div>
                <div>
                    <div class="hot">
                        <span class="hot-name">最新文章</span>
                    </div>
                    <div class="hot1" v-for="item in headers">
                        <a href="#"><span class="hot-name1">{{ item.name }}</span></a>
                    </div>
                </div>
                <div>
                    <div class="guidang">
                        <span class="hot-name">归档</span>
                    </div>
                    <div class="guidang1" v-for="item in headers">
                        <a href="#"><span class="hot-name1">2018 年 11 月</span></a>
                    </div>
                </div>
                <div>
                    <div class="guidang">
                        <span class="hot-name">标签云</span>
                    </div>
                    <div class="biaoqian" v-for="item in headers">
                        <a href="#">标签</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="footer html-bottom"></div>
    </div>
</template>

<script type="text/javascript">
//['首页','Linux','Python','Django','Tornado','Machine','生活','资源分享','其他']
    export default{
        name:"index",
        data(){
            return{
                paddingBottom: "1.5rem",
                isFixed: false,
                offsetTop: 0,
                marginTop: 0,
                headers:[
                    {name:"首页",url:"/#1"},
                    {name:"Linux",url:"/#2"},
                    {name:"Python",url:"/#3"},
                    {name:"Django",url:"/#4"},
                    {name:"Tornado",url:"/#5"},
                    {name:"Machine",url:"/#6"},
                    {name:"生活",url:"/#7"},
                    {name:"资源分享",url:"/#8"},
                    {name:"其他",url:"/#9"}
                ],
                blogs:[1,2,3,4,5,6,7,8,9],
            }
        },
        mounted(){
            this.paddingBottom = document.querySelector('.footer').offsetHeight + 20 + 'px';
            this.offsetTop = document.querySelector('#fixedBar').offsetTop;
            window.addEventListener('scroll', this.handleScroll);
        },
        method:{
            handleScroll(){
                var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
                if (scrollTop >= this.offsetTop) {
                    this.isFixed = true;
                    this.marginTop = document.querySelector('#fixedBar').offsetHeight + 'px';
                } else {
                    this.isFixed = false;
                    this.marginTop = 0;
                }
            },
            handleInteraction(){
                //var url = 
                //this.$axios.
            }
        },
        destroyed(){
            window.removeEventListener('scroll', this.handleScroll);
        },
    }
</script>

<style type="text/css" scoped>
    .fixedBar{
        position: fixed;
        top: 0;
        z-index: 999;
        width: 100%;
    }
    .html-header{
        background-color: #0b445b;
        min-width: 800px;
        margin-bottom: 20px;
    }
    .html-header ul{
        width: 90%;
        padding: 0 5%;
    }
    .html-header ul li{
        display:inline-block;
        width: 11%;
        line-height: 54px;
        text-align: center;
    }
    .html-header ul li a{
        width: 100%;
        color: #FFFFFF;
        text-decoration:none;
    }
    .html-header ul li a.active{
        color: red;
    }
    .html-body{
        margin: 0 3%;
        padding: 0 1%;
    }
    .body-left{
        float: left;
        width: 65%;
    }
    .body-right{
        float: right;
        width: 31%;
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
    .blog-login{
        background-color: #FFFFFF;
        width: 100%;
        margin-bottom: 35px;
    }
    .login-hint{
        padding: 8px 15px;
        background-color: #3D4450;
        color: #FFFFFF;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .login-form {
        height: 180px;
    }
    .input-user {
        height: 33px;
        width: 100%;
        font-size: 20px;
    }
    .input-group {
        clear: both;
        height: 55px;
        margin: 0 15px;
    }
    .input-pwd {
        height: 33px;
        width: 100%;
        font-size: 20px;
    }
    .login-text {
        background-color: #D9524E;
        float: left;
        text-align: center;
        padding: 8px 1.5%;
        margin: 8px 0;
    }
    .login-name {
        float: left;
        width: 84%;
        margin: 8px 0;
    }
    .btn {
        float: left;
        text-align: center;
        padding: 2.5% 18%;
        background-color: #3D4450;
        color: #FFFFFF;
        margin: 8px 0;
    }
    .btn-a{
        float: right;
        text-align: center;
        padding: 2.5% 18%;
        background-color: #3D4450;
        color: #FFFFFF;
        margin: 8px 0;
    }
    .search {
        height: 38px;
        background-color: #3D4450;
        padding-top: 5px;
        padding-left: 1%;
        margin-bottom: 40px;
    }
    .search-group {
        float: left;
        width: 85%;
    }
    .search-group2 {
        width: 15%;
        float: left;
    }
    .search-input {
        height: 32px;
        width: 100%;
        font-size: 15px;
    }
    .search-groups {
        float: left;
        text-align: center;
        padding: 7px 10%;
        margin-left: 20%;
        background-color: #D9534F;
        color: #FFFFFF;
        border: 0px;
    }
    .hot {
        background-color: #3D4450;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
    }
    .hot1 {
        background-color: #FFFFFF;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
        border: 1px solid #dddddd;
    }
    .hot-name {
        color: #FFFFFF;
    }
    .hot-name1 {
        color: #000000;
    }
    .hot1 a{
        text-decoration:none;
    }
    .guidang {
        background-color: #3D4450;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
        margin-top: 40px;
    }
    .guidang1 {
        background-color: #FFFFFF;
        height: 20px;
        padding: 8px 15px;
        font-size: 15px;
        border: 1px solid #dddddd;
    }
    .guidang1 a{
        text-decoration:none;
    }
    .biaoqian {
        float: left;
        background-color: #3D4450;
        padding: 5px 5px;
        margin-top: 10px;
        margin-right: 10px;
    }
    .biaoqian a{
        color: #FFFFFF;
        text-decoration:none;
    }
</style>