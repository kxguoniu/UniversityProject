<template>
    <div :class="className" :id="id" :style="{height:height,width:width}"/>
</template>

<script>
import bus from './bus';
import echarts from 'echarts'

export default {
  props: {
    net:{
        type: Object,
        default: function(){
            return{
                netin:[],
                netout:[]
            }
        }
    },
    create_time:Array,
    className: {
      type: String,
      default: 'chart2'
    },
    id: {
      type: String,
      default: 'chart2'
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
      chart2: null,
      option: {}
    }
  },
  watch:{
    create_time: {
        handler(newValue, oldValue) {
            if (this.chart2) {
                if (newValue[0] != oldValue[0]) {
                    const xAxisData = this.create_time;
                    var data = this.net.netout;
                    var data2 = this.net.netin;

                    this.option.xAxis[0].data = xAxisData;
                    this.option.series[0].data = data2;
                    this.option.series[1].data = data;
                    this.chart2.clear()
                    this.chart2.setOption(this.option);
                }
            }
        }
    }
  },
  mounted() {
    setTimeout(() => {
      this.initChart()
      console.log('dayinwo1')
    }, 500)
  },
  created(){
    var selfs = this;
        bus.$on('collapse', msg => {
            selfs.inits()
            console.log('nizuoleshenme')
        });
    },
  beforeDestroy() {
    if (!this.chart2) {
      return
    }
    this.chart2.dispose()
    this.chart2 = null
  },
  methods: {
    inits(){
            setTimeout(() => {
                self.chart2 = echarts.init(document.getElementById(this.id));
                self.chart2.resize();
                console.log('initsss')
            }, 250)
        },
    initChart() {
      this.chart2 = echarts.init(document.getElementById(this.id))

      var xAxisData = []
      var data = []
      var data2 = []
      /*
      for (let i = 0; i < 50; i++) {
        xAxisData.push(i)
        data.push((Math.sin(i / 5) * (i / 5 - 10) + i / 6) * 5)
        data2.push((Math.sin(i / 5) * (i / 5 + 10) + i / 6) * 3)
      }
      */
      xAxisData = this.create_time;
      data = this.net.netout;
      data2 = this.net.netin;
      this.option = 
        {
          backgroundColor: '#08263a',
          grid: {
            top: 80,
            left: '5%',
            right: '5%',
            bottom: '5%',
            containLable: true
          },
          // 中间竖线
          tooltip: {
            trigger: 'axis',
            axisPointer:{
              lineStyle: {
                color: '#57617B'
              }
            }
          },
          title: {
            top: 20,
            text: '流量信息',
            textStyle: {
                fontWeight: 'normal',
                fontSize: 16,
                color: '#F1F1F3'
            },
            left: '1%'
            },
            legend: {
                top: 30,
                icon: 'rect',
                itemWidth: 14,
                itemHeight: 10,
                itemGap: 13,
                data: ['netin', 'netout'],
                right: '4%',
                textStyle: {
                    fontSize: 12,
                    color: '#F1F1F3'
                }
            },
          xAxis: [{
            type: 'category',
            // 下面线的显示和颜色,上面的数据
            show: true,
            axisLine: {
                  lineStyle: {
                      color: '#57617B'
                  }
              },
            data: xAxisData
          },
          // 上面的坐标显示和下面的数据
          {
            show: false,
            data: xAxisData
          }],
          // 块状颜色
          visualMap: {
            show: false,
            min: 0,
            max: 50,
            dimension: 0,
            inRange: {
              color: ['#4a657a', '#308e92', '#b1cfa5', '#f5d69f', '#f5898b', '#ef5055']
            }
          },
          yAxis: {
            type: 'value',
            name: '(kb)',
            axisLine: {
              show: true,
              lineStyle: {
                color: '#57617B'
              }
            },
            axisLabel: {
              textStyle: {
                color: '#4a657a'
              }
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: '#08263f'
              }
            },
            axisTick: {
              show: false
            }
          },
          series: [{
            name: 'netin',
            type: 'bar',
            data: data2,
            z: 1,
            itemStyle: {
              normal: {
                opacity: 0.4,
                barBorderRadius: 5,
                shadowBlur: 3,
                shadowColor: '#111'
              }
            }
          },/*
          {
            name: 'netout',
            type: 'line',
            data:data,
            z: 2,
            //showSymbol: false,
            animationDelay: 0,
            animationEasing: 'linear',
            animationDuration: 1200,
            // 阴影线颜色
            lineStyle: {
              normal: {
                color: 'transparent'
              }
            },
            // 阴影颜色和样式
            areaStyle: {
              normal: {
                color: '#08263a',
                shadowBlur: 50,
                shadowColor: '#000'
              }
            }
          },*/
          {
            name: 'netout',
            type: 'bar',
            data:data,
            xAxisIndex: 1,
            z: 3,
            itemStyle: {
              normal: {
                barBorderRadius: 50,
                shadowColor: '#111',
              }
            }
          }],
          animationEasing: 'elasticOut',
          animationEasingUpdate: 'elasticOut',
          animationDelay(idx) {
            return idx * 20
          },
          animationDelayUpdate(idx) {
            return idx * 20
          }
        }
      this.chart2.setOption(this.option)
    }
  }
}
</script>
