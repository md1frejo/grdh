<script setup>
 import { ref, onMounted, defineComponent, h } from 'vue'
 import { Line } from 'vue-chartjs'
 import {
   Chart as ChartJS,
   Title,
   Tooltip,
   Legend,
   LineElement,
   LinearScale,
   PointElement,
   CategoryScale
 } from 'chart.js'

 ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale)

 const ticks = ref([])

 onMounted(async () => {
   try {
     const response = await fetch('/ticks.json')
     if (!response.ok) throw new Error('Failed to load ticks.json')
     const json = await response.json()
     ticks.value = json
   } catch (err) {
     console.error('Error loading ticks.json:', err)
   }
 })

 const getStockName = (entry) => Object.keys(entry)[0]
 const isNoData = (entry) => entry[getStockName(entry)] === 'nodata'

 const formatChartData = (entry) => {
   const stockName = getStockName(entry)
   const prices = entry[stockName]
   return {
     labels: prices.map((_, i) => i),
     datasets: [{
       data: prices,
       borderColor: 'darkblue',
       tension: 0.4,
       fill: false
     }]
   }
 }

 const LineChart = defineComponent({
   props: ['chartData'],
   setup(props) {
     return () =>
       h(Line, {
         data: props.chartData,
         options: {
           responsive: true,
           elements: {
             point: { radius: 0 }
           },
           plugins: {
             legend: { display: false },
             tooltip: { enabled: false }
           },
           scales: {
             x: { display: false },
             y: { display: false }
           }
         }
       })
   }
 })
</script>

<template>
  <div class="p-4">
    <h1 class="font-radley text-browngrad-300 text-center text-st2">
      candidates history</h1>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div
        v-for="(entry, index) in ticks"
        :key="index"
        class="p-4 border rounded shadow">
        <div class="text-browngrad-100 bg-antiquewhiteg-900 font-radley text-headlinecard-500 text-left text-st3">{{ getStockName(entry) }}</div>
        <div v-if="isNoData(entry)" class="text-gray-500">No data</div>
        <LineChart v-else :chart-data="formatChartData(entry)" />
      </div>
    </div>
  </div>
</template>

<style scoped>
 /* Add any additional styling here */
</style>
