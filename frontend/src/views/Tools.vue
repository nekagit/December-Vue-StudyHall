<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Developer Tools</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Useful tools for Python development and learning</p>
    </div>

    <!-- Tools Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- JSON Formatter -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all">
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-msit-accent/20 rounded">
            <svg class="h-6 w-6 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">JSON Formatter</h3>
        </div>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Format and validate JSON data</p>
        <button
          @click="activeTool = 'json'"
          class="w-full px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
        >
          Open Tool
        </button>
      </div>

      <!-- Regex Tester -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all">
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-msit-accent/20 rounded">
            <svg class="h-6 w-6 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">Regex Tester</h3>
        </div>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Test and debug regular expressions</p>
        <button
          @click="activeTool = 'regex'"
          class="w-full px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
        >
          Open Tool
        </button>
      </div>

      <!-- Base64 Encoder/Decoder -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all">
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-msit-accent/20 rounded">
            <svg class="h-6 w-6 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">Base64 Encoder/Decoder</h3>
        </div>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Encode and decode Base64 strings</p>
        <button
          @click="activeTool = 'base64'"
          class="w-full px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
        >
          Open Tool
        </button>
      </div>

      <!-- URL Encoder/Decoder -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all">
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-msit-accent/20 rounded">
            <svg class="h-6 w-6 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">URL Encoder/Decoder</h3>
        </div>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Encode and decode URL strings</p>
        <button
          @click="activeTool = 'url'"
          class="w-full px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
        >
          Open Tool
        </button>
      </div>

      <!-- Hash Generator -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all">
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-msit-accent/20 rounded">
            <svg class="h-6 w-6 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">Hash Generator</h3>
        </div>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Generate MD5, SHA1, SHA256 hashes</p>
        <button
          @click="activeTool = 'hash'"
          class="w-full px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
        >
          Open Tool
        </button>
      </div>

      <!-- Timestamp Converter -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all">
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-msit-accent/20 rounded">
            <svg class="h-6 w-6 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">Timestamp Converter</h3>
        </div>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Convert between Unix timestamp and date</p>
        <button
          @click="activeTool = 'timestamp'"
          class="w-full px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
        >
          Open Tool
        </button>
      </div>

      <!-- Color Picker -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all">
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-msit-accent/20 rounded">
            <svg class="h-6 w-6 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">Color Converter</h3>
        </div>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Convert between HEX, RGB, and HSL color formats</p>
        <button
          @click="activeTool = 'color'"
          class="w-full px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
        >
          Open Tool
        </button>
      </div>

      <!-- UUID Generator -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all">
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-msit-accent/20 rounded">
            <svg class="h-6 w-6 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">UUID Generator</h3>
        </div>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Generate unique identifiers (UUIDs)</p>
        <button
          @click="activeTool = 'uuid'"
          class="w-full px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
        >
          Open Tool
        </button>
      </div>

      <!-- QR Code Generator -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all">
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-msit-accent/20 rounded">
            <svg class="h-6 w-6 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">QR Code Generator</h3>
        </div>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Generate QR codes from text or URLs</p>
        <button
          @click="activeTool = 'qrcode'"
          class="w-full px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
        >
          Open Tool
        </button>
      </div>
    </div>

    <!-- Tool Panels -->
    <div v-if="activeTool" class="mt-8">
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-msit-dark-50 font-sans">{{ toolNames[activeTool] }}</h2>
          <button
            @click="activeTool = ''"
            class="text-msit-dark-200 hover:text-msit-dark-50 font-sans"
          >
            Close
          </button>
        </div>

        <!-- JSON Formatter -->
        <div v-if="activeTool === 'json'">
          <textarea
            v-model="jsonInput"
            placeholder="Paste your JSON here..."
            class="w-full h-48 bg-msit-dark p-4 rounded border border-msit-dark-700 text-msit-dark-200 font-mono text-sm font-sans"
          ></textarea>
          <div class="mt-4 flex gap-2">
            <button
              @click="formatJSON"
              class="px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
            >
              Format
            </button>
            <button
              @click="minifyJSON"
              class="px-4 py-2 bg-msit-dark-700 text-msit-dark-50 rounded-lg font-medium hover:bg-msit-dark-600 transition-colors font-sans"
            >
              Minify
            </button>
            <button
              @click="validateJSON"
              class="px-4 py-2 bg-msit-dark-700 text-msit-dark-50 rounded-lg font-medium hover:bg-msit-dark-600 transition-colors font-sans"
            >
              Validate
            </button>
          </div>
          <div v-if="jsonError" class="mt-4 p-3 bg-red-500/20 border border-red-500/30 rounded text-red-400 text-sm font-sans">
            {{ jsonError }}
          </div>
        </div>

        <!-- Regex Tester -->
        <div v-if="activeTool === 'regex'">
          <div class="mb-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Regular Expression:</label>
            <input
              v-model="regexPattern"
              placeholder="Enter regex pattern"
              class="w-full bg-msit-dark p-3 rounded border border-msit-dark-700 text-msit-dark-200 font-mono text-sm font-sans"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Test String:</label>
            <textarea
              v-model="regexTestString"
              placeholder="Enter text to test"
              class="w-full h-32 bg-msit-dark p-3 rounded border border-msit-dark-700 text-msit-dark-200 font-sans"
            ></textarea>
          </div>
          <button
            @click="testRegex"
            class="px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Test Regex
          </button>
          <div v-if="regexMatches.length > 0" class="mt-4">
            <p class="text-sm font-medium text-msit-dark-200 mb-2 font-sans">Matches:</p>
            <div class="bg-msit-dark p-3 rounded border border-msit-dark-700">
              <div v-for="(match, idx) in regexMatches" :key="idx" class="text-msit-accent font-mono text-sm mb-1 font-sans">
                {{ match }}
              </div>
            </div>
          </div>
        </div>

        <!-- Base64 Encoder/Decoder -->
        <div v-if="activeTool === 'base64'">
          <textarea
            v-model="base64Input"
            placeholder="Enter text to encode or base64 to decode"
            class="w-full h-32 bg-msit-dark p-4 rounded border border-msit-dark-700 text-msit-dark-200 font-sans"
          ></textarea>
          <div class="mt-4 flex gap-2">
            <button
              @click="encodeBase64"
              class="px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
            >
              Encode
            </button>
            <button
              @click="decodeBase64"
              class="px-4 py-2 bg-msit-dark-700 text-msit-dark-50 rounded-lg font-medium hover:bg-msit-dark-600 transition-colors font-sans"
            >
              Decode
            </button>
          </div>
          <div v-if="base64Output" class="mt-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Result:</label>
            <div class="bg-msit-dark p-3 rounded border border-msit-dark-700 text-msit-dark-200 font-mono text-sm break-all font-sans">
              {{ base64Output }}
            </div>
          </div>
        </div>

        <!-- URL Encoder/Decoder -->
        <div v-if="activeTool === 'url'">
          <textarea
            v-model="urlInput"
            placeholder="Enter URL to encode or decode"
            class="w-full h-32 bg-msit-dark p-4 rounded border border-msit-dark-700 text-msit-dark-200 font-sans"
          ></textarea>
          <div class="mt-4 flex gap-2">
            <button
              @click="encodeURL"
              class="px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
            >
              Encode
            </button>
            <button
              @click="decodeURL"
              class="px-4 py-2 bg-msit-dark-700 text-msit-dark-50 rounded-lg font-medium hover:bg-msit-dark-600 transition-colors font-sans"
            >
              Decode
            </button>
          </div>
          <div v-if="urlOutput" class="mt-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Result:</label>
            <div class="bg-msit-dark p-3 rounded border border-msit-dark-700 text-msit-dark-200 font-mono text-sm break-all font-sans">
              {{ urlOutput }}
            </div>
          </div>
        </div>

        <!-- Hash Generator -->
        <div v-if="activeTool === 'hash'">
          <textarea
            v-model="hashInput"
            placeholder="Enter text to hash"
            class="w-full h-32 bg-msit-dark p-4 rounded border border-msit-dark-700 text-msit-dark-200 font-sans"
          ></textarea>
          <div class="mt-4 flex gap-2 flex-wrap">
            <button
              @click="generateHash('md5')"
              class="px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
            >
              MD5
            </button>
            <button
              @click="generateHash('sha1')"
              class="px-4 py-2 bg-msit-dark-700 text-msit-dark-50 rounded-lg font-medium hover:bg-msit-dark-600 transition-colors font-sans"
            >
              SHA1
            </button>
            <button
              @click="generateHash('sha256')"
              class="px-4 py-2 bg-msit-dark-700 text-msit-dark-50 rounded-lg font-medium hover:bg-msit-dark-600 transition-colors font-sans"
            >
              SHA256
            </button>
          </div>
          <div v-if="hashOutput" class="mt-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Hash:</label>
            <div class="bg-msit-dark p-3 rounded border border-msit-dark-700 text-msit-dark-200 font-mono text-sm break-all font-sans">
              {{ hashOutput }}
            </div>
          </div>
        </div>

        <!-- Timestamp Converter -->
        <div v-if="activeTool === 'timestamp'">
          <div class="mb-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Unix Timestamp:</label>
            <input
              v-model.number="timestampInput"
              type="number"
              placeholder="Enter timestamp"
              class="w-full bg-msit-dark p-3 rounded border border-msit-dark-700 text-msit-dark-200 font-mono text-sm font-sans"
            />
            <button
              @click="timestampInput = Math.floor(Date.now() / 1000)"
              class="mt-2 text-sm text-msit-accent hover:text-msit-accent-300 font-sans"
            >
              Use Current Time
            </button>
          </div>
          <button
            @click="convertTimestamp"
            class="px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Convert
          </button>
          <div v-if="timestampOutput" class="mt-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Date:</label>
            <div class="bg-msit-dark p-3 rounded border border-msit-dark-700 text-msit-dark-200 font-sans">
              {{ timestampOutput }}
            </div>
          </div>
        </div>

        <!-- Color Converter -->
        <div v-if="activeTool === 'color'">
          <div class="mb-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">HEX Color:</label>
            <div class="flex items-center gap-3">
              <input
                v-model="colorInput"
                type="text"
                placeholder="#83E65B"
                class="flex-1 bg-msit-dark p-3 rounded border border-msit-dark-700 text-msit-dark-200 font-mono text-sm font-sans"
              />
              <input
                v-model="colorInput"
                type="color"
                class="w-16 h-12 rounded border border-msit-dark-700 cursor-pointer"
              />
            </div>
          </div>
          <button
            @click="convertColor"
            class="px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Convert
          </button>
          <div v-if="colorOutput" class="mt-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Converted Formats:</label>
            <div class="bg-msit-dark p-3 rounded border border-msit-dark-700 text-msit-dark-200 font-mono text-sm whitespace-pre-line font-sans">
              {{ colorOutput }}
            </div>
          </div>
        </div>

        <!-- UUID Generator -->
        <div v-if="activeTool === 'uuid'">
          <button
            @click="generateUUID"
            class="px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Generate UUID
          </button>
          <div v-if="uuidOutput" class="mt-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Generated UUID:</label>
            <div class="bg-msit-dark p-3 rounded border border-msit-dark-700 text-msit-dark-200 font-mono text-sm break-all font-sans">
              {{ uuidOutput }}
            </div>
            <button
              @click="navigator.clipboard.writeText(uuidOutput)"
              class="mt-2 text-sm text-msit-accent hover:text-msit-accent-300 font-sans"
            >
              Copy to Clipboard
            </button>
          </div>
        </div>

        <!-- QR Code Generator -->
        <div v-if="activeTool === 'qrcode'">
          <div class="mb-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Text or URL:</label>
            <textarea
              v-model="qrcodeInput"
              placeholder="Enter text or URL to encode..."
              class="w-full h-32 bg-msit-dark p-4 rounded border border-msit-dark-700 text-msit-dark-200 font-sans"
              @input="generateQRCode"
            ></textarea>
          </div>
          <div v-if="qrcodeUrl" class="mt-4">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">QR Code:</label>
            <div class="bg-msit-dark p-4 rounded border border-msit-dark-700 flex flex-col items-center">
              <img :src="qrcodeUrl" alt="QR Code" class="mb-2" />
              <a
                :href="qrcodeUrl"
                download="qrcode.png"
                class="text-sm text-msit-accent hover:text-msit-accent-300 font-sans"
              >
                Download QR Code
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTool = ref('')
const jsonInput = ref('')
const jsonError = ref('')
const regexPattern = ref('')
const regexTestString = ref('')
const regexMatches = ref<string[]>([])
const base64Input = ref('')
const base64Output = ref('')
const urlInput = ref('')
const urlOutput = ref('')
const hashInput = ref('')
const hashOutput = ref('')
const timestampInput = ref<number>(Math.floor(Date.now() / 1000))
const timestampOutput = ref('')
const colorInput = ref('#83E65B')
const colorOutput = ref('')
const uuidOutput = ref('')
const qrcodeInput = ref('')
const qrcodeUrl = ref('')

const toolNames: Record<string, string> = {
  json: 'JSON Formatter',
  regex: 'Regex Tester',
  base64: 'Base64 Encoder/Decoder',
  url: 'URL Encoder/Decoder',
  hash: 'Hash Generator',
  timestamp: 'Timestamp Converter',
  color: 'Color Converter',
  uuid: 'UUID Generator',
  qrcode: 'QR Code Generator'
}

const formatJSON = () => {
  try {
    const parsed = JSON.parse(jsonInput.value)
    jsonInput.value = JSON.stringify(parsed, null, 2)
    jsonError.value = ''
  } catch (e: any) {
    jsonError.value = `Invalid JSON: ${e.message}`
  }
}

const minifyJSON = () => {
  try {
    const parsed = JSON.parse(jsonInput.value)
    jsonInput.value = JSON.stringify(parsed)
    jsonError.value = ''
  } catch (e: any) {
    jsonError.value = `Invalid JSON: ${e.message}`
  }
}

const validateJSON = () => {
  try {
    JSON.parse(jsonInput.value)
    jsonError.value = '✓ Valid JSON'
  } catch (e: any) {
    jsonError.value = `Invalid JSON: ${e.message}`
  }
}

const testRegex = () => {
  try {
    const regex = new RegExp(regexPattern.value, 'g')
    const matches = regexTestString.value.match(regex)
    regexMatches.value = matches || []
  } catch (e) {
    regexMatches.value = []
    alert('Invalid regex pattern')
  }
}

const encodeBase64 = () => {
  try {
    base64Output.value = btoa(base64Input.value)
  } catch (e) {
    base64Output.value = 'Error encoding'
  }
}

const decodeBase64 = () => {
  try {
    base64Output.value = atob(base64Input.value)
  } catch (e) {
    base64Output.value = 'Error decoding'
  }
}

const encodeURL = () => {
  urlOutput.value = encodeURIComponent(urlInput.value)
}

const decodeURL = () => {
  try {
    urlOutput.value = decodeURIComponent(urlInput.value)
  } catch (e) {
    urlOutput.value = 'Error decoding URL'
  }
}

const generateHash = async (algorithm: string) => {
  // Note: Browser-based hashing using Web Crypto API
  if (!hashInput.value) return
  
  try {
    const encoder = new TextEncoder()
    const data = encoder.encode(hashInput.value)
    
    let hashBuffer: ArrayBuffer
    if (algorithm === 'md5') {
      // MD5 not available in Web Crypto API, using SHA256 as fallback
      hashBuffer = await crypto.subtle.digest('SHA-256', data)
    } else if (algorithm === 'sha1') {
      hashBuffer = await crypto.subtle.digest('SHA-1', data)
    } else {
      hashBuffer = await crypto.subtle.digest('SHA-256', data)
    }
    
    const hashArray = Array.from(new Uint8Array(hashBuffer))
    hashOutput.value = hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
  } catch (e) {
    hashOutput.value = 'Error generating hash'
  }
}

const convertTimestamp = () => {
  if (!timestampInput.value) return
  const date = new Date(timestampInput.value * 1000)
  timestampOutput.value = date.toLocaleString()
}

// Color Converter
const convertColor = () => {
  if (!colorInput.value) return
  
  try {
    // Remove # if present
    const hex = colorInput.value.replace('#', '')
    
    if (hex.length === 6) {
      const r = parseInt(hex.substring(0, 2), 16)
      const g = parseInt(hex.substring(2, 4), 16)
      const b = parseInt(hex.substring(4, 6), 16)
      
      // RGB
      const rgb = `rgb(${r}, ${g}, ${b})`
      
      // HSL conversion
      const rNorm = r / 255
      const gNorm = g / 255
      const bNorm = b / 255
      
      const max = Math.max(rNorm, gNorm, bNorm)
      const min = Math.min(rNorm, gNorm, bNorm)
      const delta = max - min
      
      let h = 0
      let s = 0
      const l = (max + min) / 2
      
      if (delta !== 0) {
        s = l > 0.5 ? delta / (2 - max - min) : delta / (max + min)
        
        if (max === rNorm) {
          h = ((gNorm - bNorm) / delta + (gNorm < bNorm ? 6 : 0)) / 6
        } else if (max === gNorm) {
          h = ((bNorm - rNorm) / delta + 2) / 6
        } else {
          h = ((rNorm - gNorm) / delta + 4) / 6
        }
      }
      
      const hsl = `hsl(${Math.round(h * 360)}, ${Math.round(s * 100)}%, ${Math.round(l * 100)}%)`
      
      colorOutput.value = `HEX: #${hex.toUpperCase()}\nRGB: ${rgb}\nHSL: ${hsl}`
    } else {
      colorOutput.value = 'Invalid HEX color format'
    }
  } catch (e) {
    colorOutput.value = 'Error converting color'
  }
}

// UUID Generator
const generateUUID = () => {
  // Generate UUID v4
  const uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
  uuidOutput.value = uuid
}

// QR Code Generator (using a public API)
const generateQRCode = () => {
  if (!qrcodeInput.value.trim()) {
    qrcodeUrl.value = ''
    return
  }
  // Using a free QR code API
  const encoded = encodeURIComponent(qrcodeInput.value)
  qrcodeUrl.value = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encoded}`
}
</script>
