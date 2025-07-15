<script setup>

 import sda from '../../news.json';
 import { ref } from 'vue';

 const statd = ref([...sda]) 

 const sdate = statd.value.shift()?.reccorded || 'No date'
 
 const ctocks = (vals) => {
   const counts = {};
   vals.forEach(k => {
     const name = k.stock;
     counts[name] = (counts[name] || 0) + 1;
   });
   
   return counts;
 }

 const topstocks = (stocks) => {
   return stocks
     .filter(x => x[1] > 10)
     .map(([name, value]) => `${name}: ${value}`);
 };
 
 //const sdate = statd.shift()
 
 const sortd = (di) => {

   return Object.entries(di).sort((a,b) => b[1] - a[1])
 }
 
 const counts=ctocks(sda);
 const rank=sortd(ctocks(sda))
 const tops=topstocks(rank)
 //const topsd=Object.fromEntries(tops)

 // { Saab: 48, Volvo: 11, Ericsson: 5 }


 
</script>

<template>
  <!-- Add this somewhere hidden to make sure the class is included -->
  <ul>
    <br>
    <p class="text-center text-4xl text-browngrad-300 font-crimson">ranking of headlines</p>
    <br>
    <li v-for="k in rank" :key="k">
      <div class="bg-deepskyblue-900 flex justify-between items-center font-dosis text-left text-st1 text-headlinecard-500">
	<span class="mr-2"> {{ k[0] }} -> {{ k[1] }} </span>
	<span class="text-xl"> {{ k[1]>10 ? "contender" : "not enough" }} </span>
      </div>
    </li>
    <br>
    <h1 class="font-radley text-stat1 text-center text-browngrad-300">We have a total of {{ Object.entries(rank).length }} stocks and a total of {{ rank.reduce((sum, [, value]) => sum + value, 0) }} headlines as of {{ sdate }} </h1>
  </ul>
  <br>
  <p class="bg-greyg-900 font-radley text-headlinecard-700 text-left text-st2"> so the conclusion is: </p>
  <p class="bg-greyg-900 font-radley text-headlinecard-700 text-left text-st2"
     v-for="k in tops" :key="k">{{ k.split(':')[0].trim() }}</p>

</template>

<style scoped>

</style>
