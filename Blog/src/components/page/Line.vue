<template>
  <div class="chart-container">
    <div style="float: left; width: 100%; height: 500px;">
        <line-marker />
    </div>
    <div style="float: left; width: 100%; height: 500px;">
        <keyboard />
    </div>
    <div style="float: left; width: 100%; height: 500px;">
        <mix-chart />
    </div>
  </div>
</template>

<script>
import lineMarker from '@/components/common/lineMarker'
import keyboard from '@/components/common/keyboard'
import mixChart from '@/components/common/mixChart'
//height="100%" width="100%"
export default {
  name: 'LineChart',
  components: { lineMarker, keyboard, mixChart }
}
</script>

<style scoped>
.chart-container{
  position: relative;
  width: 100%;
  height: calc(100vh - 84px);
}
</style>