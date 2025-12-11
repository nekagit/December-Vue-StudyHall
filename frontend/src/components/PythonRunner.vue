<template>
  <div class="space-y-4">
    <!-- Pair Programming Panel -->
    <div v-if="showPairProgramming" class="bg-msit-dark-700 border border-msit-dark-600 rounded-md p-4 mb-4">
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-sm font-semibold text-msit-dark-50 font-sans flex items-center">
          <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          Pair Programming
        </h3>
        <button
          @click="leavePairSession"
          v-if="isInPairSession"
          class="text-xs text-red-400 hover:text-red-300 font-sans"
        >
          Leave Session
        </button>
      </div>
      
      <div v-if="!isInPairSession" class="space-y-3">
        <div class="flex flex-col sm:flex-row gap-2">
          <button
            @click="createPairSession"
            :disabled="isCreatingSession"
            class="flex-1 inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 disabled:opacity-50 transition-colors font-sans"
          >
            <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            {{ isCreatingSession ? 'Creating...' : 'Start Session' }}
          </button>
          <button
            @click="showJoinDialog = true"
            class="flex-1 inline-flex items-center justify-center px-4 py-2 border border-msit-dark-600 text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-800 hover:bg-msit-dark-600 transition-colors font-sans"
          >
            <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
            Join Session
          </button>
        </div>
        
        <!-- Join Dialog -->
        <div v-if="showJoinDialog" class="bg-msit-dark-800 border border-msit-dark-600 rounded-md p-3">
          <div class="flex items-center gap-2">
            <input
              v-model="joinSessionId"
              type="text"
              placeholder="Enter session ID"
              class="flex-1 px-3 py-2 bg-msit-dark-700 border border-msit-dark-600 rounded-md text-msit-dark-50 text-sm font-sans focus:outline-none focus:ring-2 focus:ring-msit-accent"
              @keyup.enter="joinPairSession"
            />
            <button
              @click="joinPairSession"
              :disabled="!joinSessionId || isJoiningSession"
              class="px-4 py-2 bg-msit-accent text-msit-dark text-sm font-medium rounded-md hover:bg-msit-accent-500 disabled:opacity-50 transition-colors font-sans"
            >
              {{ isJoiningSession ? 'Joining...' : 'Join' }}
            </button>
            <button
              @click="showJoinDialog = false"
              class="px-3 py-2 text-msit-dark-300 hover:text-msit-dark-50 transition-colors font-sans"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
      
      <div v-else class="space-y-3">
        <!-- Session Info -->
        <div class="bg-msit-dark-800 border border-msit-dark-600 rounded-md p-3">
          <div class="text-xs text-msit-dark-300 mb-2 font-sans">Session ID:</div>
          <div class="flex items-center gap-2">
            <code class="flex-1 px-2 py-1 bg-msit-dark-700 rounded text-sm text-msit-accent font-mono break-all">{{ pairSessionId }}</code>
            <button
              @click="copySessionId"
              class="px-2 py-1 text-xs text-msit-dark-300 hover:text-msit-accent transition-colors font-sans"
            >
              Copy
            </button>
          </div>
        </div>
        
        <!-- Participants -->
        <div>
          <div class="text-xs text-msit-dark-300 mb-2 font-sans">Participants ({{ participants.length }}):</div>
          <div class="flex flex-wrap gap-2">
            <div
              v-for="(participant, index) in participants"
              :key="index"
              class="inline-flex items-center px-2 py-1 bg-msit-dark-800 border border-msit-dark-600 rounded text-xs text-msit-dark-50 font-sans"
            >
              <div class="w-2 h-2 bg-msit-accent rounded-full mr-2"></div>
              {{ participant.username }}
              <span v-if="typingUsers.has(participant.username)" class="ml-1 text-msit-accent animate-pulse">...</span>
            </div>
          </div>
        </div>

        <!-- Chat Panel -->
        <div class="bg-msit-dark-800 border border-msit-dark-600 rounded-md">
          <div class="flex items-center justify-between p-2 border-b border-msit-dark-700">
            <h4 class="text-xs font-semibold text-msit-dark-50 font-sans">Chat</h4>
            <button
              @click="showChat = !showChat"
              class="text-xs text-msit-dark-300 hover:text-msit-accent transition-colors font-sans"
            >
              {{ showChat ? 'Hide' : 'Show' }}
            </button>
          </div>
          <div v-if="showChat" class="p-3 space-y-3">
            <!-- Chat Messages -->
            <div ref="chatMessagesContainer" class="space-y-2 max-h-48 overflow-y-auto">
              <div
                v-for="msg in chatMessages"
                :key="msg.id"
                class="text-xs font-sans"
              >
                <div class="flex items-start gap-2">
                  <span class="font-semibold text-msit-accent">{{ msg.username }}:</span>
                  <span class="text-msit-dark-200 flex-1 wrap-break-word">{{ msg.message }}</span>
                  <span class="text-msit-dark-400 text-[10px] shrink-0">{{ formatTime(msg.timestamp) }}</span>
                </div>
              </div>
              <div v-if="chatMessages.length === 0" class="text-xs text-msit-dark-400 text-center py-4 font-sans">
                No messages yet. Start chatting!
              </div>
            </div>
            <!-- Chat Input -->
            <div class="flex gap-2">
              <input
                v-model="chatInput"
                @keyup.enter="sendChatMessage"
                @input="handleChatTyping"
                type="text"
                placeholder="Type a message..."
                class="flex-1 px-2 py-1.5 bg-msit-dark-700 border border-msit-dark-600 rounded text-xs text-msit-dark-50 font-sans focus:outline-none focus:ring-1 focus:ring-msit-accent"
              />
              <button
                @click="sendChatMessage"
                :disabled="!chatInput.trim()"
                class="px-3 py-1.5 bg-msit-accent text-msit-dark text-xs font-medium rounded hover:bg-msit-accent-500 disabled:opacity-50 transition-colors font-sans"
              >
                Send
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="pairProgrammingError" class="text-xs text-red-400 font-sans">
          {{ pairProgrammingError }}
        </div>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="flex flex-wrap items-center gap-2 pb-2 border-b border-msit-dark-700">
      <button
        @click="showPairProgramming = !showPairProgramming"
        :class="isInPairSession ? 'bg-msit-accent text-msit-dark' : ''"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <span class="hidden sm:inline">{{ isInPairSession ? 'Pairing' : 'Pair Program' }}</span>
      </button>
      <button
        @click="showSnippets = !showSnippets"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <span class="hidden sm:inline">Templates</span>
      </button>
      <button
        @click="showHistory = !showHistory"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="hidden sm:inline">History</span>
      </button>
      <button
        @click="showStudyHelp = !showStudyHelp"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        <span class="hidden sm:inline">Study Help</span>
      </button>
      <button
        @click="showVariables = !showVariables"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span class="hidden sm:inline">Variables</span>
      </button>
      <button
        @click="formatCode"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span class="hidden sm:inline">Format</span>
      </button>
      <button
        @click="clearCode"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        <span class="hidden sm:inline">Clear</span>
      </button>
      <button
        @click="exportCode"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        <span class="hidden sm:inline">Export</span>
      </button>
    </div>

    <!-- Code Snippets Panel -->
    <div v-if="showSnippets" class="bg-msit-dark-700 border border-msit-dark-600 rounded-md p-4">
      <h3 class="text-sm font-semibold text-msit-dark-50 mb-3 font-sans">Code Templates</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <button
          v-for="snippet in codeSnippets"
          :key="snippet.name"
          @click="loadSnippet(snippet.code)"
          class="text-left px-3 py-2 bg-msit-dark-800 border border-msit-dark-600 rounded hover:bg-msit-dark-600 hover:border-msit-accent transition-colors"
        >
          <div class="font-medium text-sm text-msit-dark-50 font-sans">{{ snippet.name }}</div>
          <div class="text-xs text-msit-dark-300 mt-1 font-sans">{{ snippet.description }}</div>
        </button>
      </div>
    </div>

    <!-- History Panel -->
    <div v-if="showHistory" class="bg-msit-dark-700 border border-msit-dark-600 rounded-md p-4">
      <h3 class="text-sm font-semibold text-msit-dark-50 mb-3 font-sans">Code History</h3>
      <div v-if="codeHistory.length === 0" class="text-sm text-msit-dark-300 font-sans">No history yet</div>
      <div v-else class="space-y-2 max-h-48 overflow-y-auto">
        <div
          v-for="(item, index) in codeHistory"
          :key="index"
          class="bg-msit-dark-800 border border-msit-dark-600 rounded p-2 hover:bg-msit-dark-600 cursor-pointer transition-colors"
          @click="loadSnippet(item.code)"
        >
          <div class="text-xs text-msit-dark-300 mb-1 font-sans">{{ item.timestamp }}</div>
          <div class="text-sm font-mono text-msit-dark-100 line-clamp-2 wrap-break-word">{{ item.code.substring(0, 100) }}{{ item.code.length > 100 ? '...' : '' }}</div>
        </div>
      </div>
    </div>

    <!-- Study Help Panel -->
    <div v-if="showStudyHelp" class="bg-msit-dark-700 border border-msit-dark-600 rounded-md p-4">
      <h3 class="text-sm font-semibold text-msit-dark-50 mb-3 font-sans flex items-center">
        <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Study Tips & Help
      </h3>
      <div class="space-y-3">
        <div v-for="tip in studyTips" :key="tip.title" class="bg-msit-dark-800 border border-msit-dark-600 rounded p-3">
          <div class="font-medium text-sm text-msit-dark-50 mb-1 font-sans">{{ tip.title }}</div>
          <div class="text-xs text-msit-dark-300 font-sans">{{ tip.description }}</div>
        </div>
        <div v-if="currentError" class="bg-red-900/20 border border-red-700 rounded p-3">
          <div class="font-medium text-sm text-red-300 mb-1 font-sans">Error Explanation</div>
          <div class="text-xs text-red-200 font-sans whitespace-pre-wrap">{{ currentError }}</div>
          <div v-if="errorLineNumber !== null" class="text-xs text-yellow-300 mt-2 font-sans">
            📍 Error at line {{ errorLineNumber }}
          </div>
        </div>
      </div>
    </div>

    <!-- Variables Inspector Panel -->
    <div v-if="showVariables && variables.length > 0" class="bg-msit-dark-700 border border-msit-dark-600 rounded-md p-4">
      <h3 class="text-sm font-semibold text-msit-dark-50 mb-3 font-sans">Variable Inspector</h3>
      <div class="space-y-2 max-h-48 overflow-y-auto">
        <div v-for="(variable, index) in variables" :key="index" class="bg-msit-dark-800 border border-msit-dark-600 rounded p-2">
          <div class="font-mono text-sm text-msit-dark-50">
            <span class="text-msit-accent">{{ variable.name }}</span>
            <span class="text-msit-dark-300 mx-2">=</span>
            <span class="text-msit-dark-100">{{ variable.value }}</span>
            <span class="text-msit-dark-400 ml-2 text-xs">({{ variable.type }})</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Code Editor with Syntax Highlighting -->
    <div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-2">
        <label for="code" class="block text-sm font-medium text-msit-dark-50 font-sans">Python Code</label>
        <div class="flex items-center gap-3">
          <span class="text-xs text-msit-dark-300 font-sans">{{ code.length }} characters, {{ code.split('\n').length }} lines</span>
          <span v-if="executionTime > 0" class="text-xs text-msit-accent font-sans">{{ executionTime }}ms</span>
          <span v-if="syntaxErrors.length > 0" class="text-xs text-red-400 font-sans">{{ syntaxErrors.length }} error(s)</span>
        </div>
      </div>
      <div class="relative border border-msit-dark-600 rounded-md overflow-hidden">
        <div ref="editorContainer" class="code-editor-container"></div>
        <!-- Copy/Paste Warning Overlay -->
        <div v-if="showCopyWarning" class="absolute inset-0 bg-red-900/80 flex items-center justify-center rounded-md z-20">
          <div class="bg-msit-dark-800 border-2 border-red-500 rounded-lg p-4 max-w-sm text-center">
            <div class="text-red-300 font-semibold mb-2 font-sans">Copy/Paste Disabled</div>
            <div class="text-sm text-msit-dark-200 font-sans">Type your code manually to improve your learning!</div>
          </div>
        </div>
      </div>
      <!-- Error List -->
      <div v-if="syntaxErrors.length > 0" class="mt-2 bg-red-900/20 border border-red-700 rounded-md p-3">
        <div class="font-medium text-sm text-red-300 mb-2 font-sans">Syntax Errors:</div>
        <div class="space-y-1">
          <div v-for="(error, index) in syntaxErrors" :key="index" class="text-xs text-red-200 font-sans">
            <span class="font-semibold">Line {{ error.line }}:</span> {{ error.message }}
            <span v-if="error.suggestion" class="block mt-1 text-yellow-300">💡 Suggestion: {{ error.suggestion }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Action Buttons -->
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
      <button
        @click="runPython"
        :disabled="isLoading"
        class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-msit-dark bg-msit-accent hover:bg-msit-accent-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-msit-accent disabled:opacity-50 transition-colors font-sans"
      >
        <svg v-if="!isLoading" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ isLoading ? 'Loading Pyodide...' : 'Run Code' }}
      </button>
      <button
        v-if="output"
        @click="clearOutput"
        class="w-full sm:w-auto inline-flex items-center justify-center px-3 py-2 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        Clear Output
      </button>
    </div>
    
    <!-- Output -->
    <div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-2">
        <label class="block text-sm font-medium text-msit-dark-50 font-sans">Output</label>
        <div class="flex items-center gap-2">
          <span v-if="lastRunSuccess !== null" class="text-xs font-sans" :class="lastRunSuccess ? 'text-green-400' : 'text-red-400'">
            {{ lastRunSuccess ? '✓ Success' : '✗ Error' }}
          </span>
          <button
            v-if="output"
            @click="copyOutput"
            class="text-xs text-msit-dark-300 hover:text-msit-accent transition-colors font-sans self-start sm:self-auto"
          >
            Copy Output
          </button>
        </div>
      </div>
      <div class="bg-msit-dark-900 text-msit-accent p-3 sm:p-4 rounded-md font-mono text-xs sm:text-sm overflow-auto max-h-64 sm:max-h-96 border border-msit-dark-700">
        <pre class="whitespace-pre-wrap wrap-break-word">{{ output || 'Ready to run code...' }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { EditorView, basicSetup } from 'codemirror'
import { python } from '@codemirror/lang-python'
import { lintGutter, setDiagnostics } from '@codemirror/lint'
import { EditorState } from '@codemirror/state'
import { keymap } from '@codemirror/view'
import { pairProgrammingClient, type ChatMessage } from '../utils/pairProgramming'

const code = ref('print("Hello, StudyHall!")')
const output = ref('Ready!')
const isLoading = ref(true)
const showSnippets = ref(false)
const showHistory = ref(false)
const showStudyHelp = ref(false)
const showVariables = ref(false)
const showCopyWarning = ref(false)
const showPairProgramming = ref(false)
const codeHistory = ref<Array<{ code: string; timestamp: string }>>([])
const executionTime = ref(0)
const lastRunSuccess = ref<boolean | null>(null)
const currentError = ref('')
const errorLineNumber = ref<number | null>(null)
const syntaxErrors = ref<Array<{ line: number; message: string; suggestion?: string }>>([])
const variables = ref<Array<{ name: string; value: string; type: string }>>([])
const editorContainer = ref<HTMLElement | null>(null)

// Pair programming state
const isInPairSession = ref(false)
const pairSessionId = ref<string | null>(null)
const participants = ref<Array<{ username: string; user_id?: number }>>([])
const showJoinDialog = ref(false)
const joinSessionId = ref('')
const isCreatingSession = ref(false)
const isJoiningSession = ref(false)
const pairProgrammingError = ref('')
let codeChangeTimeout: ReturnType<typeof setTimeout> | null = null
let isReceivingCodeUpdate = ref(false)

// Chat and typing state
const showChat = ref(true)
const chatMessages = ref<Array<{ id: string; username: string; message: string; timestamp: Date }>>([])
const chatInput = ref('')
const typingUsers = ref<Set<string>>(new Set())
const chatMessagesContainer = ref<HTMLElement | null>(null)
let typingTimeout: ReturnType<typeof setTimeout> | null = null
let cursorPositions = ref<Map<string, { line: number; column: number; username: string }>>(new Map())

let editorView: EditorView | null = null
let pyodide: any = null
let historyTimeout: ReturnType<typeof setTimeout> | null = null
let syntaxCheckTimeout: ReturnType<typeof setTimeout> | null = null

const codeSnippets = [
  {
    name: 'Hello World',
    description: 'Basic print statement',
    code: 'print("Hello, World!")'
  },
  {
    name: 'Variables',
    description: 'Variable assignment and types',
    code: `name = "StudyHall"
age = 25
height = 5.9
is_student = True

print(f"Name: {name}, Age: {age}, Height: {height}, Student: {is_student}")`
  },
  {
    name: 'Lists',
    description: 'Working with lists',
    code: `numbers = [1, 2, 3, 4, 5]
print(f"First: {numbers[0]}")
print(f"Last: {numbers[-1]}")
print(f"Sum: {sum(numbers)}")
print(f"Length: {len(numbers)}")`
  },
  {
    name: 'Loops',
    description: 'For and while loops',
    code: `# For loop
for i in range(5):
    print(f"Number: {i}")

# While loop
count = 0
while count < 3:
    print(f"Count: {count}")
    count += 1`
  },
  {
    name: 'Functions',
    description: 'Define and call functions',
    code: `def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

print(greet("StudyHall"))
print(f"5 + 3 = {add(5, 3)}")`
  },
  {
    name: 'Dictionaries',
    description: 'Working with dictionaries',
    code: `student = {
    "name": "Alice",
    "age": 20,
    "courses": ["Python", "Web Dev"]
}

print(f"Name: {student['name']}")
print(f"Age: {student.get('age')}")
print(f"Courses: {', '.join(student['courses'])}")`
  },
  {
    name: 'List Comprehension',
    description: 'Pythonic list operations',
    code: `# Square numbers
squares = [x**2 for x in range(10)]
print(f"Squares: {squares}")

# Filter even numbers
evens = [x for x in range(20) if x % 2 == 0]
print(f"Evens: {evens}")`
  },
  {
    name: 'File Operations',
    description: 'Read and write files',
    code: `# Write to file
with open("example.txt", "w") as f:
    f.write("Hello from StudyHall!")

# Read from file
with open("example.txt", "r") as f:
    content = f.read()
    print(content)`
  }
]

const loadPyodide = async () => {
  output.value = 'Loading Pyodide environment...'
  try {
    // @ts-ignore
    pyodide = await window.loadPyodide()
    isLoading.value = false
    output.value = 'Ready!'
    // Check syntax after Pyodide loads
    checkSyntax()
  } catch (e: any) {
    output.value = `Error loading Pyodide: ${e}`
  }
}

const runPython = async () => {
  if (!pyodide) return
  const startTime = performance.now()
  try {
    output.value = '' // Clear previous output
    currentError.value = ''
    variables.value = []
    lastRunSuccess.value = null

    pyodide.setStdout({ batched: (msg: string) => {
      output.value += msg + '\n'
    }})
    pyodide.setStderr({ batched: (msg: string) => {
      output.value += `ERROR: ${msg}\n`
      analyzeError(msg)
    }})

    await pyodide.runPythonAsync(code.value)

    // Extract variables
    try {
      const globals = pyodide.globals.toJs({ dict_converter: Object.fromEntries })
      const variableList: Array<{ name: string; value: string; type: string }> = []

      for (const [key, value] of Object.entries(globals)) {
        if (!key.startsWith('_') && typeof value !== 'function' && key !== 'pyodide') {
          const typeName = typeof value === 'object' && value !== null
            ? Array.isArray(value) ? 'list' : value.constructor?.name || 'object'
            : typeof value
          variableList.push({
            name: key,
            value: String(value),
            type: typeName
          })
        }
      }
      variables.value = variableList
    } catch (e) {
      // Ignore variable extraction errors
    }

    const endTime = performance.now()
    executionTime.value = Math.round(endTime - startTime)
    lastRunSuccess.value = true
    saveToHistory()
  } catch (err: any) {
    const endTime = performance.now()
    executionTime.value = Math.round(endTime - startTime)
    output.value = `Error: ${err}`
    analyzeError(String(err))
    lastRunSuccess.value = false
  }
}

const loadSnippet = (snippetCode: string) => {
  code.value = snippetCode
  showSnippets.value = false
  if (editorView) {
    editorView.dispatch({
      changes: {
        from: 0,
        to: editorView.state.doc.length,
        insert: snippetCode
      }
    })
  }
  if (pyodide) {
    checkSyntax()
  }
}

const clearCode = () => {
  if (confirm('Clear all code?')) {
    code.value = ''
    syntaxErrors.value = []
    if (editorView) {
      editorView.dispatch({
        changes: {
          from: 0,
          to: editorView.state.doc.length,
          insert: ''
        }
      })
    }
    updateEditorDiagnostics()
  }
}

const clearOutput = () => {
  output.value = ''
}

const formatCode = () => {
  // Simple formatting - indent properly
  const lines = code.value.split('\n')
  let indent = 0
  const formatted: string[] = []
  
  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) {
      formatted.push('')
      continue
    }
    
    // Decrease indent for dedent keywords
    if (trimmed.startsWith('except') || trimmed.startsWith('elif') || 
        trimmed.startsWith('else') || trimmed.startsWith('finally')) {
      indent = Math.max(0, indent - 1)
    }
    
    formatted.push('  '.repeat(indent) + trimmed)
    
    // Increase indent for block starters
    if (trimmed.endsWith(':') && !trimmed.startsWith('#')) {
      indent += 1
    }
  }
  
  code.value = formatted.join('\n')
}

const exportCode = () => {
  const blob = new Blob([code.value], { type: 'text/x-python' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `code-${new Date().toISOString().split('T')[0]}.py`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const copyOutput = () => {
  navigator.clipboard.writeText(output.value)
}

const saveToHistory = () => {
  if (historyTimeout) {
    clearTimeout(historyTimeout)
  }
  
  historyTimeout = setTimeout(() => {
    if (code.value.trim() && code.value.length > 10) {
      const historyItem = {
        code: code.value,
        timestamp: new Date().toLocaleString()
      }
      
      // Load existing history
      const existing = localStorage.getItem('python_code_history')
      let history: Array<{ code: string; timestamp: string }> = []
      
      if (existing) {
        try {
          history = JSON.parse(existing)
        } catch (e) {
          history = []
        }
      }
      
      // Add new item (avoid duplicates)
      if (history.length === 0 || history[history.length - 1]?.code !== code.value) {
        history.push(historyItem)
        // Keep only last 20 items
        if (history.length > 20) {
          history = history.slice(-20)
        }
        localStorage.setItem('python_code_history', JSON.stringify(history))
        codeHistory.value = history.reverse()
      }
    }
  }, 2000) // Save after 2 seconds of inactivity
}

const loadHistory = () => {
  const existing = localStorage.getItem('python_code_history')
  if (existing) {
    try {
      codeHistory.value = JSON.parse(existing).reverse()
    } catch (e) {
      codeHistory.value = []
    }
  }
}

const showCopyWarningMessage = () => {
  showCopyWarning.value = true
  setTimeout(() => {
    showCopyWarning.value = false
  }, 2000)
}

const handleKeyDown = (e: KeyboardEvent) => {
  // Global shortcuts (only when not in code editor)
  const target = e.target as HTMLElement
  if (target.closest('.cm-editor')) {
    return // Let CodeMirror handle it
  }
  
  // Ctrl/Cmd + Enter to run code (global)
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault()
    runPython()
  }
  // Ctrl/Cmd + S to save/export (global)
  if ((e.ctrlKey || e.metaKey) && e.key === 's') {
    e.preventDefault()
    exportCode()
  }
}

// Enhanced error analysis with line number extraction and specific suggestions
const analyzeError = (errorMsg: string) => {
  const errorLower = errorMsg.toLowerCase()
  errorLineNumber.value = null
  syntaxErrors.value = []
  
  // Extract line number from error message (common Python error format)
  const lineMatch = errorMsg.match(/line (\d+)/i) || errorMsg.match(/\(line (\d+)\)/i)
  if (lineMatch && lineMatch[1]) {
    errorLineNumber.value = parseInt(lineMatch[1])
  }
  
  // Parse error type and provide detailed suggestions
  if (errorLower.includes('syntaxerror') || errorLower.includes('invalid syntax')) {
    const suggestions = extractSyntaxErrorSuggestions(errorMsg)
    currentError.value = `Syntax Error: ${suggestions.message}\n\nCommon causes:\n${suggestions.causes.join('\n')}`
    
    if (errorLineNumber.value) {
      syntaxErrors.value.push({
        line: errorLineNumber.value,
        message: suggestions.message,
        suggestion: suggestions.fix
      })
    }
  } else if (errorLower.includes('nameerror') || errorLower.includes('is not defined')) {
    const varMatch = errorMsg.match(/name ['"]([^'"]+)['"]/i)
    const varName = varMatch ? varMatch[1] : 'variable'
    
    currentError.value = `Name Error: The name '${varName}' is not defined.\n\nPossible solutions:\n• Check if you spelled the variable name correctly\n• Make sure you assigned a value to '${varName}' before using it\n• Check if you're using the right variable name (Python is case-sensitive)\n• If it's a function, make sure you defined it before calling it`
    
    if (errorLineNumber.value) {
      syntaxErrors.value.push({
        line: errorLineNumber.value,
        message: `'${varName}' is not defined`,
        suggestion: `Check spelling and ensure '${varName}' is assigned before this line`
      })
    }
  } else if (errorLower.includes('typeerror')) {
    let suggestion = 'Check if you\'re mixing incompatible types (e.g., string + number)'
    
    if (errorLower.includes('unsupported operand')) {
      suggestion = 'You\'re trying to use an operator (+, -, *, /) on incompatible types. Convert types using str(), int(), or float()'
    } else if (errorLower.includes('not callable')) {
      suggestion = 'You\'re trying to call something that isn\'t a function. Check if you forgot parentheses or used wrong variable name'
    } else if (errorLower.includes('object is not subscriptable')) {
      suggestion = 'You\'re trying to use [] on something that doesn\'t support it. Check if the variable is a list, dict, or string'
    }
    
    currentError.value = `Type Error: ${errorMsg}\n\n${suggestion}`
    
    if (errorLineNumber.value) {
      syntaxErrors.value.push({
        line: errorLineNumber.value,
        message: 'Type mismatch',
        suggestion: suggestion
      })
    }
  } else if (errorLower.includes('indentationerror') || errorLower.includes('unexpected indent')) {
    currentError.value = `Indentation Error at line ${errorLineNumber.value || 'unknown'}\n\nPython uses indentation to define code blocks.\n• Use consistent indentation (4 spaces recommended)\n• Don't mix tabs and spaces\n• Check that your if/for/while/def statements have proper indentation\n• Make sure all code in a block has the same indentation level`
    
    if (errorLineNumber.value) {
      syntaxErrors.value.push({
        line: errorLineNumber.value,
        message: 'Indentation error',
        suggestion: 'Ensure consistent indentation (4 spaces). Check if this line should be indented or unindented'
      })
    }
  } else if (errorLower.includes('indexerror') || errorLower.includes('list index out of range')) {
    currentError.value = `Index Error: You're trying to access an index that doesn't exist.\n\nRemember:\n• Lists start at index 0\n• The last valid index is length - 1\n• Use len(list) to check the length before accessing\n• Use negative indices carefully (e.g., -1 is the last item)`
    
    if (errorLineNumber.value) {
      syntaxErrors.value.push({
        line: errorLineNumber.value,
        message: 'Index out of range',
        suggestion: 'Check the list length before accessing. Use len() to verify the list has enough elements'
      })
    }
  } else if (errorLower.includes('keyerror')) {
    const keyMatch = errorMsg.match(/['"]([^'"]+)['"]/i)
    const keyName = keyMatch ? keyMatch[1] : 'key'
    
    currentError.value = `Key Error: The dictionary key '${keyName}' doesn't exist.\n\nSolutions:\n• Use .get('${keyName}') instead of ['${keyName}'] to avoid errors\n• Check if the key exists: if '${keyName}' in dict:\n• Verify you're using the correct key name (case-sensitive)`
    
    if (errorLineNumber.value) {
      syntaxErrors.value.push({
        line: errorLineNumber.value,
        message: `Key '${keyName}' not found`,
        suggestion: `Use dict.get('${keyName}') or check if '${keyName}' in dict first`
      })
    }
  } else if (errorLower.includes('attributeerror')) {
    const attrMatch = errorMsg.match(/['"]([^'"]+)['"]/i)
    const attrName = attrMatch ? attrMatch[1] : 'attribute'
    
    currentError.value = `Attribute Error: The object doesn't have the attribute '${attrName}'.\n\nCheck:\n• The object type (use type() or isinstance())\n• Available methods for that type\n• If you meant a different method name\n• If you're calling a method on None (check for None values)`
    
    if (errorLineNumber.value) {
      syntaxErrors.value.push({
        line: errorLineNumber.value,
        message: `'${attrName}' attribute not found`,
        suggestion: `Check the object type and available methods. Verify the object is not None`
      })
    }
  } else if (errorLower.includes('valueerror')) {
    currentError.value = `Value Error: The function received an inappropriate value.\n\nCommon causes:\n• int() or float() received a non-numeric string\n• Invalid value for a function parameter\n• Empty sequence where value expected\n\nCheck the function arguments and their expected ranges/types`
    
    if (errorLineNumber.value) {
      syntaxErrors.value.push({
        line: errorLineNumber.value,
        message: 'Invalid value',
        suggestion: 'Check function arguments match expected types and ranges'
      })
    }
  } else {
    currentError.value = `Error: ${errorMsg}\n\nRead the error message carefully and check your code logic.\nCommon issues:\n• Typos in variable or function names\n• Wrong variable names\n• Incorrect function calls\n• Missing imports\n• Logic errors`
    
    if (errorLineNumber.value) {
      syntaxErrors.value.push({
        line: errorLineNumber.value,
        message: errorMsg.substring(0, 100),
        suggestion: 'Review the error message and check the code logic at this line'
      })
    }
  }
  
  // Update editor diagnostics
  updateEditorDiagnostics()
}

// Extract specific syntax error suggestions
const extractSyntaxErrorSuggestions = (errorMsg: string): { message: string; causes: string[]; fix?: string } => {
  const errorLower = errorMsg.toLowerCase()
  
  if (errorLower.includes('eol') || errorLower.includes('end of line')) {
    return {
      message: 'Unclosed string or missing quote',
      causes: [
        '• Missing closing quote (", \', """, or \'\'\')',
        '• String spans multiple lines without triple quotes',
        '• Mismatched quote types'
      ],
      fix: 'Add the missing closing quote or use triple quotes for multi-line strings'
    }
  }
  
  if (errorLower.includes('unexpected eof') || errorLower.includes('end of file')) {
    return {
      message: 'Unexpected end of file',
      causes: [
        '• Missing closing parenthesis, bracket, or brace',
        '• Incomplete function or class definition',
        '• Missing colon (:) after if/for/while/def/class'
      ],
      fix: 'Check for unmatched parentheses (), brackets [], or braces {}. Add missing colons after control structures'
    }
  }
  
  if (errorLower.includes('invalid character') || errorLower.includes('unexpected character')) {
    return {
      message: 'Invalid character in code',
      causes: [
        '• Special characters that aren\'t allowed',
        '• Copy-pasted characters from other sources',
        '• Wrong quote characters'
      ],
      fix: 'Remove or replace the invalid character. Use standard ASCII characters'
    }
  }
  
  if (errorLower.includes('can\'t assign') || errorLower.includes('cannot assign')) {
    return {
      message: 'Invalid assignment',
      causes: [
        '• Trying to assign to a literal or expression',
        '• Using = instead of == in condition',
        '• Invalid left-hand side of assignment'
      ],
      fix: 'Check if you meant == for comparison instead of = for assignment'
    }
  }
  
  return {
    message: 'Invalid syntax detected',
    causes: [
      '• Missing colons (:) after if/for/while/def/class',
      '• Unmatched parentheses, brackets, or braces',
      '• Incorrect indentation',
      '• Missing commas in lists/tuples',
      '• Invalid operator usage'
    ],
    fix: 'Check for missing colons, unmatched brackets, and proper indentation'
  }
}

// Real-time syntax checking
const checkSyntax = async () => {
  if (!pyodide || !code.value.trim()) {
    syntaxErrors.value = []
    updateEditorDiagnostics()
    return
  }
  
  try {
    // Store code in Pyodide's globals to avoid escaping issues
    pyodide.globals.set('__check_code', code.value)
    
    const checkCode = `
import ast
import json
try:
    ast.parse(__check_code)
    result = None
except SyntaxError as e:
    result = {
        "line": e.lineno if e.lineno else 1,
        "msg": str(e.msg) if e.msg else "Syntax error",
        "text": e.text if e.text else ""
    }
except Exception:
    result = None
json.dumps(result) if result else "null"
`
    
    const resultStr = pyodide.runPython(checkCode)
    const result = resultStr && resultStr !== 'null' ? JSON.parse(resultStr) : null
    
    if (result && result.line) {
      syntaxErrors.value = [{
        line: result.line,
        message: result.msg || 'Syntax error',
        suggestion: extractSyntaxErrorSuggestions(result.msg || '').fix
      }]
    } else {
      syntaxErrors.value = []
    }
  } catch (e: any) {
    // If JSON parsing fails or other errors, try direct compile check
    try {
      pyodide.globals.set('__check_code', code.value)
      pyodide.runPython('compile(__check_code, "<string>", "exec")')
      syntaxErrors.value = []
    } catch (compileError: any) {
      const errorStr = String(compileError)
      const lineMatch = errorStr.match(/line (\d+)/i) || errorStr.match(/\(line (\d+)\)/i)
      const lineNum = lineMatch && lineMatch[1] ? parseInt(lineMatch[1]) : 1
      
      if (errorStr.includes('SyntaxError') || errorStr.includes('invalid syntax')) {
        const msgMatch = errorStr.match(/(invalid syntax|SyntaxError[^:]*:?\s*)(.+?)(\n|$)/i)
        const errorMsg = msgMatch && msgMatch[2] ? msgMatch[2].trim() : 'Syntax error detected'
        
        syntaxErrors.value = [{
          line: lineNum,
          message: errorMsg,
          suggestion: extractSyntaxErrorSuggestions(errorStr).fix
        }]
      } else {
        // Not a syntax error, clear errors
        syntaxErrors.value = []
      }
    }
  }
  
  updateEditorDiagnostics()
}

// Update CodeMirror diagnostics
const updateEditorDiagnostics = () => {
  if (!editorView) return
  
  try {
    const diagnostics = syntaxErrors.value.map(error => {
      const lineNum = Math.min(Math.max(1, error.line), editorView!.state.doc.lines)
      const line = editorView!.state.doc.line(lineNum)
      return {
        from: line.from,
        to: Math.min(line.to, editorView!.state.doc.length),
        severity: 'error' as const,
        message: error.message + (error.suggestion ? `\n💡 ${error.suggestion}` : '')
      }
    })
    
    editorView.dispatch(setDiagnostics(editorView.state, diagnostics))
  } catch (e) {
    // Ignore errors in diagnostics update
  }
}

// Initialize CodeMirror editor
const initEditor = async () => {
  if (!editorContainer.value) return
  
  await nextTick()
  
  // Custom dark theme matching the app
  const customTheme = EditorView.theme({
    '&': {
      backgroundColor: '#1e293b', // msit-dark-700
      color: '#f1f5f9', // msit-dark-50
      fontSize: '14px'
    },
    '.cm-content': {
      padding: '12px',
      minHeight: '300px'
    },
    '.cm-focused': {
      outline: 'none'
    },
    '.cm-editor': {
      borderRadius: '6px'
    },
    '.cm-gutters': {
      backgroundColor: '#0f172a', // msit-dark-800
      borderRight: '1px solid #334155', // msit-dark-600
      color: '#64748b' // msit-dark-400
    },
    '.cm-lineNumbers .cm-gutterElement': {
      padding: '0 8px'
    },
    '.cm-activeLineGutter': {
      backgroundColor: '#1e293b'
    },
    '.cm-activeLine': {
      backgroundColor: '#1e293b'
    },
    '.cm-selectionMatch': {
      backgroundColor: '#3b82f6'
    }
  }, { dark: true })
  
  const state = EditorState.create({
    doc: code.value,
    extensions: [
      basicSetup,
      python(),
      customTheme,
      lintGutter(),
      EditorView.updateListener.of((update) => {
        if (update.docChanged && !isReceivingCodeUpdate.value) {
          code.value = update.state.doc.toString()
          saveToHistory()
          
          // Debounce syntax checking
          if (syntaxCheckTimeout) {
            clearTimeout(syntaxCheckTimeout)
          }
          syntaxCheckTimeout = setTimeout(() => {
            if (pyodide) {
              checkSyntax()
            }
          }, 500)
        }
        
        // Track cursor position and selection for pair programming
        if (isInPairSession.value && update.selectionSet && !isReceivingCodeUpdate.value) {
          const selection = update.state.selection.main
          const line = update.state.doc.lineAt(selection.head)
          const column = selection.head - line.from
          
          // Send cursor position
          pairProgrammingClient.sendCursorChange({
            line: line.number,
            column: column,
            lineNumber: line.number,
            character: column
          })
          
          // Send selection if there's a selection (not just cursor)
          if (selection.from !== selection.to) {
            const fromLine = update.state.doc.lineAt(selection.from)
            const toLine = update.state.doc.lineAt(selection.to)
            pairProgrammingClient.sendSelectionChange({
              from: {
                line: fromLine.number,
                column: selection.from - fromLine.from
              },
              to: {
                line: toLine.number,
                column: selection.to - toLine.from
              }
            })
          } else {
            // Clear selection
            pairProgrammingClient.sendSelectionChange(null)
          }
        }
      }),
      EditorView.domEventHandlers({
        paste: (e) => {
          e.preventDefault()
          showCopyWarningMessage()
        },
        copy: (e) => {
          e.preventDefault()
          showCopyWarningMessage()
        },
        cut: (e) => {
          e.preventDefault()
          showCopyWarningMessage()
        },
        contextmenu: (e) => {
          e.preventDefault()
          showCopyWarningMessage()
        }
      }),
      keymap.of([
        {
          key: 'Mod-Enter',
          run: () => {
            runPython()
            return true
          }
        }
      ])
    ]
  })
  
  editorView = new EditorView({
    state,
    parent: editorContainer.value
  })
}

// Watch for code changes from external sources
watch(() => code.value, (newCode) => {
  if (editorView && editorView.state.doc.toString() !== newCode) {
    editorView.dispatch({
      changes: {
        from: 0,
        to: editorView.state.doc.length,
        insert: newCode
      }
    })
  }
})

const studyTips = ref([
  {
    title: '💡 Start Simple',
    description: 'Begin with basic print statements and gradually add complexity. Master fundamentals before moving to advanced topics.'
  },
  {
    title: '📝 Read Error Messages',
    description: 'Python error messages tell you exactly what went wrong and where. Read them carefully - they\'re your best debugging tool!'
  },
  {
    title: '🔍 Use Print Statements',
    description: 'Add print() statements to see what values your variables have at different points in your code. This helps you understand what\'s happening.'
  },
  {
    title: '🎯 One Problem at a Time',
    description: 'Break complex problems into smaller pieces. Solve each piece separately, then combine them together.'
  },
  {
    title: '📚 Practice Regularly',
    description: 'Coding is a skill that improves with practice. Try writing code daily, even if it\'s just a few lines.'
  },
  {
    title: '🐍 Pythonic Style',
    description: 'Python values readability. Use meaningful variable names, add comments for complex logic, and follow PEP 8 style guidelines.'
  }
])

// Pair Programming Functions
const createPairSession = async () => {
  try {
    isCreatingSession.value = true
    pairProgrammingError.value = ''
    
    // Set user info (you can get this from auth if available)
    const username = localStorage.getItem('username') || `User${Math.floor(Math.random() * 1000)}`
    pairProgrammingClient.setUserInfo(username)
    
    // Connect to WebSocket
    pairProgrammingClient.connect()
    
    // Create session
    const sessionId = await pairProgrammingClient.createSession()
    pairSessionId.value = sessionId
    
    // Join the session
    await pairProgrammingClient.joinSession(sessionId)
    
    // Set up callbacks
    pairProgrammingClient.setCallbacks({
      onCodeUpdate: (newCode: string) => {
        if (newCode !== code.value) {
          isReceivingCodeUpdate.value = true
          code.value = newCode
          if (editorView) {
            editorView.dispatch({
              changes: {
                from: 0,
                to: editorView.state.doc.length,
                insert: newCode
              }
            })
          }
          setTimeout(() => {
            isReceivingCodeUpdate.value = false
          }, 100)
        }
      },
      onOutputUpdate: (newOutput: string) => {
        output.value = newOutput
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
      onCursorUpdate: (position: any, username: string) => {
        if (position && username) {
          cursorPositions.value.set(username, {
            line: position.line || position.lineNumber || 0,
            column: position.column || position.character || 0,
            username
          })
          // Remove cursor after 5 seconds of inactivity
          setTimeout(() => {
            cursorPositions.value.delete(username)
          }, 5000)
        }
      },
      onSelectionUpdate: (selection: any, username: string) => {
        // Handle selection updates - could be used to highlight selections
        if (selection && username) {
          // Store selections for visual indicators
          // This could be enhanced to show selections in the editor
        }
      },
      onTypingStart: (username: string) => {
        typingUsers.value.add(username)
      },
      onTypingStop: (username: string) => {
        typingUsers.value.delete(username)
      },
      onChatMessage: (message: ChatMessage) => {
        chatMessages.value.push(message)
        // Keep only last 100 messages
        if (chatMessages.value.length > 100) {
          chatMessages.value = chatMessages.value.slice(-100)
        }
        // Auto-scroll to bottom
        nextTick(() => {
          if (chatMessagesContainer.value) {
            chatMessagesContainer.value.scrollTop = chatMessagesContainer.value.scrollHeight
          }
        })
      },
      onError: (message: string) => {
        pairProgrammingError.value = message
      }
    })
    
    isInPairSession.value = true
    showPairProgramming.value = true
  } catch (error: any) {
    pairProgrammingError.value = error.message || 'Failed to create session'
  } finally {
    isCreatingSession.value = false
  }
}

const joinPairSession = async () => {
  if (!joinSessionId.value.trim()) {
    pairProgrammingError.value = 'Please enter a session ID'
    return
  }
  
  try {
    isJoiningSession.value = true
    pairProgrammingError.value = ''
    
    // Set user info
    const username = localStorage.getItem('username') || `User${Math.floor(Math.random() * 1000)}`
    pairProgrammingClient.setUserInfo(username)
    
    // Connect to WebSocket
    pairProgrammingClient.connect()
    
    // Join session
    await pairProgrammingClient.joinSession(joinSessionId.value.trim())
    pairSessionId.value = joinSessionId.value.trim()
    
    // Set up callbacks (same as create)
    pairProgrammingClient.setCallbacks({
      onCodeUpdate: (newCode: string) => {
        if (newCode !== code.value) {
          isReceivingCodeUpdate.value = true
          code.value = newCode
          if (editorView) {
            editorView.dispatch({
              changes: {
                from: 0,
                to: editorView.state.doc.length,
                insert: newCode
              }
            })
          }
          setTimeout(() => {
            isReceivingCodeUpdate.value = false
          }, 100)
        }
      },
      onOutputUpdate: (newOutput: string) => {
        output.value = newOutput
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
      onCursorUpdate: (position: any, username: string) => {
        if (position && username) {
          cursorPositions.value.set(username, {
            line: position.line || position.lineNumber || 0,
            column: position.column || position.character || 0,
            username
          })
          setTimeout(() => {
            cursorPositions.value.delete(username)
          }, 5000)
        }
      },
      onSelectionUpdate: (selection: any, username: string) => {
        // Store selections for potential visual indicators
        if (selection && username) {
          console.log(`Selection from ${username}:`, selection)
        }
      },
      onTypingStart: (username: string) => {
        typingUsers.value.add(username)
      },
      onTypingStop: (username: string) => {
        typingUsers.value.delete(username)
      },
      onChatMessage: (message: ChatMessage) => {
        chatMessages.value.push(message)
        if (chatMessages.value.length > 100) {
          chatMessages.value = chatMessages.value.slice(-100)
        }
      },
      onError: (message: string) => {
        pairProgrammingError.value = message
      }
    })
    
    isInPairSession.value = true
    showJoinDialog.value = false
    showPairProgramming.value = true
    
    // Save session to localStorage for persistence
    pairProgrammingClient.saveSessionToStorage()
  } catch (error: any) {
    pairProgrammingError.value = error.message || 'Failed to join session'
  } finally {
    isJoiningSession.value = false
  }
}

const leavePairSession = () => {
  pairProgrammingClient.leaveSession()
  pairProgrammingClient.disconnect()
  pairProgrammingClient.clearSessionStorage()
  isInPairSession.value = false
  pairSessionId.value = null
  participants.value = []
  pairProgrammingError.value = ''
  chatMessages.value = []
  chatInput.value = ''
  typingUsers.value.clear()
  cursorPositions.value.clear()
  if (typingTimeout) {
    clearTimeout(typingTimeout)
    typingTimeout = null
  }
}

// Restore session on mount
const restorePairSession = async () => {
  const savedSessionId = pairProgrammingClient.loadSessionFromStorage()
  if (savedSessionId) {
    try {
      const username = localStorage.getItem('username') || `User${Math.floor(Math.random() * 1000)}`
      pairProgrammingClient.setUserInfo(username)
      
      pairProgrammingClient.connect()
      await pairProgrammingClient.joinSession(savedSessionId)
      pairSessionId.value = savedSessionId
      
      // Set up callbacks (same as create/join)
      pairProgrammingClient.setCallbacks({
        onCodeUpdate: (newCode: string) => {
          if (newCode !== code.value) {
            isReceivingCodeUpdate.value = true
            code.value = newCode
            if (editorView) {
              editorView.dispatch({
                changes: {
                  from: 0,
                  to: editorView.state.doc.length,
                  insert: newCode
                }
              })
            }
            setTimeout(() => {
              isReceivingCodeUpdate.value = false
            }, 100)
          }
        },
        onOutputUpdate: (newOutput: string) => {
          output.value = newOutput
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
        onCursorUpdate: (position: any, username: string) => {
          if (position && username) {
            cursorPositions.value.set(username, {
              line: position.line || position.lineNumber || 0,
              column: position.column || position.character || 0,
              username
            })
            setTimeout(() => {
              cursorPositions.value.delete(username)
            }, 5000)
          }
        },
        onTypingStart: (username: string) => {
          typingUsers.value.add(username)
        },
        onTypingStop: (username: string) => {
          typingUsers.value.delete(username)
        },
        onChatMessage: (message: ChatMessage) => {
          chatMessages.value.push(message)
          if (chatMessages.value.length > 100) {
            chatMessages.value = chatMessages.value.slice(-100)
          }
        },
        onError: (message: string) => {
          pairProgrammingError.value = message
        }
      })
      
      isInPairSession.value = true
      showPairProgramming.value = true
    } catch (error: any) {
      // Session might have expired, clear it
      pairProgrammingClient.clearSessionStorage()
      console.error('Failed to restore session:', error)
    }
  }
}

const copySessionId = () => {
  if (pairSessionId.value) {
    navigator.clipboard.writeText(pairSessionId.value)
    // You could add a toast notification here
  }
}

const sendChatMessage = () => {
  if (chatInput.value.trim() && isInPairSession.value) {
    pairProgrammingClient.sendChatMessage(chatInput.value)
    chatInput.value = ''
    pairProgrammingClient.sendTypingStop()
    if (typingTimeout) {
      clearTimeout(typingTimeout)
      typingTimeout = null
    }
    // Auto-scroll after sending
    nextTick(() => {
      if (chatMessagesContainer.value) {
        chatMessagesContainer.value.scrollTop = chatMessagesContainer.value.scrollHeight
      }
    })
  }
}

const handleChatTyping = () => {
  if (isInPairSession.value && chatInput.value.trim()) {
    pairProgrammingClient.sendTypingStart()
    
    // Stop typing indicator after 3 seconds of inactivity
    if (typingTimeout) {
      clearTimeout(typingTimeout)
    }
    typingTimeout = setTimeout(() => {
      pairProgrammingClient.sendTypingStop()
    }, 3000)
  }
}

const formatTime = (date: Date): string => {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  
  if (seconds < 60) return 'just now'
  if (minutes < 60) return `${minutes}m ago`
  
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Watch for code changes to sync
watch(code, (newCode) => {
  if (isInPairSession.value && !isReceivingCodeUpdate.value && pairProgrammingClient.isConnected()) {
    // Debounce code changes
    if (codeChangeTimeout) {
      clearTimeout(codeChangeTimeout)
    }
    codeChangeTimeout = setTimeout(() => {
      pairProgrammingClient.sendCodeChange(newCode)
    }, 300)
  }
})

// Watch for output changes to sync
watch(output, (newOutput) => {
  if (isInPairSession.value && pairProgrammingClient.isConnected()) {
    pairProgrammingClient.sendOutputChange(newOutput)
  }
})

onMounted(async () => {
  loadHistory()

  // Check if code was passed from snippets page
  const savedCode = localStorage.getItem('compiler_code')
  if (savedCode) {
    code.value = savedCode
    localStorage.removeItem('compiler_code')
  }

  // Initialize CodeMirror editor
  await initEditor()

  // Add keyboard shortcuts
  window.addEventListener('keydown', handleKeyDown)

  // Try to restore pair programming session
  await restorePairSession()

  if ((window as any).loadPyodide) {
    loadPyodide()
  } else {
    const script = document.createElement('script')
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"
    script.onload = loadPyodide
    document.head.appendChild(script)
  }
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  if (isInPairSession.value) {
    leavePairSession()
  }
  if (codeChangeTimeout) {
    clearTimeout(codeChangeTimeout)
  }
  if (editorView) {
    editorView.destroy()
  }
  if (syntaxCheckTimeout) {
    clearTimeout(syntaxCheckTimeout)
  }
})
</script>

<style scoped>
.code-editor-container {
  min-height: 300px;
}

.code-editor-container :deep(.cm-editor) {
  border-radius: 6px;
}

.code-editor-container :deep(.cm-scroller) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace;
}

.code-editor-container :deep(.cm-lint-marker-error) {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath fill='%23ef4444' d='M6 0L0 6l6 6 6-6L6 0zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4z'/%3E%3C/svg%3E");
}

.code-editor-container :deep(.cm-lint-marker-warning) {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath fill='%23f59e0b' d='M6 0L0 6l6 6 6-6L6 0zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4z'/%3E%3C/svg%3E");
}
</style>
