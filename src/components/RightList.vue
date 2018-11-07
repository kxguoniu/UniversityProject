<template lang="html">
    <div class="body-right">
        <div v-if="logins" class="blog-login">
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
            <div class="hot1" v-for="item in hots">
                <a href="#"><span class="hot-name1">{{ item.name }}</span></a>
            </div>
        </div>
        <div>
            <div class="guidang">
                <span class="hot-name">归档</span>
            </div>
            <div class="guidang1" v-for="item in hots">
                <a href="#"><span class="hot-name1">2018 年 11 月</span></a>
            </div>
        </div>
        <div>
            <div class="guidang">
                <span class="hot-name">标签云</span>
            </div>
            <div class="biaoqian" v-for="item in hots">
                <a href="#">标签</a>
            </div>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"elements",
        data(){
            return{
                hots:[1,2,3],
                logins:true
            }
        }
    }
</script>

<style type="text/css">
    .body-right{
        float: right;
        width: 31%;
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