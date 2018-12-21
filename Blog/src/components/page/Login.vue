<template>
    <div class="login-wraps">
        <div v-if="status" class="ms-login">
            <div class="ms-title">后台管理系统</div>
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="ms-content">
                <el-form-item prop="username">
                    <el-input v-model="ruleForm.username" placeholder="username">
                        <el-button slot="prepend" icon="el-icon-lx-people"></el-button>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" placeholder="password" v-model="ruleForm.password" @keyup.enter.native="submitForm('ruleForm')">
                        <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
                    </el-input>
                </el-form-item>
                <div class="login-btn">
                    <div style="width: 50%;float: left">
                        <el-button style="width: 90%" type="primary" @click="submitForm('ruleForm')">登录</el-button>
                    </div>
                    <div style="width: 50%;float: left;">
                        <el-button style="width: 90%" type="primary" @click="change">马上注册</el-button>
                    </div>
                </div>
            </el-form>
        </div>
        <div v-if="!status" class="ms-register">
            <div class="ms-title">
                注册用户信息
            </div>
            <el-form :model="registerForm" :rules="rules" ref="registerForm" class="ms-write" prop="registerForm">
                <el-form-item prop="user">
                    <div style="float: left; width: 90px; text-align: center;">
                        <span solt="label" class="item-label">用&nbsp;&nbsp;户&nbsp;&nbsp;名</span>
                    </div>
                    <div style="float: left; width: 250px">
                        <el-input v-model="registerForm.user" style="float: left"></el-input>
                    </div>
                </el-form-item>
                <el-form-item prop="passwd">
                    <div style="float: left; width: 90px; text-align: center;">
                        <span solt="label" class="item-label">密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码</span>
                    </div>
                    <div style="float: left; width: 250px">
                        <el-input v-model="registerForm.passwd" type="password" style="float: left"></el-input>
                    </div>
                </el-form-item>
                <el-form-item prop="passwd2">
                    <div style="float: left; width: 90px; text-align: center;">
                        <span solt="label" class="item-label">确认密码</span>
                    </div>
                    <div style="float: left; width: 250px">
                        <el-input v-model="registerForm.passwd2" type="password" style="float: left"></el-input>
                    </div>
                </el-form-item>
                <div style="text-align: center;">
                    <div style="width: 50%; float: left;">
                        <el-button style="width: 90%;" type="primary" @click="register">注册</el-button>
                    </div>
                    <div style="width: 50%; float: left;">
                        <el-button style="width: 90%;" type="primary" @click="change">返回登录</el-button>
                    </div>
                </div>
            </el-form>
        </div>
    </div>
</template>

<script>
    export default {
        data(){
            // 密码验证
            let passcheck = (rule, value, callback) => {
                console.log(value)
                if (value.length >= 8){
                    for (var i=0, num=0, letter=0, LETTER=0; i<value.length; i++){
                        if (value.charCodeAt(i) >= 48 && value.charCodeAt(i) <= 57) {
                            num = 1
                        } else if (value.charCodeAt(i) >=65 && value.charCodeAt(i) <= 90) {
                            letter = 1
                        } else if (value.charCodeAt(i) >=97 && value.charCodeAt(i) <= 122) {
                            LETTER = 1
                        } else {
                            this.registerForm.passwd = ''
                            return callback(new Error('只能输入数字大小写字母'))
                        }
                    }
                    if (num+letter+LETTER == 3){
                        callback()
                    } else {
                        this.registerForm.passwd = ''
                        callback(new Error('必须包含数字和大小写字母'))
                    }
                } else {
                    this.registerForm.passwd = ''
                    callback(new Error('密码长度不能小于8位'))
                }
            }
            // 相同验证
            let passcheck2 = (rule, value, callback) => {
                console.log(value)
                if (value == this.registerForm.passwd){
                    callback()
                } else {
                    this.registerForm.passwd2 = ''
                    callback(new Error('与输入密码不一致'))
                }
            }
            return {
                ruleForm: {
                    username: 'kxguoniu',
                    password: '123456'
                },
                registerForm: {
                    user: '',
                    passwd: '',
                    passwd2: ''
                },
                rules: {
                    username: [
                        { required: true, message: '请输入用户名', trigger: 'blur', }
                    ],
                    password: [
                        { required: true, message: '请输入密码', trigger: 'blur' }
                    ],
                    user: [
                        { required: true, message: '请输入用户名', trigger: 'blur' }
                    ],
                    passwd: [
                        { validator: passcheck, trigger: 'blur' }
                    ],
                    passwd2: [
                        { validator: passcheck2, trigger: 'blur' }
                    ]
                },
                status: true,
            }
        },
        methods: {
            // 登录
            submitForm(formName){
                if (this.ruleForm.username != '' && this.ruleForm.password != '') {
                    var url = this.HOST + 'login'
                    this.$axios({
                        method: 'post',
                        url: url,
                        data: this.ruleForm,
                    })
                    .then(res => {
                        if (res.data.status == 0) {
                            localStorage.setItem('nkx_username', this.ruleForm.username)
                            console.log('111',this.$route.query.redirect)
                            var redict = /.*(\/blogdetail\/\d+)$/.exec(this.$route.query.redirect)
                            console.log(redict)
                            if (redict){
                                this.$router.push({ path:redict[1], query: {floor:true } })
                                //this.$router.go(-1)
                            } else {
                                this.$router.push('/dashboard')
                            }
                        } else {
                            this.$message.error(res.data.msg)
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
                }
            },
            // 注册
            register(){
                if (this.registerForm.user != '' && this.registerForm.passwd != '' && this.registerForm.passwd2 != ''){
                    var url = this.HOST + 'login'
                    this.$axios({
                        method: 'put',
                        url: url,
                        data: this.registerForm,
                    })
                    .then(res => {
                        if (res.data.status == 0){
                            this.$message.success(res.data.msg)
                        } else {
                            this.$message.error(res.data.msg)
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
                } else {
                    this.$message.error('请填写注册信息')
                }
            },
            change(){
                this.status = !this.status
            },
        }
    }
    //
</script>

<style>
    html,body,#app{
        height: 100%;
        width: 100%;
    }
    .login-wraps{
        position: relative;
        width:100%;
        height:100%;
        background-image: url(../../assets/login-bg.jpg);
        background-size: 100%;
        z-index: 100;
    }
    .ms-title{
        width:100%;
        line-height: 50px;
        text-align: center;
        font-size:20px;
        color: #fff;
        border-bottom: 1px solid #ddd;
    }
    .ms-login{
        position: absolute;
        left:50%;
        top:50%;
        width:350px;
        margin:-190px 0 0 -175px;
        border-radius: 5px;
        background: rgba(255,255,255, 0.3);
        overflow: hidden;
    }
    .ms-register{
        position: absolute;
        left: 50%;
        top: 50%;
        width: 400px;
        margin: -200px 0 0 -200px;
        overflow: hidden;
    }
    .ms-content{
        padding: 30px 30px;
    }
    .ms-write{
        padding: 30px 30px;
    }
    .login-btn{
        text-align: center;
    }
    .login-btn button{
        width:100%;
        height:36px;
        margin-bottom: 10px;
        overflow: hidden;
    }
    .login-tips{
        font-size:12px;
        line-height:30px;
        color:#fff;
    }
    .item-label:before{
        content: '*';
        color: #f56c6c;
        margin-right: 4px;
    }
    .item-label{
        font-size: 16px;
        color: 
    }
</style>