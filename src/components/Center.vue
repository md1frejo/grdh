<script setup>
 
 import GetStocks from './GetStocks.vue'
 import Stats from './Stats.vue'
 import Graphs from './Graphs.vue'
 import Bottom from './Bottom.vue'
 
</script>

<template>
    <div class="grid grid-cols-2 gap-4">
	<div class="p-4 text-topblue-200">
	  <GetStocks :limit="16"/>	    
	</div>
	<div class="p-4">
	  <Stats />
	</div>
    </div>
    <div class="grid grid-cols-1 gap-4">
	<div class="bg-topblue-200 p-4">
	    <Bottom />
	</div>
    </div>
</template>


<style scoped>

</style>
