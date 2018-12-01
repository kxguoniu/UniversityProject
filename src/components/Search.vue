<template lang="html">
    <div class="search">
        <div>
            <el-autocomplete
                class="search-input"
                v-model="state"
                :fetch-suggestions="querySearchAsync"
                placeholder="搜索..."
                @select="handleSelect"
            ></el-autocomplete>
        </div>
    </div>
</template>

<script type="text/javascript">
    //select-when-unmatched
    export default{
        name:"",
        data(){
            return{
                restaurants: [],
                state: '',
                timeout: null,
            }
        },
        methods:{
            // 返回查询结果
            querySearchAsync(queryString, callback){
                clearTimeout(this.timeout);
                this.timeout = setTimeout(() => {
                    var url = this.HOST + 'search'
                    this.$axios({
                        method: 'get',
                        url: url,
                        params: {
                            title: queryString
                        }
                    })
                    .then(res => {
                        if (res.data.status == 0) {
                            this.restaurants = res.data.data
                            callback(this.restaurants)
                        } else {
                            this.$message.error(res.data.msg)
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
                }, 800 * Math.random());
            },
            // 查询结果
            handleSelect(item) {
                this.$router.push({name:'BlogDetail', params:{id:item.id}})
            }
        },
    }
</script>

<style type="text/css" scoped>
    .search {
        height: 47px;
        background-color: #3D4450;
        padding-top: 5px;
        padding-left: 1%;
        padding-right: 1%;
        margin-bottom: 30px;
    }
    .search-input {
        width: 100%;
        font-size: 25px;
    }
</style>