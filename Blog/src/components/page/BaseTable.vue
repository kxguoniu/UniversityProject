<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-cascades"></i> 博文列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-button type="primary" icon="delete" class="handle-del mr10" @click="delAll">批量删除</el-button>
                <el-select v-model="select" clearable placeholder="请选择" class="handle-select mr10">
                    <el-option
                        v-for="item in options"
                        :key="item.name"
                        :label="item.name"
                        :value="item.value">
                    </el-option>
                </el-select>
                <el-input v-model="select_word" placeholder="筛选关键词" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="search" @click="getList">搜索</el-button>
            </div>
            <el-table :data="blogList" border class="table" ref="multipleTable" @selection-change="handleSelectionChange" @sort-change="Soft">
                <el-table-column type="selection" width="55" align="center"></el-table-column>
                <el-table-column prop="create_time" label="日期" sortable="custom" width="180">
                </el-table-column>
                <el-table-column prop="author" label="作者" width="80">
                </el-table-column>
                <el-table-column prop="category" label="分类" width="80">
                </el-table-column>
                <el-table-column prop="views" label="流量" sortable="custom" width="80">
                </el-table-column>
                <el-table-column prop="weight" label="权重" sortable="custom" width="100">
                    <template slot-scope="scope">
                        <el-rate
                            v-model="scope.row.weight"
                            disabled
                            :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                            :low-threshold="1"
                            :high-threshold="3"
                            style="margin-top:4px;">
                        </el-rate>
                    </template>
                </el-table-column>
                <el-table-column prop="title" label="标题" width="auto">
                </el-table-column> 
                <el-table-column label="操作" width="120" align="center">
                    <template slot-scope="scope">
                        <el-tooltip class="item" effect="dark" content="编辑" placement="bottom">
                            <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)"></el-button>
                        </el-tooltip>
                        <router-link :to="'/edit/'+ scope.row.id ">
                            <el-tooltip class="item" effect="dark" content="修改" placement="bottom">
                                <el-button type="text" icon="el-icon-lx-edit" style="color: blue;"></el-button>
                            </el-tooltip>
                        </router-link>
                        <el-tooltip class="item" effect="dark" content="下载" placement="bottom">
                            <el-button type="text" icon="el-icon-lx-down" class="download" @click="handleDownload(scope.$index, scope.row)"></el-button>
                        </el-tooltip>
                        <el-tooltip class="item" effect="dark" content="删除" placement="bottom">
                            <el-button type="text" icon="el-icon-delete" class="red" @click="handleDelete(scope.$index, scope.row)"></el-button>
                        </el-tooltip>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination
                    background
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[1, 5, 10, 20, 50, 100, 200]"
                    :page-size="20"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total">
                </el-pagination>
            </div>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="form" :model="form" label-width="50px">
                <el-form-item label="标题">
                    <el-input v-model="form.title"></el-input>
                </el-form-item>
                <el-form-item label="权重">
                    <el-rate
                        v-model="form.weight"
                        :max="3"
                        :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                        :low-threshold="1"
                        :high-threshold="3"
                        style="margin-top:8px;">
                    </el-rate>
                </el-form-item>
                <el-form-item label="分类">
                    <el-select v-model="form.category" clearable placeholder="请选择" class="selectcate">
                        <el-option
                            v-for="item in categorylist"
                            :key="item.name"
                            :label="item.name"
                            :value="item.name">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 删除提示框 -->
        <el-dialog title="提示" :visible.sync="delVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteRow">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: 'basetable',
        data() {
            return {
                blogList:[],     //博文列表
                options: [
                    {name:'作者', value:'author'},
                    {name:'分类', value:'category'},
                    {name:'流量', value:'views'},
                    {name:'权重', value:'weight'},
                    {name:'标题', value:'title'},
                    {name:'摘要', value:'digested'},
                    {name:'日期', value:'time'},
                ],
                total: 0,   //总数量
                listQuery:{
                    page: 1,
                    limit: 20
                },
                currentPage: 1,     //当前页
                tagList:[],         //标签列表
                categorylist: [],   //分类列表
                deleteid: -1,       //单选删除的博文id
                tableData: [],
                cur_page: 1,
                select_cate: '',
                del_list: [],       // 多选删除列表
                is_search: false,
                editVisible: false, // 编辑弹出框控制
                delVisible: false,  // 删除提示框控制
                form: {
                    title: '',
                    weight: '',
                    category: '',
                    id: -1,
                },
                idx: -1,             // 当前显示的第几行数据
                select: '',          // 筛选条件
                select_word: '',    // 筛选关键词
            }
        },
        created() {
            this.init();
            var url = this.HOST + 'taglist'
            this.$axios({
                url: url,
                method: 'get',
            })
            .then(res => {
                this.tagList = res.data.data.tag;
                this.categorylist = res.data.data.category;
            })
        },
        methods: {
            // 获取博文列表
            Soft(val){
                var soft = val.order
                var colum = val.prop
                var softlist = this.blogList
                var length = softlist.length
                var middle
                for (let i=0; i<length; i++){
                    for (let j=i; j<length; j++){
                        if (softlist[i][colum] > softlist[j][colum]){
                            if (soft == "descending"){
                                middle = softlist[j]
                                softlist[j] = softlist[i]
                                softlist[i] = middle
                            }
                        }else{
                            if (soft == "ascending"){
                                middle = softlist[j]
                                softlist[j] = softlist[i]
                                softlist[i] = middle
                            }
                        }
                    }
                }
                for (let i=0; i<length; i++){
                    Vue.set(this.blogList, i, softlist[i])
                }
            },
            init() {
                let url = this.HOST + 'bloglist'
                this.$axios({
                    method: 'get',
                    url: url,
                    params:{
                        search: 'category',
                        flag: '1', //分类
                        page: this.listQuery.page,
                        limit: this.listQuery.limit,
                    }
                })
                .then(res => {
                    if (res.data.status == 0) {
                        this.blogList = res.data.data;
                        this.total = res.data.total;
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error =>{
                    console.log(error);
                })
            },
            // 搜索博文
            getList(){
                if (this.select == '' || this.select_word == ''){
                    this.init()
                    return
                }
                let url = this.HOST + 'search'
                this.$axios({
                    method: 'put',
                    url: url,
                    params:{
                        page: this.listQuery.page,
                        limit: this.listQuery.limit,
                        select: this.select,
                        value: this.select_word,
                    }
                })
                .then(res => {
                    if (res.data.status == 0) {
                        this.blogList = res.data.data;
                        this.total = res.data.total;
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error =>{
                    console.log(error);
                })
            },
            // 改变页面显示数
            handleSizeChange(val){
                this.listQuery.limit = val;
                this.listQuery.page = 1;
                this.getList()
            },
            // 改变页数
            handleCurrentChange(val) {
                this.listQuery.page = val;
                this.getList() // 改变数据
            },
            formatter(row, column) {
                return row.address;
            },
            filterTag(value, row) {
                return row.tag === value;
            },
            // 准备编辑数据
            handleEdit(index, row) {
                this.idx = index;
                const item = this.blogList[index];
                this.form = {
                    title: item.title,
                    category: item.category,
                    weight: item.weight,
                    id: item.id,
                }
                this.editVisible = true;
            },
            // 下载文件
            handleDownload(index, row){
                var url = this.HOST + 'download'
                window.location.href = url + '?id=' + row.id
            },
            // 准备删除数据
            handleDelete(index, row) {
                this.idx = index;
                this.delVisible = true;
                this.deleteid = row.id;
            },
            // 多选删除
            delAll() {
                const length = this.del_list.length;
                let url = this.HOST + 'blog';
                let arr = {};
                for (let i = 0; i < length; i++) {
                    arr[i] = this.del_list[i]['id'];
                }
                this.$axios({
                    method: 'delete',
                    url: url,
                    params: {
                        ids: arr,
                    }
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.$message.success(`删除了 ${length} 行数据`);
                        this.del_list = [];
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error => {
                    console.log(error);
                })
            },
            // 多选保存
            handleSelectionChange(val) {
                this.del_list = val;
            },
            // 保存编辑
            saveEdit() {
                let url = this.HOST + 'blog';
                this.$axios({
                    method: 'put',
                    url: url,
                    params: {
                        flag: 'head',
                    },
                    data: this.form
                })
                .then(res => {
                    console.log(res.data);
                    if (res.data.status == 0){
                        this.blogList[this.idx]['title'] = this.form['title'];
                        this.blogList[this.idx]['category'] = this.form['category'];
                        this.blogList[this.idx]['weight'] = this.form['weight'];
                        this.$set(this.blogList);
                        this.$message.success(`修改第 ${this.idx+1} 行成功`);
                        this.editVisible = false;
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            },
            // 确定删除
            deleteRow(){
                let url = this.HOST + 'blog'
                this.$axios({
                    method: 'delete',
                    url: url,
                    params: {
                        id: this.deleteid,
                    }
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.blogList.splice(this.idx, 1);
                        this.$message.success('删除成功');
                        this.total = this.total - 1;
                        this.delVisible = false;
                    } else {
                        this.$message.error(res.data.msg)
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
    .pagination{
        text-align: center;
    }
    .pagination el-pagination__sizes{
        text-align: center;
    }
    .handle-box {
        margin-bottom: 20px;
    }
    .handle-select {
        width: 100px;
    }
    .handle-input {
        width: 200px;
        display: inline-block;
    }
    .del-dialog-cnt{
        font-size: 16px;
        text-align: center
    }
    .table{
        width: 100%;
        font-size: 14px;
    }
    .red{
        color: #ff0000;
        margin: 0 0 !important;
    }
    .download{
        margin: 0 0;
    }
</style>
