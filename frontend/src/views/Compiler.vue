<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden border border-msit-dark-700">
      <div class="px-4 sm:px-6 py-4 sm:py-6 border-b border-msit-dark-700">
        <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 font-serif">Python Compiler</h1>
        <p class="mt-2 text-sm text-msit-dark-200 font-sans">Write and execute Python code directly in your browser</p>
      </div>
      
      <div class="px-4 sm:px-6 py-4 sm:py-6">
        <PythonRunner />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import PythonRunner from '../components/PythonRunner.vue'
</script>


