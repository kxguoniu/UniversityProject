<template>
    <div class="">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-copy"></i> 系统消息</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-tabs v-model="message">
                <el-tab-pane :label="`未读消息(${datatwo(0).length})`" name="first">
                    <el-table :data="datatwo(0)" :show-header="false" style="width: 100%">
                        <el-table-column>
                            <template slot-scope="scope">
                                <span class="message-title">{{scope.row.content}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="create_time" width="180"></el-table-column>
                        <el-table-column width="120">
                            <template slot-scope="scope">
                                <el-button size="small" @click="handleRead(scope.row)">标为已读</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="handle-row">
                        <el-button type="primary">全部标为已读</el-button>
                    </div>
                </el-tab-pane>
                <el-tab-pane :label="`已读消息(${datatwo(1).length})`" name="second">
                    <template v-if="message === 'second'">
                        <el-table :data="datatwo(1)" :show-header="false" style="width: 100%">
                            <el-table-column>
                                <template slot-scope="scope">
                                    <span class="message-title">{{scope.row.content}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="create_time" width="150"></el-table-column>
                            <el-table-column width="120">
                                <template slot-scope="scope">
                                    <el-button type="danger" @click="handleDel(scope.row)">删除</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <div class="handle-row">
                            <el-button type="danger">删除全部</el-button>
                        </div>
                    </template>
                </el-tab-pane>
                <el-tab-pane :label="`回收站(${datatwo(2).length})`" name="third">
                    <template v-if="message === 'third'">
                        <el-table :data="datatwo(2)" :show-header="false" style="width: 100%">
                            <el-table-column>
                                <template slot-scope="scope">
                                    <span class="message-title">{{scope.row.content}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="create_time" width="150"></el-table-column>
                            <el-table-column width="120">
                                <template slot-scope="scope">
                                    <el-button @click="handleRestore(scope.row)">还原</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <div class="handle-row">
                            <el-button type="danger">清空回收站</el-button>
                        </div>
                    </template>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'tabs',
        data() {
            return {
                message: 'first',       // 点击改变选项卡
                showHeader: false,
                msglist: [],            // 信息列表
                lists: [
                    {
                        id: 1,
                        create_time: '2018-04-19 20:10:00',
                        content: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护',
                        status: 0,
                    },
                    {
                        id: 2,
                        date: '2018-04-19 21:20:00',
                        title: '今晚12点整发大红包，先到先得',
                        status: 1
                    },
                    {
                        id: 3,
                        date: '2018-04-19 20:30:00',
                        title: '【系统通知】该系统将于今晚5点进行升级维护',
                        status: 2
                    },
                    {
                        id: 4,
                        date: '2018-04-19 20:40:00',
                        title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护',
                        status:0
                    }
                ]
            }
        },
        created(){
            this.init()
        },
        methods: {
            init(){
                var url = this.HOST + 'message'
                this.$axios({
                    method: 'get',
                    url: url,
                })
                .then(res => {
                    if (res.data.status == 0) {
                        this.lists = res.data.data
                    } else {
                        this.$message.error(res.data.msg)
                    }
                    console.log(this.msglist)
                })
                .catch(error => {
                    console.log(error)
                })
            },
            submit(msgid,status){
                var url = this.HOST + 'message'
                this.$axios({
                    method: 'post',
                    url: url,
                    params: {
                        msgid: msgid,
                        status: status
                    }
                })
                .then(res => {
                    if (res.data.status == 0) {
                        this.$message.sucess('操作成功')
                        this.msglist = res.data.data
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            },
            datatwo(val){
                return this.lists.filter((d) => {
                    if (d.status == val) {
                        return d
                    }
                })
            },
            handleRead(val) {
                for (let i = 0; i < this.lists.length; i++) {
                    if (val.id == this.lists[i].id) {
                        this.lists[i].status = 1
                    }
                }
                this.submit(val.id,1)
            },
            handleDel(val) {
                for (let i = 0; i < this.lists.length; i++) {
                    if (val.id == this.lists[i].id) {
                        this.lists[i].status = 2
                    }
                }
                this.submit(val.id,2)
            },
            handleRestore(val) {
                for (let i = 0; i < this.lists.length; i++) {
                    if (val.id == this.lists[i].id) {
                        this.lists[i].status = 1
                    }
                }
                this.submit(val.id,1)
            }
        },
        computed: {
            unreadNum(){
                return this.unread.length;
            }
        }
    }

</script>

<style>
.message-title{
    cursor: pointer;
}
.handle-row{
    margin-top: 30px;
}
</style>

