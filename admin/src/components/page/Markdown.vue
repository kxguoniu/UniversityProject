<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 编辑博客</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div>
                <el-form ref="postForm" :model="postForm" :rules="rules" class="form-container">
                    <el-row>
                        <el-col :span="24">
                            <el-form-item style="margin-bottom: 40px;" prop="title">
                                <MDinput v-model="postForm.title" :maxlength="100" name="name" required>
                                    标题
                                </MDinput>
                            </el-form-item>
                            <div class="postInfo-container">
                                <el-row>
                                    <el-col :span="8">
                                        <el-form-item label-width="45px" label="作者:" class="postInfo-container-item">
                                            <el-input placeholder="请输入内容" v-model="postForm.author" :disabled="true" class="inputadmin">
                                            </el-input>
                                        </el-form-item>
                                    </el-col>

                                    <el-col :span="10">
                                        <el-form-item label-width="80px" label="发布时间:" class="postInfo-container-item">
                                        <el-date-picker v-model="postForm.create_time" type="datetime" format="yyyy-MM-dd HH:mm:ss" placeholder="选择日期时间"/>
                                        </el-form-item>
                                    </el-col>

                                    <el-col :span="6">
                                        <el-form-item label-width="60px" label="重要性:" class="postInfo-container-item">
                                            <el-rate
                                              v-model="postForm.weight"
                                              :max="3"
                                              :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                                              :low-threshold="1"
                                              :high-threshold="3"
                                              style="margin-top:8px;"/>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col :span="8">
                                        <el-form-item label-width="45px" label="分类:" class="postInfo-container-item">
                                            <el-select v-model="postForm.category" clearable placeholder="请选择" class="selectcate">
                                                <el-option
                                                    v-for="item in categorylist"
                                                    :key="item.name"
                                                    :label="item.name"
                                                    :value="item.name">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span="8">
                                        <el-form-item label-width="80px" label="标签:" class="postInfo-container-item">
                                            <el-select v-model="postForm.taglist" multiple filterable allow-create default-first-option placeholder="请选择">
                                                <el-option
                                                    v-for="item in tagList"
                                                    :key="item.name"
                                                    :label="item.name"
                                                    :value="item.name">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                            </div>
                        </el-col>
                    </el-row>
                    <el-form-item style="margin-bottom: 40px;" label-width="45px" label="摘要:">
                        <el-input :rows="1" v-model="postForm.digested" type="textarea" class="extra" autosize placeholder="请输入内容">
                        </el-input>
                        <span v-show="contentShortLength" class="word-counter">{{ contentShortLength }}字</span>
                        
                    </el-form-item>
                </el-form>
            </div>
            <mavon-editor v-model="postForm.body" ref="md" @imgAdd="$imgAdd" @change="change" style="min-height: 600px"/>
            <el-button class="editor-btn" type="primary" @click="submit">提交</el-button>
        </div>
    </div>
</template>

<script>
    import { mavonEditor } from 'mavon-editor'
    import 'mavon-editor/dist/css/index.css'
    import MDinput from '../common/MDinput'
    const defaultForm = {
        title: '测试博客12', // 文章题目
        author: 'admin', // 作者
        category: '', // 分类
        taglist: [], //标签
        weight: 1, //重要性
        body: '', // 文章内容
        html: '', // 文章解析内容
        digested: '你好啊,这里是小牛运维站', // 文章摘要
        create_time: undefined, // 发布时间
    }
    export default {
        name: 'markdown',
        data(){
            const validateRequire = (rule, value, callback) => {
                if (value === '') {
                    this.$message({
                        message: rule.field + '为必传项',
                        type: 'error'
                    })
                    callback(new Error(rule.field + '为必传项'))
                } else {
                    callback()
                }
            }
            return {
                tagList:[],
                categorylist: [],
                postForm: Object.assign({}, defaultForm),
                rules: {
                    title: [{ validator: validateRequire }],
                },
            }
        },
        props:{
            isEdit:{
                type: Boolean,
                default: false
            }
        },
        computed:{
            // 动态显示摘要长度
            contentShortLength() {
                return this.postForm.digested.length
            }
        },
        created(){
            // 分类,标签 列表请求
            var url = this.HOST + 'taglist'
            this.$axios({
                url: url,
                method: 'get',
            })
            .then(res => {
                console.log(res.data.data);
                this.tagList = res.data.data.tag;
                this.categorylist = res.data.data.category;
            })
            .catch(error => {
                console.log(error)
            })
            // 编辑博文,请求
            if (this.isEdit){
                const id = this.$route.params && this.$route.params.id
                let url = this.HOST + 'detail'
                this.$axios({
                    method: 'get',
                    url: url,
                    params:{
                        id: id,
                    }
                })
                .then(res => {
                    console.log(res.data)
                    this.postForm = res.data.data;
                })
                .catch(error => {
                    console.log(error)
                })
            } else {
                this.postForm = Object.assign({}, defaultForm)
            }
        },
        components: {
            mavonEditor,
            MDinput,
        },
        methods: {
            // 将图片上传到服务器，返回地址替换到md中
            $imgAdd(pos, $file){
                var formdata = new FormData();
                formdata.append('file', $file);
                // 这里没有服务器供大家尝试，可将下面上传接口替换为你自己的服务器接口
                this.$axios({
                    url: '/common/upload',
                    method: 'post',
                    data: formdata,
                    headers: { 'Content-Type': 'multipart/form-data' },
                }).then((url) => {
                    this.$refs.md.$img2Url(pos, url);
                })
            },
            // 解析后的结果保存到 html
            change(value, render){
                this.postForm.html = render;
            },
            // 博文保存
            submit(){
                console.log(this.postForm);
                let url = this.HOST + 'blogsave';
                var postForm = this.postForm;
                this.$axios({
                    url: url,
                    method: 'post',
                    data: postForm,
                    headers: { 'Content-Type': 'multipart/form-data' },
                })
                .then(res => {
                    console.log(res.data);
                    if (res.data.data.status == 1 ){
                        this.$message.success(res.data.data.msg);
                    } else {
                        this.$message.success('提交成功！');
                    }
                })
                .catch(error => {
                    console.log(error);
                    this.$message.error('提交失败');
                })
            }
        }
    }
</script>
<style scoped>
    .selectcate{
    }
    .inputadmin{
        width: auto;
    }
    .editor-btn{
        margin-top: 20px;
    }
    .word-counter{
        width: 40px;
        position: absolute;
        right: -5px;
        top: 0px;
    }
</style>