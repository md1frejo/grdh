<script setup>
 import { ref, onMounted, defineComponent, h } from 'vue'
 import { Line } from 'vue-chartjs'
 import tdate from '../../public/tdate.json'
 import dayjs from 'dayjs'
 import zoomPlugin from 'chartjs-plugin-zoom'
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

 const trendMap = ref({})
 
 ChartJS.register(
   Title,
   Tooltip,
   Legend,
   LineElement,
   LinearScale,
   PointElement,
   CategoryScale,
   zoomPlugin
 )

 const { sdate2, tops } =  defineProps({
   sdate2: String,
   tops: Object
 })

 console.log(tops)
 
 const chartRef = ref(null)  // GLOBAL!
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

     const first20 = {}

     for (const [key, obj] of Object.entries(ticks.value)) {
       const valuesArray = Object.values(obj)
       first20[key] = valuesArray.slice(0, 20)
     }
     
   } catch (err) {
     console.error('Error loading ticks.json:', err)
   }
 })

 const getStockName = (entry) => Object.keys(entry)[0]
 const isNoData = (entry) => entry[getStockName(entry)] === 'nodata'

 const formatChartData = (entry) => {
  const stockName = getStockName(entry)
  const startDate = dayjs(tdate.td)
  const prices = entry[stockName]

  const filteredDates = []
  const filteredPrices = []

  prices.forEach((price, i) => {
    const date = startDate.add(i, 'day')
    const dayOfWeek = date.day() // 0 = Sunday, 6 = Saturday

    if (dayOfWeek !== 0 && dayOfWeek !== 6) {
      filteredDates.push(date.format('YYYY-MM-DD'))
      filteredPrices.push(price)
    }
  })

   const ftrend = ref({})
   
   ticks.value.forEach(x => {const [k,v] = Object.entries(x)[0]; trendMap.value[k]=v.slice(0,10).every(x => v[0] <= x)})

   ftrend.value=trendMap
   console.log(trendMap.value)
   
   return {
     labels: filteredDates,
     datasets: [{
      data: filteredPrices,
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

const resetZoom = () => {
   const chart = chartRef.value?.chartInstance?.chart
   chart?.resetZoom?.()
 }

 const LineChart = defineComponent({
   props: ['chartData', 'showAxes'],
   setup(props, { expose }) {
     const chartInstance = ref(null)

     expose({
       chartInstance
     })

     return () =>
       h(Line, {
         ref: chartInstance,
         data: props.chartData,
         options: {
           responsive: true,
           elements: { point: { radius: 0 } },
           plugins: {
             legend: { display: false },
             tooltip: { enabled: false },
             zoom: props.showAxes
		 ? {
                   zoom: {
                     wheel: { enabled: true },
                     pinch: { enabled: true },
                     mode: 'x'
                   },
                   pan: {
                     enabled: true,
                     mode: 'x'
                   },
                   limits: {
                     x: { min: 0 }
                   }
                 }
		 : false
           },
           scales: {
             x: { display: props.showAxes ?? false },
             y: { display: props.showAxes ?? false }
           }
         }
       })
   }
 })

</script>

<template>
  <div class="p-4">
    <h1 class="font-radley text-browngrad-300 text-center text-st2">
      top contenders
    </h1>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div
        v-for="(entry, index) in ticks"
        :key="index"
	       class="p-4 border-6 border-brown-700 rounded shadow cursor-pointer hover:shadow-lg transition-shadow duration-200"
        @click="!isNoData(entry) && openChart(entry)"
      >
        <div class="text-browngrad-100 bg-antiquewhiteg-900 font-radley text-headlinecard-500 text-left text-st3">
          {{ getStockName(entry) }}
        </div>
        <div v-if="isNoData(entry)" class="text-gray-500">No data</div>
	<LineChart v-else :chart-data="formatChartData(entry)" :show-axes="false" />
      </div>
    </div>
    <h1 class="font-radley text-browngrad-300 text-center text-st3">
      range: {{ tdate.td }} - {{ sdate2 }}
    </h1>
    <!-- Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeModal">
      <div class="bg-white p-4 rounded shadow-lg w-[90%] max-w-3xl border-4 border-[#383838]">
  	<div class="flex justify-between items-center mb-2">
	  <h2 class="text-lg font-semibold text-browngrad-100">
            {{ selectedChart.name }}
	  </h2>
	  <button
	    class="text-sm text-blue-600 hover:underline"
	    @click="resetZoom">
	    Reset Zoom
	  </button>
          <button class="float-right text-gray-700" @click="closeModal">✕</button>
	</div>
        <div class="mt-4" style="height: 300px;">

	  <LineChart
	    ref="chartRef"
	    v-if="selectedChart.data"
	    :chart-data="selectedChart.data"
	    :show-axes="true"
	  />

        </div>
      </div>
    </div>
  </div>
  <p class="bg-antiquewhiteg-900 font-radley text-headlinecard-500 text-left text-st1"
     v-for="(k, j) in tops" :key="j">
    {{ k.split(':')[0].trim() }} - {{ trendMap[k.split(':')[0].trim()] ? "positive trend" : "uncertain trend" }}</p>
</template>

<style scoped>
 /* Optional: customize modal appearance */
</style>
