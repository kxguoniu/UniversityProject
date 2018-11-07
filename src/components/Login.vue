<template lang="html">
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
</template>

<script type="text/javascript">
    export default{
        name:"loginelement",
        data(){
            return{

            }
        }
    }
</script>

<style type="text/css">
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
</style>