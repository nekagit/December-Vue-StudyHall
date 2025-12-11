<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Code Templates</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Ready-to-use code templates and project starters</p>
    </div>

    <!-- Search -->
    <div class="mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search templates..."
        class="w-full px-4 py-2 bg-msit-dark-800 border border-msit-dark-700 rounded-lg text-msit-dark-50 placeholder-msit-dark-400 focus:outline-none focus:ring-2 focus:ring-msit-accent focus:border-transparent font-sans"
      />
    </div>

    <!-- Categories -->
    <div class="mb-6">
      <div class="flex flex-wrap gap-2">
        <button
          v-for="category in categories"
          :key="category"
          @click="selectedCategory = selectedCategory === category ? '' : category"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors font-sans',
            selectedCategory === category
              ? 'bg-msit-accent text-msit-dark'
              : 'bg-msit-dark-800 text-msit-dark-200 border border-msit-dark-700 hover:border-msit-accent'
          ]"
        >
          {{ category }}
        </button>
      </div>
    </div>

    <!-- Templates Grid -->
    <div v-if="filteredTemplates.length === 0" class="text-center py-12">
      <p class="text-msit-dark-300 font-sans">No templates found</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div
        v-for="template in filteredTemplates"
        :key="template.id"
        class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg overflow-hidden hover:border-msit-accent transition-all"
      >
        <div class="p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <h3 class="text-xl font-semibold text-msit-dark-50 mb-2 font-sans">{{ template.name }}</h3>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-msit-accent/20 text-msit-accent font-sans">
                {{ template.category }}
              </span>
            </div>
          </div>
          
          <p class="text-sm text-msit-dark-200 mb-4 font-sans">{{ template.description }}</p>

          <!-- Code Preview -->
          <div class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4 mb-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs text-msit-dark-400 font-sans">Preview</span>
              <button
                @click="togglePreview(template.id)"
                class="text-xs text-msit-accent hover:text-msit-accent-300 font-sans"
              >
                {{ showPreview[template.id] ? 'Hide' : 'Show' }} Code
              </button>
            </div>
            <pre v-if="showPreview[template.id]" class="text-xs text-msit-dark-200 font-mono overflow-x-auto max-h-60 overflow-y-auto"><code>{{ template.code }}</code></pre>
          </div>

          <!-- Features -->
          <div v-if="template.features && template.features.length > 0" class="mb-4">
            <h4 class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Features:</h4>
            <ul class="text-xs text-msit-dark-300 space-y-1 font-sans">
              <li v-for="feature in template.features" :key="feature" class="flex items-center gap-2">
                <svg class="h-3 w-3 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                {{ feature }}
              </li>
            </ul>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-3">
            <button
              @click="useTemplate(template)"
              class="flex-1 inline-flex items-center justify-center px-4 py-2 bg-msit-accent text-msit-dark rounded-lg hover:bg-msit-accent-500 transition-colors text-sm font-medium font-sans"
            >
              <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
              Use Template
            </button>
            <button
              @click="copyTemplate(template.code)"
              class="px-4 py-2 bg-msit-dark-700 text-msit-dark-200 rounded-lg hover:bg-msit-dark-600 transition-colors text-sm font-medium border border-msit-dark-600 font-sans"
            >
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')
const selectedCategory = ref('')
const showPreview = ref<Record<number, boolean>>({})

const templates = [
  {
    id: 1,
    name: 'Basic Python Script',
    category: 'Script',
    description: 'A simple Python script template with main function and command-line argument handling.',
    code: `#!/usr/bin/env python3
"""
Basic Python Script Template
"""

def main():
    print("Hello from Python script!")
    # Your code here

if __name__ == "__main__":
    main()`,
    features: ['Main function pattern', 'Command-line ready', 'Documentation header']
  },
  {
    id: 2,
    name: 'Class Template',
    category: 'OOP',
    description: 'A complete class template with constructor, methods, and properties.',
    code: `class MyClass:
    """Class documentation"""
    
    def __init__(self, param1, param2):
        """Initialize the class"""
        self.param1 = param1
        self.param2 = param2
    
    def method1(self):
        """Method documentation"""
        return self.param1
    
    def __str__(self):
        return f"MyClass({self.param1}, {self.param2})"
    
    def __repr__(self):
        return f"MyClass(param1={self.param1}, param2={self.param2})"

# Usage
obj = MyClass("value1", "value2")
print(obj)`,
    features: ['Constructor', 'Methods', 'String representation', 'Documentation']
  },
  {
    id: 3,
    name: 'REST API Client',
    category: 'API',
    description: 'Template for making HTTP requests and handling API responses.',
    code: `import requests
import json

class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json'
        }
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def get(self, endpoint):
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint, data):
        response = requests.post(
            f"{self.base_url}/{endpoint}",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

# Usage
# client = APIClient("https://api.example.com", api_key="your-key")
# result = client.get("users")`,
    features: ['GET requests', 'POST requests', 'Error handling', 'Headers management']
  },
  {
    id: 4,
    name: 'File Processor',
    category: 'File I/O',
    description: 'Template for reading, processing, and writing files.',
    code: `def process_file(input_file, output_file):
    """
    Process a file and write results to another file
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Process content here
        processed = content.upper()  # Example: convert to uppercase
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed)
        
        print(f"Processed {input_file} -> {output_file}")
        return True
    except FileNotFoundError:
        print(f"Error: File {input_file} not found")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Usage
# process_file("input.txt", "output.txt")`,
    features: ['File reading', 'File writing', 'Error handling', 'UTF-8 encoding']
  },
  {
    id: 5,
    name: 'Data Processing Pipeline',
    category: 'Data',
    description: 'Template for processing data through multiple stages.',
    code: `def process_data(data):
    """Process data through multiple stages"""
    
    # Stage 1: Filter
    filtered = [item for item in data if item > 0]
    
    # Stage 2: Transform
    transformed = [x * 2 for x in filtered]
    
    # Stage 3: Aggregate
    result = sum(transformed)
    
    return result

def pipeline(data):
    """Main pipeline function"""
    try:
        result = process_data(data)
        return {
            'success': True,
            'result': result,
            'count': len(data)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Usage
# data = [1, 2, 3, -1, 4, 5]
# result = pipeline(data)
# print(result)`,
    features: ['Data filtering', 'Data transformation', 'Aggregation', 'Error handling']
  },
  {
    id: 6,
    name: 'CLI Application',
    category: 'CLI',
    description: 'Command-line interface template with argument parsing.',
    code: `import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Description of your CLI tool'
    )
    parser.add_argument(
        'input',
        help='Input file or value'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file',
        default='output.txt'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Processing {args.input}...")
    
    # Your processing logic here
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())`,
    features: ['Argument parsing', 'Help messages', 'Verbose mode', 'Exit codes']
  },
  {
    id: 7,
    name: 'Context Manager',
    category: 'Advanced',
    description: 'Custom context manager template for resource management.',
    code: `class MyContextManager:
    """Custom context manager"""
    
    def __init__(self, resource):
        self.resource = resource
    
    def __enter__(self):
        print(f"Opening {self.resource}")
        # Initialize resource
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing {self.resource}")
        # Cleanup resource
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        return False  # Don't suppress exceptions
    
    def do_something(self):
        print("Doing something with resource")

# Usage
# with MyContextManager("file.txt") as cm:
#     cm.do_something()`,
    features: ['Context protocol', 'Resource management', 'Exception handling', 'Cleanup']
  },
  {
    id: 8,
    name: 'Decorator Template',
    category: 'Advanced',
    description: 'Function and class decorator templates.',
    code: `import functools
import time

def timer_decorator(func):
    """Decorator to measure function execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_attempts=3):
    """Decorator to retry function on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator

# Usage
# @timer_decorator
# @retry_decorator(max_attempts=3)
# def my_function():
#     # Your code
#     pass`,
    features: ['Function decorators', 'Parameterized decorators', 'functools.wraps', 'Error handling']
  }
]

const categories = computed(() => {
  const cats = new Set(templates.map(t => t.category))
  return Array.from(cats).sort()
})

const filteredTemplates = computed(() => {
  let result = templates
  
  if (selectedCategory.value) {
    result = result.filter(t => t.category === selectedCategory.value)
  }
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(t => 
      t.name.toLowerCase().includes(query) ||
      t.description.toLowerCase().includes(query) ||
      t.category.toLowerCase().includes(query) ||
      t.code.toLowerCase().includes(query)
    )
  }
  
  return result
})

const togglePreview = (id: number) => {
  showPreview.value[id] = !showPreview.value[id]
}

const useTemplate = (template: any) => {
  localStorage.setItem('compiler_code', template.code)
  router.push('/compiler')
}

const copyTemplate = async (code: string) => {
  try {
    await navigator.clipboard.writeText(code)
    alert('Template copied to clipboard!')
  } catch (e) {
    alert('Failed to copy template')
  }
}
</script>



