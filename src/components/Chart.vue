<script setup>
 import { ref, onMounted, defineComponent, h } from 'vue'
 import { Line } from 'vue-chartjs'
 import tdate from '../../public/tdate.json';
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
 const selectedChart = ref(
   { data:null, name:''}
 )
 const showModal = ref(false)

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

 const openChart = (entry) => {
   selectedChart.value = {
     data: formatChartData(entry),
     name: getStockName(entry)
   } 
   showModal.value = true
 }

 const closeModal = () => {
   showModal.value = false
   selectedChart.value = { data:null,name:  ''}
 }

 const LineChart = defineComponent({
   props: ['chartData'],
   setup(props) {
     return () =>
       h(Line, {
         data: props.chartData,
         options: {
           responsive: true,
           elements: { point: { radius: 0 } },
           plugins: { legend: { display: false }, tooltip: { enabled: false } },
           scales: { x: { display: false }, y: { display: false } }
         }
       })
   }
 })
</script>

<template>
  <div class="p-4">
    <h1 class="font-radley text-browngrad-300 text-center text-st2">
      trend since {{ tdate.td }}:
    </h1>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div
        v-for="(entry, index) in ticks"
        :key="index"
        class="p-4 border rounded shadow cursor-pointer"
        @click="!isNoData(entry) && openChart(entry)"
      >
        <div class="text-browngrad-100 bg-antiquewhiteg-900 font-radley text-headlinecard-500 text-left text-st3">
          {{ getStockName(entry) }}
        </div>
        <div v-if="isNoData(entry)" class="text-gray-500">No data</div>
        <LineChart v-else :chart-data="formatChartData(entry)" />
      </div>
    </div>

    <!-- Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeModal">
      <div class="bg-white p-4 rounded shadow-lg w-[90%] max-w-3xl">
	<div class="flex justify-between items-center mb-2">
	  <h2 class="text-lg font-semibold text-gray-800">
            {{ selectedChart.name }}
	  </h2>
          <button class="float-right text-gray-700" @click="closeModal">✕</button>
	</div>
          <div class="mt-4" style="height: 300px;">
            <LineChart v-if="selectedChart.data" :chart-data="selectedChart.data" />
          </div>
	</div>
      </div>
    </div>
</template>

<style scoped>
 /* Optional: customize modal appearance */
</style>
