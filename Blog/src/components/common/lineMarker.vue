<template>
    <div>
        <div :class="className" :id="id" :style="{height:height,width:width}" ref="myEchart">
        </div>
    </div>
</template>

<script>
    import bus from './bus';
    import echarts from 'echarts'
    import resize from './resize'

export default {
  mixins: [resize],
  props: {
    memory:{
        type: Object,
        default: function(){
            return{
                free:[],
                total:[],
                used:[]
            }
        }
    },
    create_time:Array,
    className: {
      type: String,
      default: 'chart1'
    },
    id: {
      type: String,
      default: 'chart1'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '400px'
    }
  },
  data() {
    return {
        chart1: null,
        option: {}
    }
  },
  watch:{
    create_time: {
        handler(newValue, oldValue) {
            if (this.chart1) {
                if (newValue[0] != oldValue[0]) {
                    const xData = this.create_time;
                    var data1 = this.memory.used;
                    var data2 = this.memory.free;
                    var data3 = this.memory.total;
                    // 之前的data
                    var dataZoom = this.option.dataZoom

                    // 获取的option
                    this.option = this.chart1.getOption()
                    //console.log(this.option.dataZoom[0].start,this.option.dataZoom[0].end,this.option.dataZoom[0].height,this.option.dataZoom[0].bottom)
                    //console.log(this.option.dataZoom[1].start,this.option.dataZoom[1].end,this.option.dataZoom[1].height)
                    dataZoom[0].start = this.option.dataZoom[0].start
                    dataZoom[0].end = this.option.dataZoom[0].end
                    this.option.dataZoom = dataZoom;
                    this.option.xAxis[0].data = xData;
                    this.option.series[0].data = data3;
                    this.option.series[1].data = data1;
                    this.option.series[2].data = data2;
                    this.chart1.clear()
                    this.chart1.setOption(this.option);
                    //this.chart4.resize();
                }
            }
        }
    }
  },
  created(){
    var selfs = this;
        bus.$on('collapse', msg => {
            selfs.inits()
        });
    },
  mounted() {
    setTimeout(() => {
        this.initChart()
    }, 500)
  },
  beforeDestroy() {
    if (!this.chart1) {
        return
    }
        this.chart1.dispose()
        this.chart1 = null
    },
    methods: {
        inits(){
            setTimeout(() => {
                self.chart1 = echarts.init(document.getElementById(this.id));
                self.chart1.resize();
            }, 500)
        },
        initChart() {
            //this.chart1 = echarts.init(document.getElementById(this.id))
            this.chart1 = echarts.init(this.$refs.myEchart);
            const xData = this.create_time;
            var data3 = this.memory.total;
            var data1 = this.memory.used;
            var data2 = this.memory.free;
            this.option = 
                {
                    // 背景颜色
                    backgroundColor: '#394056',
                    // 标题
                    title: {
                        top: 20,
                        text: '内存信息',
                        textStyle: {
                            fontWeight: 'normal',
                            fontSize: 16,
                            color: '#F1F1F3'
                        },
                        left: '1%'
                    },
                    //显示线
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            lineStyle: {
                                color: '#57617B'
                                //color: '#ffffff'
                            }
                        }
                    },
                    // 标签 显示
                    legend: {
                        top: 20,
                        icon: 'rect',
                        itemWidth: 14,
                        itemHeight: 10,
                        itemGap: 13,
                        data: ['total', 'used', 'free'],
                        right: '4%',
                        textStyle: {
                            fontSize: 12,
                            color: '#F1F1F3'
                        }
                    },
                    // 显示图边框大小
                    grid: {
                        top: 100,
                        left: '2%',
                        right: '2%',
                        borderWidth: 0,
                        bottom: '80',
                        containLabel: true
                    },
                    // X轴数据
                    xAxis: [{
                        type: 'category',
                        boundaryGap: false,
                        axisLine: {
                            lineStyle: {
                                color: '#57617B'
                            }
                        },
                        data: xData
                    }],
                    // Y轴数据
                    yAxis: [{
                        type: 'value',
                        name: '(m)',
                        axisTick: {
                            show: false
                        },
                        axisLine: {
                            lineStyle: {
                            color: '#57617B'
                            }
                        },
                        // y轴字体
                        axisLabel: {
                            margin: 10,
                            textStyle: {
                                fontSize: 14
                            }
                        },
                        splitLine: {
                            lineStyle: {
                                color: '#57617B'
                            }
                        }
                    }],
                    // 下面的左右拉条
                    dataZoom: [{
                      show: true,
                      height: 30,
                      xAxisIndex: [
                        0
                      ],
                      bottom: 30,
                      start: 10,
                      end: 80,
                      handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
                      handleSize: '110%',
                      handleStyle: {
                        color: '#d3dee5'
                      },
                      textStyle: {
                        color: '#fff' },
                      borderColor: '#90979c'

                    }, {
                      type: 'inside',
                      show: true,
                      height: 15,
                      start: 1,
                      end: 35
                    }],
                    // 三条线数据
                    series: [{
                        name: 'total',
                        type: 'line',
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 5,
                        showSymbol: false,
                        // 线的宽度
                        lineStyle: {
                            normal: {
                                width: 3
                            }
                        },
                        /*
                        线下面的颜色显示
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgba(219, 50, 51, 0.3)'
                                },
                                {
                                    offset: 0.8,
                                    color: 'rgba(219, 50, 51, 0)'
                                }], false),
                                shadowColor: 'rgba(0, 0, 0, 0.1)',
                                shadowBlur: 10
                            }
                        },*/
                        // 圆点样式和大小
                        itemStyle: {
                            normal: {
                                color: 'rgb(219,50,51)',
                                borderColor: 'rgba(219,50,51,0.2)',
                                borderWidth: 12

                            }
                        },
                        //data: [220, 182, 191, 134, 150, 120, 110, 125, 145, 122, 165, 122]
                        data: data3
                    },
                    {
                        name: 'used',
                        type: 'line',
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 5,
                        showSymbol: false,
                        lineStyle: {
                            normal: {
                                width: 1
                            }
                        },
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgba(0, 136, 212, 0.3)'
                                },
                                {
                                    offset: 0.8,
                                    color: 'rgba(0, 136, 212, 0)'
                                }], false),
                                shadowColor: 'rgba(0, 0, 0, 0.1)',
                                shadowBlur: 10
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: 'rgb(0,136,212)',
                                borderColor: 'rgba(0,136,212,0.2)',
                                borderWidth: 12

                            }
                        },
                        //data: [120, 110, 125, 145, 122, 165, 122, 220, 182, 191, 134, 150]
                        data: data1
                    },
                    {
                        name: 'free',
                        type: 'line',
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 5,
                        showSymbol: false,
                        lineStyle: {
                            normal: {
                                width: 1
                            }
                        },
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgba(137, 189, 27, 0.3)'
                                },
                                {
                                    offset: 0.8,
                                    color: 'rgba(137, 189, 27, 0)'
                                }], false),

                                shadowColor: 'rgba(0, 0, 0, 0.1)',
                                shadowBlur: 10
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: 'rgb(137,189,27)',
                                borderColor: 'rgba(137,189,2,0.27)',
                                borderWidth: 12
                            }
                        },
                        //data: [220, 182, 125, 145, 122, 191, 134, 150, 120, 110, 165, 122]
                        data: data2
                    }]
                }
            this.chart1.setOption(this.option)
        },
    }
}
</script>

<style type="text/css">
    .className1{
        height: 400px;
        width: 100%;
    }
    .className2{
        height: 400px;
        width: 100%;
    }
</style>