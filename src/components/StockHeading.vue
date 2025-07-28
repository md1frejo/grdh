<script setup>
 import { defineProps, ref } from 'vue'

 defineProps({
   st: Object
 })

 const showNoLinkModal = ref(false)

 const testf = (x, y) => {
   return "adding two numbers:" + (x + y)
 }

 const nolink = () => {
   showNoLinkModal.value = true
 }

 const shortext = (text, mlength) => {
   if (!text) return ''
   return text.length > mlength ? text.slice(0, mlength) + ' ...' : text
 }

 const closeModal = () => {
   showNoLinkModal.value = false
 }
</script>

<template>
  <section class="bg-lightblueg-1000 px-2 py-2 max-w-xl mx-auto in-h-[800px]">
    <div class="container-xl lg:container m-auto">
      <div class="max-w-custom-sm mx-auto bg-sky-100 shadow-lg rounded-xl overflow-hidden">
        <div class="grid grid-rows-[auto_8rem_3rem] gap-2">
          <div class="bg-paleGreen-400">
            <h1 class="bg-deepskyblue-500 text-sh1 text-headlinecard-700">{{ st.stock }}</h1>
          </div>
          <div class="bg-deepskyblue-800 p-1">
            <h2 class="text-md font-semibold text-blackgrad-500 py-4">{{ shortext(st.headline, 30) }}</h2>
          </div>
          <div class="bg-deepskyblue-700 py-0.5 px-0.5 mb-2">
            <a v-if="st.link !== 'missing'" :href="st.link" class="inline-block px-4 py-2 bg-sky-100 text-mg3 text-black text-sm font-medium rounded hover:bg-sky-400 transition">Read more</a>
            <a v-else href="#" @click.prevent="nolink" class="inline-block px-4 py-2 bg-sky-100 text-black text-sm font-medium rounded cursor-not-allowed">Read more</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div
      v-if="showNoLinkModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white p-4 rounded-lg shadow-xl w-[90%] max-w-sm border border-gray-300">
        <div class="flex justify-between items-center mb-2">
          <h2 class="text-lg font-bold text-gray-700">No link available</h2>
          <button class="text-gray-500 hover:text-black text-xl" @click="closeModal">×</button>
        </div>
        <p class="text-gray-700">There is no link provided for this entry.</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
 /* Optional: custom styles for smoother appearance */
</style>
