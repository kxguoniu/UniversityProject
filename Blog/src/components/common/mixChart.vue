<template>
    <div :class="className" :id="id" :style="{height:height,width:width}"/>
</template>

<script>
import bus from './bus';
import echarts from 'echarts'

export default {
  props: {
    cpu:{
        type: Object,
        default: function(){
            return{
                uscpu:[],
                sycpu:[]
            }
        }
    },
    create_time:Array,
    className: {
      type: String,
      default: 'chart3'
    },
    id: {
      type: String,
      default: 'chart3'
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
      chart3: null,
      option: {}
    }
  },
  watch:{
    create_time: {
        handler(newValue, oldValue) {
            if (this.chart3) {
                if (newValue[0] != oldValue[0]) {
                    const xData = this.create_time;
                    var data1 = this.cpu.sycpu;
                    var data2 = this.cpu.uscpu;
                    // 之前的data
                    var dataZoom = this.option.dataZoom

                    // 获取的option
                    this.option = this.chart3.getOption()
                    //console.log(this.option.dataZoom[0].start,this.option.dataZoom[0].end,this.option.dataZoom[0].height,this.option.dataZoom[0].bottom)
                    //console.log(this.option.dataZoom[1].start,this.option.dataZoom[1].end,this.option.dataZoom[1].height)
                    dataZoom[0].start = this.option.dataZoom[0].start
                    dataZoom[0].end = this.option.dataZoom[0].end
                    this.option.dataZoom = dataZoom;
                    this.option.xAxis[0].data = xData;
                    this.option.series[0].data = data1;
                    this.option.series[1].data = data2;
                    this.chart3.clear()
                    this.chart3.setOption(this.option);
                    //this.chart4.resize();
                }
            }
        }
    }
  },
  mounted() {
    setTimeout(() => {
        this.initChart()
    }, 500)
  },
  created(){
    var selfs = this;
        bus.$on('collapse', msg => {
            selfs.inits()
        });
    },
  beforeDestroy() {
    if (!this.chart3) {
      return
    }
    this.chart3.dispose()
    this.chart3 = null
  },
  methods: {
    inits(){
            setTimeout(() => {
                self.chart3 = echarts.init(document.getElementById(this.id));
                self.chart3.resize();
            }, 500)
        },
    initChart() {
      this.chart3 = echarts.init(document.getElementById(this.id))
      /*
      const xData = (function() {
        const data = []
        for (let i = 1; i < 57; i++) {
          data.push(i)
        }
        return data
      }())*/
      //console.log(xData)
      //const data1 = [709,1917,2455,2610,1719,1433,1544,3285,5208,3372,2484,4078]
      //const data2 = [9327,1776,507,1200,9800,482,204,1390,1001,951,381,220]
      //const data3 = [1036,3693,2962,3810,2519,1915,1748,4675,6209,4323,2865,4298]
      const data = this.create_time;
      const xData = this.create_time;
      var data3 = [];
      var data1 = this.cpu.sycpu;
      var data2 = this.cpu.uscpu;
      this.option = {
        backgroundColor: '#344b58',
        // 标题
        title: {
          text: 'CPU信息',
          x: '20',
          top: '20',
          //标题字体
          textStyle: {
            color: '#fff',
            fontSize: '22'
          },
          subtextStyle: {
            color: '#90979c',
            fontSize: '16'
          }
        },
        // 显示线
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            textStyle: {
              color: '#fff'
            }
          }
        },
        // 图片大小
        grid: {
          left: '5%',
          right: '2%',
          borderWidth: 0,
          top: 100,
          bottom: 95,
          textStyle: {
            color: '#fff'
          }
        },
        // 标签显示
        legend: {
          //x: '5%',
          right: '5%',
          top: '30',
          textStyle: {
            color: '#90979c'
          },
          //data: ['female', 'male', 'average']
          data: ['user', 'sys', 'total']
        },
        calculable: true,
        xAxis: [{
          type: 'category',
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          },
          splitLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          splitArea: {
            show: false
          },
          axisLabel: {
            interval: 0

          },
          data: xData
        }],
        yAxis: [{
          type: 'value',
          name: '(%)',
          splitLine: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            interval: 0
          },
          splitArea: {
            show: false
          }
        }],
        // 下面显示框
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
        series: [{
          //name: 'female',
          name: 'sys',
          type: 'bar',
          stack: 'total',
          barMaxWidth: 35,
          barGap: '10%',
          itemStyle: {
            normal: {
              color: 'rgba(255,144,128,1)',
              label: {
                show: true,
                textStyle: {
                  color: '#fff'
                },
                position: 'insideTop',
                formatter(p) {
                  return p.value > 0 ? p.value : ''
                }
              }
            }
          },
          data: data1
        },
        {
          //name: 'male',
          name: 'user',
          type: 'bar',
          stack: 'total',
          itemStyle: {
            normal: {
              color: 'rgba(0,191,183,1)',
              barBorderRadius: 0,
              label: {
                show: true,
                position: 'top',
                formatter(p) {
                  return p.value > 0 ? p.value : ''
                }
              }
            }
          },
          data: data2
        }, {
          //name: 'average',
          name: 'total',
          type: 'line',
          stack: 'total',
          // 圆点点大小
          symbolSize: 10,
          symbol: 'circle',
          itemStyle: {
            normal: {
              color: 'rgba(252,230,48,1)',
              barBorderRadius: 0,
              // 每一点显示数字
              label: {
                show: true,
                position: 'top',
                formatter(p) {
                  return p.value > 0 ? p.value : ''
                }
              }
            }
          },
          data: data3
        }
        ]
      }
      this.chart3.setOption(this.option)
    }
  }
}
</script>
