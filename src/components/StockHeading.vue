<script setup>

import {defineProps} from 'vue';

defineProps({
    st: Object
    });

const testf = (x,y) => {
     return "adding two numbers:" + (x+y)
}

const nolink = () => {
    alert('no link')
}

const shortext = (text,mlength) => {
    if(!text) return '';
    else;
    return text.length > mlength ? text.slice(0,mlength) + ' ...' : text;
}
     
</script>

<template>
    <section class="bg-cyangrad-900 px-2 py-2 max-w-xl mx-auto">
	<div class="container-xl lg:container m-auto">
	    <div class="max-w-custom-sm mx-auto bg-sky-100 shadow-lg rounded-xl overflow-hidden">
		<div class="grid grid-rows [auto_2rem_3rem] gap-2">
		  <div class="bg-deepskyblue-700"><h1 class="text-sh1 text-headlinecard-700">{{ st.stock }}</h1></div>
		  <div class="bg-deepskyblue-800 p-1"><h2 class="text-md font-semibold text-blackgrad-500">{{ shortext(st.headline,30) }}</h2></div>
		  <div class="bg-deepskyblue-700 py-0.5 px-0.5 mb-2"><a v-if="st.link !== 'missing'" :href="st.link" class="inline-block mt-4 px-4 py-2 bg-sky-100 text-mg3 text-black text-sm font-medium rounded hover:bg-sky-400 transition">Read more</a> <a v-else href="#" @click.prevent="nolink" class="inline-block mt-4 px-4 py-2 bg-sky-100 text-black text-sm font-medium rounded cursor-not-allowed">
      Read more
    </a></div>
		</div>
	    </div>
	</div>
    </section>
</template>


<style scoped>

</style>
