<template>
  <div class="h-screen flex flex-col bg-msit-dark-900 overflow-hidden">
    <!-- Header -->
    <div class="flex items-center justify-between px-4 py-2 bg-msit-dark-800 border-b border-msit-dark-700">
      <div class="flex items-center gap-4">
        <h1 class="text-lg font-semibold text-msit-dark-50 font-serif">Code Editor</h1>
        <span class="text-xs text-msit-dark-300 font-sans">{{ files.length }} file{{ files.length !== 1 ? 's' : '' }}</span>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click="showNewFileDialog = true"
          class="px-3 py-1.5 bg-msit-dark-700 text-msit-dark-200 rounded hover:bg-msit-dark-600 transition-colors text-sm font-sans flex items-center gap-2"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          New File
        </button>
        <button
          @click="showNewFolderDialog = true"
          class="px-3 py-1.5 bg-msit-dark-700 text-msit-dark-200 rounded hover:bg-msit-dark-600 transition-colors text-sm font-sans flex items-center gap-2"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
          </svg>
          New Folder
        </button>
        <button
          @click="exportProject"
          class="px-3 py-1.5 bg-msit-accent text-msit-dark rounded hover:bg-msit-accent-500 transition-colors text-sm font-sans flex items-center gap-2"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Export ZIP
        </button>
        <button
          @click="showGithubDialog = true"
          class="px-3 py-1.5 bg-msit-dark-700 text-msit-dark-200 rounded hover:bg-msit-dark-600 transition-colors text-sm font-sans flex items-center gap-2"
        >
          <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          Upload to GitHub
        </button>
        <button
          @click="showPairProgramming = !showPairProgramming"
          :class="isInPairSession ? 'bg-msit-accent text-msit-dark' : ''"
          class="px-3 py-1.5 bg-msit-dark-700 text-msit-dark-200 rounded hover:bg-msit-dark-600 transition-colors text-sm font-sans flex items-center gap-2"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          Pair Program
        </button>
        <button
          @click="clearProject"
          class="px-3 py-1.5 bg-red-600 text-white rounded hover:bg-red-700 transition-colors text-sm font-sans flex items-center gap-2"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Clear
        </button>
      </div>
    </div>

    <!-- Pair Programming Panel -->
    <div v-if="showPairProgramming" class="bg-msit-dark-800 border-b border-msit-dark-700 px-4 py-2">
      <div v-if="!isInPairSession" class="flex items-center gap-2">
        <button
          @click="createPairSession"
          :disabled="isCreatingSession"
          class="px-3 py-1.5 bg-msit-accent text-msit-dark rounded hover:bg-msit-accent-500 disabled:opacity-50 transition-colors text-sm font-sans"
        >
          {{ isCreatingSession ? 'Creating...' : 'Start Session' }}
        </button>
        <input
          v-model="joinSessionId"
          @keyup.enter="joinPairSession"
          type="text"
          placeholder="Or enter session ID to join"
          class="flex-1 px-3 py-1.5 bg-msit-dark-700 border border-msit-dark-600 rounded text-sm text-msit-dark-50 font-sans focus:outline-none focus:ring-1 focus:ring-msit-accent"
        />
        <button
          @click="joinPairSession"
          :disabled="!joinSessionId || isJoiningSession"
          class="px-3 py-1.5 bg-msit-dark-700 text-msit-dark-200 rounded hover:bg-msit-dark-600 disabled:opacity-50 transition-colors text-sm font-sans"
        >
          {{ isJoiningSession ? 'Joining...' : 'Join' }}
        </button>
      </div>
      <div v-else class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <span class="text-xs text-msit-dark-300 font-sans">Session: <code class="text-msit-accent">{{ pairSessionId }}</code></span>
          <span class="text-xs text-msit-dark-300 font-sans">{{ participants.length }} participant(s)</span>
        </div>
        <button
          @click="leavePairSession"
          class="px-3 py-1.5 bg-red-600 text-white rounded hover:bg-red-700 transition-colors text-sm font-sans"
        >
          Leave Session
        </button>
      </div>
    </div>

    <div class="flex flex-1 overflow-hidden">
      <!-- File Tree Sidebar -->
      <div class="w-64 bg-msit-dark-800 border-r border-msit-dark-700 overflow-y-auto">
        <div class="p-2">
          <div class="text-xs font-semibold text-msit-dark-300 mb-2 px-2 font-sans">EXPLORER</div>
          <FileTreeItem
            v-for="item in files"
            :key="item.id"
            :item="item"
            :current-file-id="currentFileId"
            :depth="0"
            @open-file="openFile"
            @toggle-folder="toggleFolder"
            @show-context-menu="showContextMenu"
            @delete-item="deleteItem"
            @drag-start="handleDragStart"
            @drag-over="handleDragOver"
            @drop="handleDrop"
          />
        </div>
      </div>

      <!-- Main Editor Area -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Tabs -->
        <div class="flex items-center bg-msit-dark-800 border-b border-msit-dark-700 overflow-x-auto">
          <div
            v-for="tab in openTabs"
            :key="tab.id"
            @click="switchTab(tab.id)"
            :class="[
              'px-4 py-2 text-sm font-sans flex items-center gap-2 border-r border-msit-dark-700 cursor-pointer',
              currentFileId === tab.id ? 'bg-msit-dark-900 text-msit-accent' : 'bg-msit-dark-800 text-msit-dark-200 hover:bg-msit-dark-700'
            ]"
          >
            <span>{{ tab.name }}</span>
            <button
              @click.stop="closeTab(tab.id)"
              class="hover:text-red-400"
            >
              <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Monaco Editor -->
        <div ref="editorContainer" class="flex-1"></div>
      </div>
    </div>

    <!-- New File Dialog -->
    <div v-if="showNewFileDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-msit-dark-800 rounded-lg p-6 w-96 border border-msit-dark-700">
        <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-serif">New File</h2>
        <div class="mb-4">
          <label class="block text-sm text-msit-dark-200 mb-2 font-sans">Parent Folder (optional)</label>
          <select
            v-model="selectedParentId"
            class="w-full px-3 py-2 bg-msit-dark-900 border border-msit-dark-700 rounded text-msit-dark-50 mb-4 font-sans focus:outline-none focus:ring-2 focus:ring-msit-accent"
          >
            <option :value="null">Root</option>
            <option v-for="folder in getAllFolders()" :key="folder.id" :value="folder.id">
              {{ folder.path }}
            </option>
          </select>
        </div>
        <input
          v-model="newFileName"
          @keyup.enter="createFile"
          @keyup.esc="showNewFileDialog = false"
          type="text"
          placeholder="filename.py"
          class="w-full px-3 py-2 bg-msit-dark-900 border border-msit-dark-700 rounded text-msit-dark-50 mb-4 font-sans focus:outline-none focus:ring-2 focus:ring-msit-accent"
          autofocus
        />
        <div class="flex justify-end gap-2">
          <button
            @click="showNewFileDialog = false; selectedParentId = null"
            class="px-4 py-2 bg-msit-dark-700 text-msit-dark-200 rounded hover:bg-msit-dark-600 transition-colors font-sans"
          >
            Cancel
          </button>
          <button
            @click="createFile"
            class="px-4 py-2 bg-msit-accent text-msit-dark rounded hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Create
          </button>
        </div>
      </div>
    </div>

    <!-- New Folder Dialog -->
    <div v-if="showNewFolderDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-msit-dark-800 rounded-lg p-6 w-96 border border-msit-dark-700">
        <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-serif">New Folder</h2>
        <div class="mb-4">
          <label class="block text-sm text-msit-dark-200 mb-2 font-sans">Parent Folder (optional)</label>
          <select
            v-model="selectedParentId"
            class="w-full px-3 py-2 bg-msit-dark-900 border border-msit-dark-700 rounded text-msit-dark-50 mb-4 font-sans focus:outline-none focus:ring-2 focus:ring-msit-accent"
          >
            <option :value="null">Root</option>
            <option v-for="folder in getAllFolders()" :key="folder.id" :value="folder.id">
              {{ folder.path }}
            </option>
          </select>
        </div>
        <input
          v-model="newFolderName"
          @keyup.enter="createFolder"
          @keyup.esc="showNewFolderDialog = false"
          type="text"
          placeholder="folder-name"
          class="w-full px-3 py-2 bg-msit-dark-900 border border-msit-dark-700 rounded text-msit-dark-50 mb-4 font-sans focus:outline-none focus:ring-2 focus:ring-msit-accent"
          autofocus
        />
        <div class="flex justify-end gap-2">
          <button
            @click="showNewFolderDialog = false; selectedParentId = null"
            class="px-4 py-2 bg-msit-dark-700 text-msit-dark-200 rounded hover:bg-msit-dark-600 transition-colors font-sans"
          >
            Cancel
          </button>
          <button
            @click="createFolder"
            class="px-4 py-2 bg-msit-accent text-msit-dark rounded hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Create
          </button>
        </div>
      </div>
    </div>

    <!-- Context Menu -->
    <div
      v-if="showContextMenuDialog && contextMenuItem"
      class="fixed bg-msit-dark-800 border border-msit-dark-700 rounded-lg shadow-lg z-50 py-1 min-w-[150px]"
      :style="{ left: contextMenuPosition.x + 'px', top: contextMenuPosition.y + 'px' }"
      @click.stop
    >
      <button
        @click="showRenameDialog = true; renameName = contextMenuItem.name; showContextMenuDialog = false"
        class="w-full px-4 py-2 text-left text-sm text-msit-dark-200 hover:bg-msit-dark-700 font-sans"
      >
        Rename
      </button>
      <button
        @click="deleteItem(contextMenuItem.id); showContextMenuDialog = false; contextMenuItem = null"
        class="w-full px-4 py-2 text-left text-sm text-red-400 hover:bg-msit-dark-700 font-sans"
      >
        Delete
      </button>
      <button
        @click="showContextMenuDialog = false; contextMenuItem = null"
        class="w-full px-4 py-2 text-left text-sm text-msit-dark-300 hover:bg-msit-dark-700 font-sans"
      >
        Cancel
      </button>
    </div>

    <!-- Rename Dialog -->
    <div v-if="showRenameDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-msit-dark-800 rounded-lg p-6 w-96 border border-msit-dark-700">
        <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-serif">Rename</h2>
        <input
          v-model="renameName"
          @keyup.enter="renameItem"
          @keyup.esc="showRenameDialog = false; renameName = ''"
          type="text"
          class="w-full px-3 py-2 bg-msit-dark-900 border border-msit-dark-700 rounded text-msit-dark-50 mb-4 font-sans focus:outline-none focus:ring-2 focus:ring-msit-accent"
          autofocus
        />
        <div class="flex justify-end gap-2">
          <button
            @click="showRenameDialog = false; renameName = ''"
            class="px-4 py-2 bg-msit-dark-700 text-msit-dark-200 rounded hover:bg-msit-dark-600 transition-colors font-sans"
          >
            Cancel
          </button>
          <button
            @click="renameItem"
            class="px-4 py-2 bg-msit-accent text-msit-dark rounded hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Rename
          </button>
        </div>
      </div>
    </div>

    <!-- GitHub Upload Dialog -->
    <div v-if="showGithubDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-msit-dark-800 rounded-lg p-6 w-96 border border-msit-dark-700">
        <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-serif">Upload to GitHub</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm text-msit-dark-200 mb-1 font-sans">Repository (owner/repo)</label>
            <input
              v-model="githubRepo"
              type="text"
              placeholder="username/repo-name"
              class="w-full px-3 py-2 bg-msit-dark-900 border border-msit-dark-700 rounded text-msit-dark-50 font-sans focus:outline-none focus:ring-2 focus:ring-msit-accent"
            />
          </div>
          <div>
            <label class="block text-sm text-msit-dark-200 mb-1 font-sans">Branch</label>
            <input
              v-model="githubBranch"
              type="text"
              placeholder="main"
              class="w-full px-3 py-2 bg-msit-dark-900 border border-msit-dark-700 rounded text-msit-dark-50 font-sans focus:outline-none focus:ring-2 focus:ring-msit-accent"
            />
          </div>
          <div>
            <label class="block text-sm text-msit-dark-200 mb-1 font-sans">GitHub Token (stored locally)</label>
            <input
              v-model="githubToken"
              type="password"
              placeholder="ghp_xxxxxxxxxxxx"
              class="w-full px-3 py-2 bg-msit-dark-900 border border-msit-dark-700 rounded text-msit-dark-50 font-sans focus:outline-none focus:ring-2 focus:ring-msit-accent"
            />
            <p class="text-xs text-msit-dark-300 mt-1 font-sans">Token is stored in localStorage only</p>
          </div>
        </div>
        <div class="flex justify-end gap-2 mt-6">
          <button
            @click="showGithubDialog = false"
            class="px-4 py-2 bg-msit-dark-700 text-msit-dark-200 rounded hover:bg-msit-dark-600 transition-colors font-sans"
          >
            Cancel
          </button>
          <button
            @click="uploadToGithub"
            :disabled="!githubRepo || !githubToken"
            class="px-4 py-2 bg-msit-accent text-msit-dark rounded hover:bg-msit-accent-500 transition-colors font-sans disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Upload
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import loader from '@monaco-editor/loader'
import JSZip from 'jszip'
import type * as monaco from 'monaco-editor'
import FileTreeItem from '../components/FileTreeItem.vue'
import { pairProgrammingClient } from '../utils/pairProgramming'

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

const editorContainer = ref<HTMLElement | null>(null)
const files = ref<FileItem[]>([])
const openTabs = ref<FileItem[]>([])
const currentFileId = ref<string | null>(null)
const editorInstance = ref<monaco.editor.IStandaloneCodeEditor | null>(null)
let monacoInstance: typeof monaco | null = null

const showNewFileDialog = ref(false)
const showNewFolderDialog = ref(false)
const showGithubDialog = ref(false)
const showRenameDialog = ref(false)
const showContextMenuDialog = ref(false)
const contextMenuPosition = ref({ x: 0, y: 0 })
const contextMenuItem = ref<FileItem | null>(null)
const newFileName = ref('')
const newFolderName = ref('')
const renameName = ref('')
const selectedParentId = ref<string | null>(null)
const githubRepo = ref('')
const githubBranch = ref('main')
const githubToken = ref('')
const draggedItem = ref<FileItem | null>(null)

const STORAGE_KEY = 'editor_files'
const GITHUB_TOKEN_KEY = 'github_token'

// Pair programming state
const showPairProgramming = ref(false)
const isInPairSession = ref(false)
const pairSessionId = ref<string | null>(null)
const participants = ref<Array<{ username: string; user_id?: number }>>([])
const joinSessionId = ref('')
const isCreatingSession = ref(false)
const isJoiningSession = ref(false)
let isReceivingCodeUpdate = ref(false)
let codeChangeTimeout: ReturnType<typeof setTimeout> | null = null

// Build tree structure from flat array
function buildTree(items: FileItem[]): FileItem[] {
  const itemMap = new Map<string, FileItem>()
  const rootItems: FileItem[] = []

  // Create map of all items
  items.forEach(item => {
    itemMap.set(item.id, { ...item, children: [], expanded: item.expanded ?? false })
  })

  // Build tree structure
  items.forEach(item => {
    const node = itemMap.get(item.id)!
    if (item.parentId && itemMap.has(item.parentId)) {
      const parent = itemMap.get(item.parentId)!
      if (!parent.children) parent.children = []
      parent.children.push(node)
    } else {
      rootItems.push(node)
    }
  })

  // Sort: folders first, then files, both alphabetically
  const sortItems = (items: FileItem[]) => {
    items.sort((a, b) => {
      if (a.type !== b.type) {
        return a.type === 'folder' ? -1 : 1
      }
      return a.name.localeCompare(b.name)
    })
    items.forEach(item => {
      if (item.children) {
        sortItems(item.children)
      }
    })
  }
  sortItems(rootItems)
  return rootItems
}

// Flatten tree structure for storage
function flattenTree(items: FileItem[], parentId: string | null = null): FileItem[] {
  const result: FileItem[] = []
  items.forEach(item => {
    const flatItem: FileItem = {
      id: item.id,
      name: item.name,
      content: item.content || '',
      language: item.language || '',
      path: item.path,
      type: item.type,
      parentId: parentId,
      expanded: item.expanded
    }
    result.push(flatItem)
    if (item.children && item.children.length > 0) {
      result.push(...flattenTree(item.children, item.id))
    }
  })
  return result
}

// Get all files (not folders) from tree
function getAllFiles(items: FileItem[]): FileItem[] {
  const result: FileItem[] = []
  items.forEach(item => {
    if (item.type === 'file') {
      result.push(item)
    }
    if (item.children) {
      result.push(...getAllFiles(item.children))
    }
  })
  return result
}

// Get all folders from tree
function getAllFolders(): FileItem[] {
  const result: FileItem[] = []
  function traverse(items: FileItem[]) {
    items.forEach(item => {
      if (item.type === 'folder') {
        result.push(item)
        if (item.children) {
          traverse(item.children)
        }
      }
    })
  }
  traverse(files.value)
  return result
}

// Load files from localStorage
function loadFiles() {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored) {
    try {
      const flatFiles = JSON.parse(stored)
      // Migrate old files without type
      flatFiles.forEach((file: FileItem) => {
        if (!file.type) {
          file.type = 'file'
          file.parentId = null
        }
      })
      files.value = buildTree(flatFiles)
      const allFiles = getAllFiles(files.value)
      if (allFiles.length > 0 && allFiles[0] && openTabs.value.length === 0) {
        openTabs.value = [allFiles[0]]
        currentFileId.value = allFiles[0].id
      }
    } catch (e) {
      console.error('Failed to load files:', e)
    }
  } else {
    // Create a default file
    const defaultFile: FileItem = {
      id: generateId(),
      name: 'main.py',
      content: '# Welcome to Code Editor\nprint("Hello, World!")',
      language: 'python',
      path: 'main.py',
      type: 'file',
      parentId: null
    }
    files.value = [defaultFile]
    openTabs.value = [defaultFile]
    currentFileId.value = defaultFile.id
    saveFiles()
  }
}

// Save files to localStorage
function saveFiles() {
  const flatFiles = flattenTree(files.value)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(flatFiles))
}

// Generate unique ID
function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

// Detect language from filename
function detectLanguage(filename: string): string {
  const ext = filename.split('.').pop()?.toLowerCase() || ''
  const langMap: Record<string, string> = {
    'py': 'python',
    'js': 'javascript',
    'ts': 'typescript',
    'html': 'html',
    'css': 'css',
    'json': 'json',
    'md': 'markdown',
    'yaml': 'yaml',
    'yml': 'yaml',
    'sh': 'shell',
    'bash': 'shell',
    'sql': 'sql',
    'java': 'java',
    'cpp': 'cpp',
    'c': 'c',
    'go': 'go',
    'rs': 'rust',
    'php': 'php',
    'rb': 'ruby',
    'xml': 'xml',
    'vue': 'vue',
    'jsx': 'javascript',
    'tsx': 'typescript'
  }
  return langMap[ext] || 'plaintext'
}

// Initialize Monaco Editor
async function initEditor() {
  if (!editorContainer.value) return

  if (!monacoInstance) {
    monacoInstance = await loader.init()
  }
  
  if (monacoInstance) {
    // Define custom dark theme
    monacoInstance.editor.defineTheme('msit-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [],
      colors: {
        'editor.background': '#0F1D19',
        'editor.foreground': '#E0EADD',
        'editorLineNumber.foreground': '#6B8A63',
        'editor.selectionBackground': '#2A3F35',
        'editor.lineHighlightBackground': '#1A312B',
        'editorCursor.foreground': '#83E65B',
        'editorWhitespace.foreground': '#4A6946'
      }
    })
  
    editorInstance.value = monacoInstance.editor.create(editorContainer.value, {
    value: '',
    language: 'python',
    theme: 'msit-dark',
    automaticLayout: true,
    fontSize: 14,
    minimap: { enabled: true },
    scrollBeyondLastLine: false,
    wordWrap: 'on',
    fontFamily: 'Monaco, Menlo, "Courier New", monospace'
  })

  // Save content on change
  editorInstance.value.onDidChangeModelContent(() => {
    if (currentFileId.value && !isReceivingCodeUpdate.value) {
      const file = findItemInTree(files.value, currentFileId.value)
      if (file && file.type === 'file' && editorInstance.value) {
        file.content = editorInstance.value.getValue()
        saveFiles()
        
        // Sync with pair programming session
        if (isInPairSession.value && pairProgrammingClient.isConnected()) {
          if (codeChangeTimeout) {
            clearTimeout(codeChangeTimeout)
          }
          codeChangeTimeout = setTimeout(() => {
            pairProgrammingClient.sendCodeChange(file.content)
          }, 300)
        }
      }
    }
  })

  // Track cursor position for pair programming
  editorInstance.value.onDidChangeCursorPosition(() => {
    if (isInPairSession.value && editorInstance.value && !isReceivingCodeUpdate.value) {
      const position = editorInstance.value.getPosition()
      if (position) {
        pairProgrammingClient.sendCursorChange({
          line: position.lineNumber,
          column: position.column,
          lineNumber: position.lineNumber,
          character: position.column
        })
      }
    }
  })

  // Load initial file
  if (currentFileId.value) {
    loadFileContent(currentFileId.value)
  }
  }
}

// Load file content into editor
function loadFileContent(fileId: string) {
  const file = findItemInTree(files.value, fileId)
  if (file && file.type === 'file' && editorInstance.value && monacoInstance) {
    const model = monacoInstance.editor.createModel(file.content, file.language)
    editorInstance.value.setModel(model)
  }
}

// Open file
function openFile(fileId: string) {
  const file = findItemInTree(files.value, fileId)
  if (!file || file.type !== 'file') return

  if (!openTabs.value.find(t => t.id === fileId)) {
    openTabs.value.push(file)
  }
  currentFileId.value = fileId
  loadFileContent(fileId)
}

// Switch tab
function switchTab(fileId: string) {
  currentFileId.value = fileId
  loadFileContent(fileId)
}

// Close tab
function closeTab(fileId: string) {
  const index = openTabs.value.findIndex(t => t.id === fileId)
  if (index === -1) return

  openTabs.value.splice(index, 1)

  if (currentFileId.value === fileId) {
    if (openTabs.value.length > 0) {
      const nextTab = openTabs.value[Math.max(0, index - 1)]
      if (nextTab) {
        currentFileId.value = nextTab.id
        loadFileContent(currentFileId.value)
      }
    } else {
      currentFileId.value = null
      if (editorInstance.value && monacoInstance) {
        const model = monacoInstance.editor.createModel('', 'plaintext')
        editorInstance.value.setModel(model)
      }
    }
  }
}

// Find item in tree by ID
function findItemInTree(items: FileItem[], id: string): FileItem | null {
  for (const item of items) {
    if (item.id === id) return item
    if (item.children) {
      const found = findItemInTree(item.children, id)
      if (found) return found
    }
  }
  return null
}

// Get full path for an item
function getFullPath(item: FileItem, items: FileItem[]): string {
  if (!item.parentId) return item.name
  const parent = findItemInTree(items, item.parentId)
  if (!parent) return item.name
  return `${getFullPath(parent, items)}/${item.name}`
}

// Add item to tree
function addItemToTree(items: FileItem[], item: FileItem, parentId: string | null) {
  if (!parentId) {
    items.push(item)
    return
  }
  for (const node of items) {
    if (node.id === parentId) {
      if (!node.children) node.children = []
      node.children.push(item)
      return
    }
    if (node.children) {
      addItemToTree(node.children, item, parentId)
    }
  }
}

// Remove item from tree
function removeItemFromTree(items: FileItem[], id: string): boolean {
  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (item && item.id === id) {
      items.splice(i, 1)
      return true
    }
    if (item && item.children) {
      if (removeItemFromTree(item.children, id)) {
        return true
      }
    }
  }
  return false
}

// Create new file
function createFile() {
  if (!newFileName.value.trim()) return

  const parentId = selectedParentId.value
  const parent = parentId ? findItemInTree(files.value, parentId) : null
  const basePath = parent ? getFullPath(parent, files.value) : ''
  const fullPath = basePath ? `${basePath}/${newFileName.value}` : newFileName.value

  const file: FileItem = {
    id: generateId(),
    name: newFileName.value,
    content: '',
    language: detectLanguage(newFileName.value),
    path: fullPath,
    type: 'file',
    parentId: parentId
  }

  addItemToTree(files.value, file, parentId)
  openTabs.value.push(file)
  currentFileId.value = file.id
  saveFiles()
  loadFileContent(file.id)

  showNewFileDialog.value = false
  newFileName.value = ''
  selectedParentId.value = null
}

// Create new folder
function createFolder() {
  if (!newFolderName.value.trim()) return

  const parentId = selectedParentId.value
  const parent = parentId ? findItemInTree(files.value, parentId) : null
  const basePath = parent ? getFullPath(parent, files.value) : ''
  const fullPath = basePath ? `${basePath}/${newFolderName.value}` : newFolderName.value

  const folder: FileItem = {
    id: generateId(),
    name: newFolderName.value,
    content: '',
    language: '',
    path: fullPath,
    type: 'folder',
    parentId: parentId,
    children: [],
    expanded: true
  }

  addItemToTree(files.value, folder, parentId)
  saveFiles()

  showNewFolderDialog.value = false
  newFolderName.value = ''
  selectedParentId.value = null
}

// Toggle folder expansion
function toggleFolder(item: FileItem) {
  item.expanded = !item.expanded
  saveFiles()
}

// Rename item
function renameItem() {
  if (!contextMenuItem.value || !renameName.value.trim()) return

  const item = contextMenuItem.value
  item.name = renameName.value
  
  // Update path
  if (item.parentId) {
    const parent = findItemInTree(files.value, item.parentId)
    const basePath = parent ? getFullPath(parent, files.value) : ''
    item.path = basePath ? `${basePath}/${item.name}` : item.name
  } else {
    item.path = item.name
  }

  // Update children paths if it's a folder
  if (item.type === 'folder' && item.children) {
    updateChildrenPaths(item, files.value)
  }

  // Update open tabs
  const tabIndex = openTabs.value.findIndex(t => t.id === item.id)
  if (tabIndex !== -1) {
    openTabs.value[tabIndex] = { ...item }
  }

  saveFiles()
  showRenameDialog.value = false
  showContextMenuDialog.value = false
  contextMenuItem.value = null
  renameName.value = ''
}

// Update paths for all children
function updateChildrenPaths(folder: FileItem, allItems: FileItem[]) {
  if (!folder.children) return
  folder.children.forEach(child => {
    child.path = getFullPath(child, allItems)
    if (child.type === 'folder' && child.children) {
      updateChildrenPaths(child, allItems)
    }
  })
}

// Delete file or folder
function deleteItem(itemId: string) {
  const item = findItemInTree(files.value, itemId)
  if (!item) return

  const itemType = item.type === 'folder' ? 'folder' : 'file'
  const hasChildren = item.type === 'folder' && item.children && item.children.length > 0
  
  if (hasChildren) {
    if (!confirm(`Are you sure you want to delete the folder "${item.name}" and all its contents?`)) return
  } else {
    if (!confirm(`Are you sure you want to delete this ${itemType}?`)) return
  }

  // Close all tabs for files in this folder
  if (item.type === 'folder' && item.children) {
    const allFiles = getAllFiles([item])
    allFiles.forEach(file => closeTab(file.id))
  } else {
    closeTab(itemId)
  }

  removeItemFromTree(files.value, itemId)
  saveFiles()
}

// Show context menu
function showContextMenu(event: MouseEvent, item: FileItem) {
  event.preventDefault()
  event.stopPropagation()
  contextMenuItem.value = item
  contextMenuPosition.value = { x: event.clientX, y: event.clientY }
  showContextMenuDialog.value = true
}

// Handle drag start
function handleDragStart(event: DragEvent, item: FileItem) {
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
    draggedItem.value = item
  }
}

// Handle drag over
function handleDragOver(event: DragEvent, item: FileItem) {
  event.preventDefault()
  if (event.dataTransfer) {
    if (item.type === 'folder' && draggedItem.value && draggedItem.value.id !== item.id) {
      event.dataTransfer.dropEffect = 'move'
    } else {
      event.dataTransfer.dropEffect = 'none'
    }
  }
}

// Handle drop
function handleDrop(event: DragEvent, targetItem: FileItem) {
  event.preventDefault()
  event.stopPropagation()
  
  if (!draggedItem.value || draggedItem.value.id === targetItem.id) {
    draggedItem.value = null
    return
  }

  // Can only drop on folders
  if (targetItem.type !== 'folder') {
    draggedItem.value = null
    return
  }

  // Can't drop folder into itself or its children
  if (draggedItem.value.type === 'folder') {
    const isDescendant = (folder: FileItem, itemId: string): boolean => {
      if (folder.id === itemId) return true
      if (folder.children) {
        return folder.children.some(child => isDescendant(child, itemId))
      }
      return false
    }
    if (isDescendant(draggedItem.value, targetItem.id)) {
      alert('Cannot move folder into itself or its subfolder')
      draggedItem.value = null
      return
    }
  }

  // Remove from old location
  removeItemFromTree(files.value, draggedItem.value.id)
  
  // Add to new location
  draggedItem.value.parentId = targetItem.id
  if (!targetItem.children) targetItem.children = []
  targetItem.children.push(draggedItem.value)
  
  // Update paths
  if (draggedItem.value.type === 'folder' && draggedItem.value.children) {
    updateChildrenPaths(draggedItem.value, files.value)
  } else {
    draggedItem.value.path = getFullPath(draggedItem.value, files.value)
  }

  // Expand target folder
  targetItem.expanded = true

  saveFiles()
  draggedItem.value = null
}

// Export project as ZIP
async function exportProject() {
  try {
    const zip = new JSZip()
    const allFiles = getAllFiles(files.value)

    allFiles.forEach(file => {
      zip.file(file.path, file.content)
    })

    const blob = await zip.generateAsync({ type: 'blob' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `project-${new Date().toISOString().split('T')[0]}.zip`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Export failed:', error)
    alert('Failed to export project')
  }
}

// Upload to GitHub
async function uploadToGithub() {
  if (!githubRepo.value || !githubToken.value) {
    alert('Please provide repository and token')
    return
  }

  try {
    // Save token to localStorage
    localStorage.setItem(GITHUB_TOKEN_KEY, githubToken.value)

    const [owner, repo] = githubRepo.value.split('/')
    if (!owner || !repo) {
      alert('Invalid repository format. Use: owner/repo')
      return
    }

    const branch = githubBranch.value || 'main'

    // Create or update files via GitHub API
    const allFiles = getAllFiles(files.value)
    for (const file of allFiles) {
      const content = btoa(unescape(encodeURIComponent(file.content)))
      
      // Check if file exists
      const checkUrl = `https://api.github.com/repos/${owner}/${repo}/contents/${file.path}?ref=${branch}`
      const checkResponse = await fetch(checkUrl, {
        headers: {
          'Authorization': `token ${githubToken.value}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      })

      let sha: string | undefined
      if (checkResponse.ok) {
        const existingFile = await checkResponse.json()
        sha = existingFile.sha
      }

      // Create or update file
      const url = `https://api.github.com/repos/${owner}/${repo}/contents/${file.path}`
      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'Authorization': `token ${githubToken.value}`,
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: `Update ${file.path}`,
          content: content,
          branch: branch,
          ...(sha ? { sha } : {})
        })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || 'Failed to upload file')
      }
    }

    alert('Successfully uploaded to GitHub!')
    showGithubDialog.value = false
  } catch (error: any) {
    console.error('GitHub upload failed:', error)
    alert(`Failed to upload: ${error.message}`)
  }
}

// Clear project
function clearProject() {
  if (!confirm('Are you sure you want to clear all files? This cannot be undone.')) return
  files.value = []
  openTabs.value = []
  currentFileId.value = null
  localStorage.removeItem(STORAGE_KEY)
  
  // Create default file
  const defaultFile: FileItem = {
    id: generateId(),
    name: 'main.py',
    content: '# Welcome to Code Editor\nprint("Hello, World!")',
    language: 'python',
    path: 'main.py',
    type: 'file',
    parentId: null
  }
  files.value = [defaultFile]
  openTabs.value = [defaultFile]
  currentFileId.value = defaultFile.id
  saveFiles()
  loadFileContent(defaultFile.id)
}

// Pair Programming Functions
async function createPairSession() {
  try {
    isCreatingSession.value = true
    
    const username = localStorage.getItem('username') || `User${Math.floor(Math.random() * 1000)}`
    pairProgrammingClient.setUserInfo(username)
    
    pairProgrammingClient.connect()
    
    const sessionId = await pairProgrammingClient.createSession()
    pairSessionId.value = sessionId
    
    await pairProgrammingClient.joinSession(sessionId)
    
    pairProgrammingClient.setCallbacks({
      onCodeUpdate: (newCode: string) => {
        if (currentFileId.value && !isReceivingCodeUpdate.value) {
          isReceivingCodeUpdate.value = true
          const file = findItemInTree(files.value, currentFileId.value)
          if (file && file.type === 'file' && editorInstance.value) {
            file.content = newCode
            const model = monacoInstance!.editor.createModel(newCode, file.language)
            editorInstance.value.setModel(model)
            saveFiles()
          }
          setTimeout(() => {
            isReceivingCodeUpdate.value = false
          }, 100)
        }
      },
      onParticipantJoined: (_username: string, participantList: any[]) => {
        participants.value = participantList.map((p: any) => ({
          username: p.username,
          user_id: p.user_id
        }))
      },
      onParticipantLeft: (participantList: any[]) => {
        participants.value = participantList.map((p: any) => ({
          username: p.username,
          user_id: p.user_id
        }))
      },
      onError: (message: string) => {
        alert(`Pair programming error: ${message}`)
      }
    })
    
    isInPairSession.value = true
  } catch (error: any) {
    alert(`Failed to create session: ${error.message}`)
  } finally {
    isCreatingSession.value = false
  }
}

async function joinPairSession() {
  if (!joinSessionId.value.trim()) {
    alert('Please enter a session ID')
    return
  }
  
  try {
    isJoiningSession.value = true
    
    const username = localStorage.getItem('username') || `User${Math.floor(Math.random() * 1000)}`
    pairProgrammingClient.setUserInfo(username)
    
    pairProgrammingClient.connect()
    
    await pairProgrammingClient.joinSession(joinSessionId.value.trim())
    pairSessionId.value = joinSessionId.value.trim()
    
    pairProgrammingClient.setCallbacks({
      onCodeUpdate: (newCode: string) => {
        if (currentFileId.value && !isReceivingCodeUpdate.value) {
          isReceivingCodeUpdate.value = true
          const file = findItemInTree(files.value, currentFileId.value)
          if (file && file.type === 'file' && editorInstance.value) {
            file.content = newCode
            const model = monacoInstance!.editor.createModel(newCode, file.language)
            editorInstance.value.setModel(model)
            saveFiles()
          }
          setTimeout(() => {
            isReceivingCodeUpdate.value = false
          }, 100)
        }
      },
      onParticipantJoined: (_username: string, participantList: any[]) => {
        participants.value = participantList.map((p: any) => ({
          username: p.username,
          user_id: p.user_id
        }))
      },
      onParticipantLeft: (participantList: any[]) => {
        participants.value = participantList.map((p: any) => ({
          username: p.username,
          user_id: p.user_id
        }))
      },
      onError: (message: string) => {
        alert(`Pair programming error: ${message}`)
      }
    })
    
    isInPairSession.value = true
    joinSessionId.value = ''
  } catch (error: any) {
    alert(`Failed to join session: ${error.message}`)
  } finally {
    isJoiningSession.value = false
  }
}

function leavePairSession() {
  pairProgrammingClient.leaveSession()
  pairProgrammingClient.disconnect()
  isInPairSession.value = false
  pairSessionId.value = null
  participants.value = []
  if (codeChangeTimeout) {
    clearTimeout(codeChangeTimeout)
    codeChangeTimeout = null
  }
}

// Watch for file changes
watch(currentFileId, (newId) => {
  if (newId) {
    loadFileContent(newId)
  }
})

// Handle click outside context menu
function handleClickOutside(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('.context-menu')) {
    showContextMenuDialog.value = false
  }
}

onMounted(async () => {
  loadFiles()
  // Load GitHub token if exists
  const storedToken = localStorage.getItem(GITHUB_TOKEN_KEY)
  if (storedToken) {
    githubToken.value = storedToken
  }
  
  // Add click outside listener for context menu
  document.addEventListener('click', handleClickOutside)
  
  await nextTick()
  await initEditor()
})

onUnmounted(() => {
  if (editorInstance.value) {
    editorInstance.value.dispose()
  }
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Monaco Editor container */
:deep(.monaco-editor) {
  background-color: #0F1D19 !important;
}

:deep(.monaco-editor .margin) {
  background-color: #0F1D19 !important;
}
</style>







