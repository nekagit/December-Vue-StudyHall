<template>
  <div>
    <div
      :class="[
        'px-2 py-1.5 rounded cursor-pointer text-sm font-sans flex items-center gap-2',
        isActive ? 'bg-msit-dark-700 text-msit-accent' : 'text-msit-dark-200 hover:bg-msit-dark-700',
        isFolder && 'select-none'
      ]"
      :style="{ paddingLeft: depth * 16 + 8 + 'px' }"
      @click="handleClick"
      @contextmenu.prevent="handleContextMenu"
      :draggable="true"
      @dragstart="handleDragStart"
      @dragover.prevent="handleDragOver"
      @drop.prevent="handleDrop"
    >
      <svg v-if="isFolder" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path v-if="isExpanded" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
      </svg>
      <svg v-else class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <span class="truncate flex-1">{{ item.name }}</span>
    </div>
    <div v-if="isFolder && isExpanded && item.children && item.children.length > 0">
      <FileTreeItem
        v-for="child in item.children"
        :key="child.id"
        :item="child"
        :current-file-id="currentFileId"
        :depth="depth + 1"
        @open-file="(id: string) => emit('open-file', id)"
        @toggle-folder="(item: FileItem) => emit('toggle-folder', item)"
        @show-context-menu="(e: MouseEvent, item: FileItem) => emit('show-context-menu', e, item)"
        @delete-item="(id: string) => emit('delete-item', id)"
        @drag-start="(e: DragEvent, item: FileItem) => emit('drag-start', e, item)"
        @drag-over="(e: DragEvent, item: FileItem) => emit('drag-over', e, item)"
        @drop="(e: DragEvent, item: FileItem) => emit('drop', e, item)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface FileItem {
  id: string
  name: string
  content: string
  language: string
  path: string
  type: 'file' | 'folder'
  parentId: string | null
  children?: FileItem[]
  expanded?: boolean
}

const props = defineProps<{
  item: FileItem
  currentFileId: string | null
  depth: number
}>()

const emit = defineEmits<{
  'open-file': [id: string]
  'toggle-folder': [item: FileItem]
  'show-context-menu': [event: MouseEvent, item: FileItem]
  'delete-item': [id: string]
  'drag-start': [event: DragEvent, item: FileItem]
  'drag-over': [event: DragEvent, item: FileItem]
  'drop': [event: DragEvent, item: FileItem]
}>()

const isFolder = computed(() => props.item.type === 'folder')
const isExpanded = computed(() => props.item.expanded ?? false)
const isActive = computed(() => props.currentFileId === props.item.id)

function handleClick() {
  if (isFolder.value) {
    emit('toggle-folder', props.item)
  } else {
    emit('open-file', props.item.id)
  }
}

function handleContextMenu(e: MouseEvent) {
  emit('show-context-menu', e, props.item)
}

function handleDragStart(e: DragEvent) {
  emit('drag-start', e, props.item)
}

function handleDragOver(e: DragEvent) {
  emit('drag-over', e, props.item)
}

function handleDrop(e: DragEvent) {
  emit('drop', e, props.item)
}
</script>
