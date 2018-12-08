<template>
    <div class="asd" v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(0, 0, 0, 0.8)">
        <el-row v-if="!loading" :gutter="20" class="montorrow">
            <keyboard :net="net" :create_time="create_time" :height="height" :width="width" />
        </el-row>
        <el-row v-if="!loading" :gutter="20" class="montorrow">
            <line-marker :memory="memory" :create_time="create_time" :height="height" :width="width" />
        </el-row>
        <el-row v-if="!loading" :gutter="20" class="montorrow">
            <mix-chart :cpu="cpu" :create_time="create_time" :height="height" :width="width" />
        </el-row>
        <el-row v-if="!loading" :gutter="20" class="montorrow">
            <Load :load="load" :create_time="create_time" :height="height" :width="width" />
        </el-row>
    </div>
</template>

<script>
    import bus from '../common/bus';
    import lineMarker from '@/components/common/lineMarker'
    import keyboard from '@/components/common/keyboard'
    import mixChart from '@/components/common/mixChart'
    import Load from '@/components/common/Load'
    export default {
        name: 'LineChart',
        data(){
            return{
                net:{},
                load:{},
                cpu:{},
                memory:{},
                create_time:[],
                height: '550px',
                width: '100%',
                loading: true,
                sort: true,
                timer: null,
            }
        },
        components: { keyboard, lineMarker, mixChart, Load },
        created(){
            this.loading = true
            this.init()
            this.loading = false
            this.Loop()
        },
        methods:{
            init(){
                this.sort = !this.sort
                let url = this.HOST + 'system'
                this.$axios({
                    method: 'get',
                    url: url,
                    params:{
                        limit: 60,
                        sort: this.sort
                    }
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.net = res.data.data.net;
                        this.load = res.data.data.load;
                        this.cpu = res.data.data.cpu;
                        this.memory = res.data.data.memory;
                        this.create_time = res.data.data.create_time;
                        //console.log(this.net,this.load,this.cpu,this.memory,this.create_time)
                    } else {
                        this.$message.error(res.data.msg)
                    }
                })
                .catch(error => {
                    this.loading = false
                    this.$message.error('请求失败')
                    console.log(error)
                })
            },
            Loop(){
                this.timer = setInterval(this.init, 60000)
            }
        },
        beforeDestroy(){
            clearInterval(this.timer)
            this.timer = null
        },
    }
</script>

<style scoped>
    .montorrow{
        margin-left: 20px !important;
        margin-right: 10px !important;
        text-align: center;
        height: 600px;
        width: 98%;
    }
    .asd{
        height: 100%;
    }
</style>
