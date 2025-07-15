<script setup>
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale,
 } from 'chart.js'
 
import { Bar } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const chartData = {
  labels: ['Swedbank', 'SCA', 'Nibe'],
  datasets: [{
    label: 'Counts',
    backgroundColor: '#4ade80',
    data: [1, 2, 3]
  }]
 }
 
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}
 
</script>

<template>
    <p>graphs</p>
    <Bar :data="chartData" :options="chartOptions" />
</template>


<style scoped>

</style>
