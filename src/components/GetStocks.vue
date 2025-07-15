<script setup>
 
 import stockdata from '../../news.json';
 import StockHeading from './StockHeading.vue';
 import { defineProps,ref,computed } from 'vue';

 const props = defineProps({
   limit: Number,
 });
 
 const sdata=ref(stockdata);
 const rest=ref(sdata.value.slice(1))
 const lrest=ref(rest.value.length)
 const mindisp = ref(props.limit ?? 8)
 const count = 8;
 const scounter = ref(props.limit ?? count); 
 const disp = computed(() => rest.value.slice(0, scounter.value)); 
 const smax=rest.value.slice(1).length;
 
 function showMore(arg) {
   if (arg === 'm') {
     scounter.value+=scounter.value<smax?8:0;
   }
   else {
     scounter.value-=scounter.value>count?8:0;
   }
 }
 
</script>

<template>
  <p class="font-josefin text-hd1 text-center text-browngrad-300">
    number of headlines: {{ lrest }} </p>
  <p class="font-josefin text-hd1 text-center text-browngrad-300">
    reccorded: {{ sdata[0].reccorded }} </p>
  <br>
  <br>
  <div class="grid bg-deepskyblue-900 grid-cols-1 md:grid-cols-4 gap-6">
    <StockHeading v-for="st in disp" :key="st.id" :st="st" />
  </div>
  
  <div class="mt-4 flex justify-center space-x-4">
    <p class="text-black font-poppins px-4 py-2 bg-deepskyblue-600 rounded hover:bg-red-200">viewing: {{ disp.length }} </p>
    <button class="bg-deepskyblue-300 text-black px-4 py-2 rounded hover:bg-blue-600"
      @click="showMore('m')">
      Show More
    </button>
    <button class="bg-deepskyblue-100 text-black px-4 py-2 rounded hover:bg-blue-600"
      @click="showMore('l')">
      Show less
    </button>
  </div>
  
</template>
