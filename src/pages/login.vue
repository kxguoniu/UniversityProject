<template lang="html">
    <div class="login">
        <form @submit.prevent="submit">
            <table>
                <tr class="tr1">
                    <td width="25%">用户名</td>
                    <td><input v-model="inputtext.name" type="text" name="username" /></td>
                </tr>
                <tr class="tr1">
                    <td>密码</td>
                    <td><input v-model="inputtext.password" type="password" name="pwd" /></td>
                </tr>
                <tr class="tr2">
                    <td width="50%"><input v-model="inputtext.code" type="text" name="code" ></td>
                    <td>asd </td>
                </tr>
                <tr class="tr2">
                    <td><input type="submit" value="提交"></td>
                    <td><button type="button">重置</button></td>
                </tr>
            </table>
        </form>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"login",
        data(){
            return {
                inputtext:{}
            }
        },
        methods:{
            submit:function(){
                console.log(this.inputtext);
                this.$axios.get()
            }
        }
    }
</script>

<style type="text/css" scoped>
.login{
    height: 500px;
    margin: 0 auto;
}
.login form{
    width: 50%;
    margin: 0 auto;
}
.login form table{
    border: 1px solid;
}
.login form table td{
    border: 1px solid;
}
.tr1 td{
    text-align: center;
}
.tr1 input{
    width: 99%;
    height: 99%;
}
.tr2 td{
    text-align: center;
}
.tr2 input{
    width: 99%;
    height: 99%;
}
</style>