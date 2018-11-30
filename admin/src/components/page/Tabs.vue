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
                        <el-button type="primary" @click="handleAll(0,0)">全部标为已读</el-button>
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
                            <el-button type="danger" @click="handleAll(1,2)">删除全部</el-button>
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
                            <el-button type="danger" @click="handleAll(2,1)">清空回收站</el-button>
                        </div>
                    </template>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script>
    import bus from '../common/bus';
    export default {
        name: 'tabs',
        data() {
            return {
                message: 'first',       // 点击改变选项卡
                showHeader: false,
                msglist: [],            // 信息列表
                lists: []
            }
        },
        created(){
            this.init()
        },
        methods: {
            // 数据请求
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
            // 信息修改
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
            // 数据筛选
            datatwo(val){
                return this.lists.filter((d) => {
                    if (d.status == val) {
                        return d
                    }
                })
            },
            // 已读
            handleRead(val) {
                for (let i = 0; i < this.lists.length; i++) {
                    if (val.id == this.lists[i].id) {
                        this.lists[i].status = 1
                    }
                }
                this.submit(val.id,1)
            },
            // 删除
            handleDel(val) {
                for (let i = 0; i < this.lists.length; i++) {
                    if (val.id == this.lists[i].id) {
                        this.lists[i].status = 2
                    }
                }
                this.submit(val.id,2)
                bus.$emit('message', this.datatwo(2).length)
            },
            // 回收
            handleRestore(val) {
                for (let i = 0; i < this.lists.length; i++) {
                    if (val.id == this.lists[i].id) {
                        this.lists[i].status = 1
                    }
                }
                this.submit(val.id,1)
                bus.$emit('message', this.datatwo(2).length)
            },
            // 全部操作
            handleAll(start, end){
                var dellist = this.datatwo(start)
                for (let i = 0; i < this.lists.length; i++) {
                    for (let j = 0; j < dellist.length; j++) {
                        if (dellist[j].id == this.lists[i].id) {
                            this.lists[i].status = end
                        }
                    }
                }
                dellist.filter((d) => {
                    this.submit(d.id, end)
                })
                bus.$emit('message', this.datatwo(2).length)
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

