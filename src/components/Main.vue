<script setup>

</script>

<template>
  <header class="bg-antiquewhiteg-900 shadow-md w-full">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
	    <div class="max-w-sm rounded overflow-hidden shadow-lg">
	      <div class="px-2 py-2">
	      </div>
	    </div>
	    <div class="grid grid-cols-1 gap-1" style="height: 200px;">
	      <img class="w-full h-full object-cover st2-img-size" src="/images/stock2.jpeg" alt="Image" />
	    </div>
	    
	    <div class="md:hidden">
	      <button class="text-red-500 focus:outline-none focus:ring-2 focus:ring-blue-600">
		<!-- Icon (burger) -->
		<svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2"
		     viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
		  <path d="M4 6h16M4 12h16M4 18h16" />
		</svg>
	      </button>
	    </div>
	</div>
	
	<p class="text-howtw text-headlinecard-500 text-center font-crimson">how this works:</p>
	<br>
	<div class="font-mono text-base text-gray-800">
	  <ul class="list-disc pl-6">
	    <p class="font-mono text-3xl text-headingtext mb-6">All stock headlines are collected before the stock markets open</p>
	    <p class="font-sans-serif text-center text-3xl text-headingtext mb-6"> buy the corresponding stock and you may get rich</p>
	      <p class="font-mono text-3xl text-center text-red-500 mb-6">or</p>
	      <p class="font-fire text-center text-3xl text-headingtext mb-6">just don't care and die happy</p>
	      <br>
	  </ul>
	</div>
    </header>
</template>

<style scoped>

 .st2-img-size {
     max-width: 100%;
     max-height: 20%;
 }
 
</style>
