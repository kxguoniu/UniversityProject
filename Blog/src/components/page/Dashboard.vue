<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="8">
                <el-card shadow="hover" class="mgb20" style="height:252px;">
                    <div class="user-info">
                        <img src="/static/img/img.jpg" class="user-avator" alt="">
                        <div class="user-info-cont">
                            <div class="user-info-name">{{name}}</div>
                            <div>{{role}}</div>
                        </div>
                    </div>
                    <div class="user-info-list">上次登录时间：<span>{{ lasttime }}</span></div>
                    <div class="user-info-list">上次登录地点：<span>北京</span></div>
                </el-card>
                <el-card shadow="hover" style="height:252px;">
                    <div slot="header" class="clearfix">
                        <span>语言详情</span>
                    </div>
                    Vue
                    <el-progress :percentage="72.9" color="#42b983"></el-progress>
                    JavaScript
                    <el-progress :percentage="22.1" color="#f1e05a"></el-progress>
                    CSS
                    <el-progress :percentage="4.1"></el-progress>
                    HTML
                    <el-progress :percentage="0.9" color="#f56c6c"></el-progress>
                </el-card>
            </el-col>
            <el-col :span="16">
                <el-row :gutter="20" class="mgb20">
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-1">
                                <i class="el-icon-lx-people grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ views }}</div>
                                    <div>用户访问量</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-2">
                                <i class="el-icon-lx-notice grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ message }}</div>
                                    <div>系统消息</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-3">
                                <i class="el-icon-lx-goods grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ blogsums }}</div>
                                    <div>博文数量</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
                <el-card shadow="hover" style="height:403px;">
                    <div slot="header" class="clearfix">
                        <span>待办事项</span>
                        <el-button style="float: right; padding: 3px 0" type="text" @click="addList">添加</el-button>
                    </div>
                    <el-table :data="todoList" :show-header="false" height="304" style="width: 100%;font-size:14px;">
                        <el-table-column>
                            <template slot-scope="scope">
                                <div class="todo-item" :class="{'todo-item-del': scope.row.status}">{{scope.row.title}}</div>
                            </template>
                        </el-table-column>
                        <el-table-column width="60">
                            <template slot-scope="scope">
                                <el-tooltip class="item" effect="dark" content="编辑" placement="bottom">
                                    <i class="el-icon-edit" style="cursor:pointer; color: #409EFF" @click="putList(scope.$index, scope.row)"></i>
                                </el-tooltip>
                                <el-tooltip class="item" effect="dark" content="删除" placement="bottom">
                                    <i class="el-icon-delete" style="cursor:pointer; color: #ff0000" @click="delList(scope.$index, scope.row)"></i>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="12">
                <el-card shadow="hover">
                    <schart ref="bar" class="schart" canvasId="bar" :data="data1" type="bar" :options="options"></schart>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card shadow="hover">
                    <schart ref="line" class="schart" canvasId="line" :data="data2" type="line" :options="options2"></schart>
                </el-card>
            </el-col>
        </el-row>


        <!--添加-->
        <el-dialog title="添加" :visible.sync="addstatus" width="30%">
            <el-form ref="form" :model="form" label-width="80px">
                <el-form-item label="添加事项">
                    <el-input v-model="form.title"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addstatus = false">取 消</el-button>
                <el-button type="primary" @click="addEvent">确 定</el-button>
            </span>
        </el-dialog>

        <!--编辑事项-->
        <el-dialog title="编辑" :visible.sync="putstatus" width="30%">
            <el-form ref="form" :model="form">
                <el-form-item>
                    <div style="float: left; width: 60px; text-align: center;">
                        <span solt="label" class="item-label">内&nbsp;容</span>
                    </div>
                    <div style="float: left; width: 250px">
                        <el-input v-model="form.title" style="float: left"></el-input>
                    </div>
                </el-form-item>
                <el-form-item>
                    <div style="float: left; width: 60px; text-align: center;">
                        <span solt="label" class="item-label">状&nbsp;态</span>
                    </div>
                    <div style="float: left; width: 250px">
                        <el-button @click="changestatus">{{ form.status }}</el-button>
                    </div>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="putstatus = false">取 消</el-button>
                <el-button type="primary" @click="putEvent">确 定</el-button>
            </span>
        </el-dialog>

        <!--删除提示框-->
        <el-dialog title="提示" :visible.sync="delstatus" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delstatus = false">取 消</el-button>
                <el-button type="primary" @click="delEvent">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import Schart from 'vue-schart';
    import bus from '../common/bus';
    export default {
        name: 'dashboard',
        data() {
            return {
                name: localStorage.getItem('nkx_username'),
                views: 0,
                message: 0,
                blogsums: 0,
                lasttime: '',
                addstatus: false,
                putstatus: false,
                delstatus: false,
                todoList: [],
                data1: [],
                data2: [],
                form: {
                    id: -1,
                    title: '',
                    status: ''
                },
                options: {
                    title: '最近七天每天的用户访问量',
                    showValue: true,
                    fillColor: 'rgb(45, 140, 240)',
                    bottomPadding: 30,
                    topPadding: 30
                },
                options2: {
                    title: '最近七天用户访问增长趋势',
                    fillColor: '#FC6FA1',
                    axisColor: '#008ACD',
                    contentColor: '#EEEEEE',
                    bgColor: '#F5F8FD',
                    bottomPadding: 30,
                    topPadding: 30
                }
            }
        },
        components: {
            Schart
        },
        computed: {
            role() {
                return this.name === 'admin' ? '超级管理员' : '普通用户';
            }
        },
        created(){
            //this.handleListener();
            //this.changeDate();
            this.sumcount();
            this.visinit()
            this.todoinit()
        },
        activated(){
            this.handleListener();
        },
        deactivated(){
            window.removeEventListener('resize', this.renderChart);
            bus.$off('collapse', this.handleBus);
        },
        methods: {
            // 首页展示
            sumcount(){
                var url = this.HOST + 'countview'
                this.$axios({
                    method: 'get',
                    url: url
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.views = res.data.data.views
                        this.message = res.data.data.message
                        this.blogsums = res.data.data.blogsums
                        this.lasttime = res.data.data.time
                    } else {
                        this.$message.error(this.data.msg)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            },
            // 修改时间
            changeDate(){
                const now = new Date().getTime();
                this.data.forEach((item, index) => {
                    const date = new Date(now - (6 - index) * 86400000);
                    item.name = `${date.getFullYear()}/${date.getMonth()+1}/${date.getDate()}`
                })
            },
            // 修改数据2
            handleListener(){
                bus.$on('collapse', this.handleBus);
                // 调用renderChart方法对图表进行重新渲染
                window.addEventListener('resize', this.renderChart)
            },
            handleBus(msg){
                setTimeout(() => {
                    this.renderChart()
                }, 300);
            },
            renderChart(){
                this.$refs.bar.renderChart();
                this.$refs.line.renderChart();
            },
            // 查看事件
            todoinit(){
                var url = this.HOST + 'todolist'
                this.$axios({
                    method: 'get',
                    url: url,
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.todoList = res.data.data
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            },
            // 添加
            addList(){
                this.form = {title: ''}
                this.addstatus = true
            },
            addEvent(){
                var url = this.HOST + 'todolist'
                this.$axios({
                    method: 'post',
                    url: url,
                    data: this.form
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.$message.success(res.data.msg)
                        this.addstatus = false
                        this.todoinit()
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            },
            // 编辑
            putList(index, row){
                console.log(row)
                this.idx = index
                this.form = {
                    id: row.id,
                    title: row.title,
                    status: row.status
                }
                this.putstatus = true
            },
            putEvent(){
                var url = this.HOST + 'todolist'
                this.$axios({
                    method: 'put',
                    url: url,
                    data: this.form
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.$message.success(res.data.msg)
                        this.todoinit()
                        this.putstatus = false
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            },
            changestatus(){
                this.form.status = !this.form.status
            },
            // 删除
            delList(index, row){
                this.idx = index
                this.form = {
                    id: row.id
                }
                this.delstatus = true
            },
            delEvent(){
                var url = this.HOST + 'todolist'
                this.$axios({
                    method: 'delete',
                    url: url,
                    data: this.form.id
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.$message.success(res.data.msg)
                        this.todoinit()
                        this.delstatus = false
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            },
            visinit(){
                var url = this.HOST + 'visitor'
                this.$axios({
                    method: 'get',
                    url: url
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.data1 = res.data.data
                        this.data2 = res.data.data2
                        console.log(this.data1, this.data2)
                        this.handleListener()
                    } else {
                        console.log(res.data.msg)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            }
        }
    }
</script>


<style scoped>
    .el-row {
        margin-bottom: 20px;
    }

    .grid-content {
        display: flex;
        align-items: center;
        height: 100px;
    }

    .grid-cont-right {
        flex: 1;
        text-align: center;
        font-size: 14px;
        color: #999;
    }

    .grid-num {
        font-size: 30px;
        font-weight: bold;
    }

    .grid-con-icon {
        font-size: 50px;
        width: 100px;
        height: 100px;
        text-align: center;
        line-height: 100px;
        color: #fff;
    }

    .grid-con-1 .grid-con-icon {
        background: rgb(45, 140, 240);
    }

    .grid-con-1 .grid-num {
        color: rgb(45, 140, 240);
    }

    .grid-con-2 .grid-con-icon {
        background: rgb(100, 213, 114);
    }

    .grid-con-2 .grid-num {
        color: rgb(45, 140, 240);
    }

    .grid-con-3 .grid-con-icon {
        background: rgb(242, 94, 67);
    }

    .grid-con-3 .grid-num {
        color: rgb(242, 94, 67);
    }

    .user-info {
        display: flex;
        align-items: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #ccc;
        margin-bottom: 20px;
    }

    .user-avator {
        width: 120px;
        height: 120px;
        border-radius: 50%;
    }

    .user-info-cont {
        padding-left: 50px;
        flex: 1;
        font-size: 14px;
        color: #999;
    }

    .user-info-cont div:first-child {
        font-size: 30px;
        color: #222;
    }

    .user-info-list {
        font-size: 14px;
        color: #999;
        line-height: 25px;
    }

    .user-info-list span {
        margin-left: 70px;
    }

    .mgb20 {
        margin-bottom: 20px;
    }

    .todo-item {
        font-size: 14px;
    }

    .todo-item-del {
        text-decoration: line-through;
        color: #999;
    }

    .schart {
        width: 100%;
        height: 300px;
    }

</style>
