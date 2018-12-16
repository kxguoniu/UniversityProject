<template>
    <div class="footer">
        <div class="floor_1">
            <div class="footer_1">
                <div class="aboutme">
                    <p><span class="titlename">关于我们：</span></p>
                    <p><span class="aboutcontent1"><a href="https://github.com/kxguoniu">https://github.com/kxguoniu</a></span></p>
                </div>
                <div class="callme">
                    <p><span class="titlename">联系我们：</span></p>
                    <p><span class="aboutcontent1">QQ</span><span style="color: #fff; font-size: 16px;">1320741337</span></p>
                    <p><span class="aboutcontent2">Email</span><span style="color: #fff; font-size: 16px;">13213790823@163.com</span></p>
                </div>
            </div>
            <div class="footer_1">
                <div class="friendship">
                    <p><span class="friendtitle">友情链接</span></p>
                    <p><span class="friend_a"><a href="#">虚位以待</a></span></p>
                    <p><span class="friend_a"><a href="#">虚位以待</a></span></p>
                    <p><span class="friend_a"><a href="#">虚位以待</a></span></p>
                </div>
                <div class="friendship">
                    <p><span class="friend_2"><a href="#">虚位以待</a></span></p>
                    <p><span class="friend_a"><a href="#">虚位以待</a></span></p>
                    <p><span class="friend_a"><a href="#">虚位以待</a></span></p>
                    <p><span class="friend_a"><a href="#">虚位以待</a></span></p>
                </div>
                <div class="friendship">
                    <p><span class="friend_2"><a href="#">虚位以待</a></span></p>
                    <p><span class="friend_a"><a href="#">虚位以待</a></span></p>
                    <p><span class="friend_a"><a href="#">虚位以待</a></span></p>
                    <p><span class="friend_a"><a href="#">虚位以待</a></span></p>
                </div>
            </div>
        </div>
        <div class="floor_2">
            <p>
                Copyright © 2018-2018 小牛运维站. All Rights Reserved
            </p>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default{
        name: 'footer',
        data(){
            return{
            }
        },
    }
</script>

<style type="text/css">
    .footer{
        height: 200px;
        background-color: #2d3341;
        flex: 0;
    }
    .floor_1{
        padding-left: 5%;
        padding-right: 18%;
        height: 180px;
    }
    .floor_2{
        height: 20px;
        background-color: #f3f3f3;
    }
    .floor_2 p{
        text-align: center;
    }
    .footer_1{
        float: left;
        margin-top: 25px;
        margin-right: 1%;
        width: 49%;
        height: 130px;
    }
    .aboutme{
        height: 60px;
    }
    .callme{
        height: 65px;
    }
    .titlename{
        color: #fff;
        padding-left: 25px;
        font-size: 18px;
    }
    .aboutcontent1{
        padding-left: 60px;
        padding-right: 40px;
        font-size: 16px;
        color: #fff;
    }
    .aboutcontent2{
        padding-left: 60px;
        padding-right: 25px;
        font-size: 16px;
        color: #fff;
    }
    .friendship{
        float: left;
        width: 29%;
        margin: 0 2%;
        height: 130px;
    }
    .friendtitle{
        display: block;
        color: #fff;
        font-size: 20px;
        margin: 10px 0;
    }
    .friend_a{
        color: #fff;
        font-size: 16px;
        display: block;
        margin-bottom: 10px;
    }
    .footer a{
        text-decoration: none;
        color: #fff;
    }
    .footer a:hover{
        color: blue;
    }
    .friend_2{
        color: #fff;
        display: block;
        font-size: 16px;
        margin: 10px 0;
    }
</style>