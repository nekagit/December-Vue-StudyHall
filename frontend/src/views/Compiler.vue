<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h1 class="text-3xl font-bold text-gray-900">Python Compiler</h1>
        <p class="mt-2 text-sm text-gray-600">Write and execute Python code directly in your browser</p>
      </div>
      
      <div class="px-6 py-4">
        <PythonRunner />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import PythonRunner from '../components/PythonRunner.vue'
</script>


