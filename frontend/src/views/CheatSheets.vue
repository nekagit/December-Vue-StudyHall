<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Python Cheat Sheets</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Quick reference guides for Python syntax and common operations</p>
    </div>

    <!-- Search -->
    <div class="mb-6 bg-msit-dark-800 p-4 sm:p-6 rounded-lg shadow border border-msit-dark-700">
      <label for="search" class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Search Cheat Sheets</label>
      <input
        id="search"
        v-model="searchQuery"
        type="text"
        placeholder="Search by topic..."
        class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 placeholder-msit-dark-300 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-3 py-2.5 border font-sans"
      />
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-msit-accent"></div>
      <p class="mt-2 text-msit-dark-200 font-sans">Loading cheat sheets...</p>
    </div>

    <!-- Cheat Sheets Grid -->
    <div v-else-if="filteredSheets.length === 0" class="text-center py-12">
      <p class="text-msit-dark-200 font-sans">No cheat sheets found</p>
    </div>

    <div v-else class="grid grid-cols-1 gap-4 sm:gap-6 lg:grid-cols-2">
      <div
        v-for="sheet in filteredSheets"
        :key="sheet.id"
        class="bg-msit-dark-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent"
      >
        <div class="p-4 sm:p-6">
          <div class="flex items-start justify-between mb-4">
            <h3 class="text-lg sm:text-xl font-semibold text-msit-dark-50 font-sans">{{ sheet.title }}</h3>
            <button
              @click="expandedSheet = expandedSheet === sheet.id ? null : sheet.id"
              class="text-msit-dark-300 hover:text-msit-accent transition-colors"
            >
              <svg
                v-if="expandedSheet !== sheet.id"
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
              <svg
                v-else
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
              </svg>
            </button>
          </div>
          
          <p class="text-sm text-msit-dark-200 mb-4 font-sans">{{ sheet.description }}</p>
          
          <div v-if="expandedSheet === sheet.id" class="mt-4 space-y-4">
            <div
              v-for="(section, index) in sheet.sections"
              :key="index"
              class="bg-msit-dark-900 p-4 rounded border border-msit-dark-700"
            >
              <h4 class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">{{ section.title }}</h4>
              <pre class="text-xs text-msit-dark-200 font-mono whitespace-pre-wrap overflow-x-auto font-sans">{{ section.content }}</pre>
            </div>
          </div>
          
          <div class="mt-4 flex items-center gap-2">
            <button
              @click="copySheet(sheet)"
              class="flex-1 inline-flex items-center justify-center px-4 py-2 border border-msit-dark-600 text-sm font-medium rounded-md text-msit-dark-200 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
            >
              <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Copy
            </button>
            <button
              @click="expandedSheet = expandedSheet === sheet.id ? null : sheet.id"
              class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
            >
              {{ expandedSheet === sheet.id ? 'Collapse' : 'Expand' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'

const searchQuery = ref('')
const expandedSheet = ref<number | null>(null)
const cheatSheets = ref<any[]>([])
const loading = ref(false)

const loadCheatSheets = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (searchQuery.value) {
      params.append('search', searchQuery.value)
    }
    
    const response = await fetch(`/api/cheat-sheets?${params.toString()}`, {
      credentials: 'include'
    })
    if (response.ok) {
      cheatSheets.value = await response.json()
    }
  } catch (e) {
    console.error('Error loading cheat sheets:', e)
  } finally {
    loading.value = false
  }
}

// Legacy cheat sheets for fallback
const legacyCheatSheets = [
  {
    id: 1,
    title: 'Python Basics',
    description: 'Essential Python syntax and operations',
    sections: [
      {
        title: 'Variables and Types',
        content: `# Variables
name = "Python"
age = 30
height = 5.9
is_active = True

# Type checking
type(name)      # <class 'str'>
type(age)       # <class 'int'>
type(height)    # <class 'float'>
type(is_active) # <class 'bool'>`
      },
      {
        title: 'Basic Operations',
        content: `# Arithmetic
a + b    # Addition
a - b    # Subtraction
a * b    # Multiplication
a / b    # Division (float)
a // b   # Floor division
a % b    # Modulo
a ** b   # Exponentiation

# Comparison
a == b   # Equal
a != b   # Not equal
a < b    # Less than
a > b    # Greater than
a <= b   # Less or equal
a >= b   # Greater or equal`
      },
      {
        title: 'Print and Input',
        content: `# Print
print("Hello")
print(f"Value: {x}")  # f-string
print("A", "B", sep="-")  # A-B

# Input
name = input("Enter name: ")
age = int(input("Enter age: "))`
      }
    ]
  },
  {
    id: 2,
    title: 'Strings',
    description: 'String operations and methods',
    sections: [
      {
        title: 'String Creation',
        content: `# String literals
s1 = "Double quotes"
s2 = 'Single quotes'
s3 = """Multi-line
string"""
s4 = f"Formatted {variable}"`
      },
      {
        title: 'String Methods',
        content: `s.upper()           # Convert to uppercase
s.lower()           # Convert to lowercase
s.strip()           # Remove whitespace
s.replace(old, new) # Replace substring
s.split(sep)        # Split into list
s.join(iterable)    # Join iterable
s.startswith(prefix) # Check prefix
s.endswith(suffix)  # Check suffix
s.find(sub)         # Find index
s.count(sub)        # Count occurrences
len(s)              # Get length`
      },
      {
        title: 'String Formatting',
        content: `# f-strings (Python 3.6+)
name = "Alice"
age = 25
f"{name} is {age} years old"

# .format()
"{} is {} years old".format(name, age)
"{0} is {1} years old".format(name, age)
"{name} is {age} years old".format(name=name, age=age)

# % formatting (old style)
"%s is %d years old" % (name, age)`
      }
    ]
  },
  {
    id: 3,
    title: 'Lists',
    description: 'List operations and methods',
    sections: [
      {
        title: 'List Creation',
        content: `# Create lists
lst = [1, 2, 3]
lst = list(range(5))
lst = [x for x in range(10)]  # List comprehension
empty = []`
      },
      {
        title: 'List Operations',
        content: `lst[0]           # First element
lst[-1]          # Last element
lst[1:3]         # Slice
lst.append(x)    # Add to end
lst.insert(i, x) # Insert at index
lst.remove(x)    # Remove value
lst.pop(i)       # Remove and return
lst.extend(lst2) # Extend list
lst.index(x)     # Find index
lst.count(x)     # Count occurrences
len(lst)         # Length
sum(lst)         # Sum (numbers)
max(lst)         # Maximum
min(lst)         # Minimum`
      },
      {
        title: 'List Methods',
        content: `lst.sort()        # Sort in place
lst.reverse()    # Reverse in place
sorted(lst)      # Return sorted copy
reversed(lst)    # Return reversed iterator
lst.copy()       # Shallow copy
lst.clear()      # Clear list`
      }
    ]
  },
  {
    id: 4,
    title: 'Dictionaries',
    description: 'Dictionary operations and methods',
    sections: [
      {
        title: 'Dictionary Creation',
        content: `# Create dictionaries
d = {"key": "value"}
d = dict(key="value")
d = {k: v for k, v in items}  # Dict comprehension
empty = {}`
      },
      {
        title: 'Dictionary Operations',
        content: `d[key]           # Get value
d[key] = value   # Set value
d.get(key, default)  # Get with default
d.keys()         # Get keys
d.values()       # Get values
d.items()        # Get key-value pairs
del d[key]       # Delete key
key in d         # Check key exists
len(d)           # Length`
      },
      {
        title: 'Dictionary Methods',
        content: `d.update(d2)    # Update with another dict
d.pop(key)       # Remove and return
d.popitem()      # Remove last item
d.clear()        # Clear dictionary
d.copy()         # Shallow copy`
      }
    ]
  },
  {
    id: 5,
    title: 'Control Flow',
    description: 'If statements, loops, and control structures',
    sections: [
      {
        title: 'If Statements',
        content: `# If-elif-else
if condition:
    # code
elif other_condition:
    # code
else:
    # code

# Ternary operator
result = value if condition else other_value`
      },
      {
        title: 'For Loops',
        content: `# Iterate over sequence
for item in sequence:
    # code

# With index
for i, item in enumerate(sequence):
    # code

# Range
for i in range(10):
    # code

# Multiple sequences
for a, b in zip(seq1, seq2):
    # code`
      },
      {
        title: 'While Loops',
        content: `# While loop
while condition:
    # code

# Break and continue
while True:
    if condition:
        break      # Exit loop
    if other:
        continue   # Skip to next iteration`
      }
    ]
  },
  {
    id: 6,
    title: 'Functions',
    description: 'Function definition and usage',
    sections: [
      {
        title: 'Function Definition',
        content: `# Basic function
def function_name():
    return value

# With parameters
def func(param1, param2):
    return param1 + param2

# With default values
def func(param1, param2=10):
    return param1 + param2

# With type hints
def func(x: int, y: int) -> int:
    return x + y`
      },
      {
        title: 'Function Arguments',
        content: `# Positional arguments
func(1, 2)

# Keyword arguments
func(param1=1, param2=2)

# *args (variable positional)
def func(*args):
    # args is a tuple

# **kwargs (variable keyword)
def func(**kwargs):
    # kwargs is a dict`
      },
      {
        title: 'Lambda Functions',
        content: `# Lambda function
square = lambda x: x ** 2

# With map
result = list(map(lambda x: x*2, [1,2,3]))

# With filter
evens = list(filter(lambda x: x%2==0, [1,2,3]))

# With sorted
sorted(lst, key=lambda x: x[1])`
      }
    ]
  },
  {
    id: 7,
    title: 'File I/O',
    description: 'Reading and writing files',
    sections: [
      {
        title: 'Reading Files',
        content: `# Read entire file
with open("file.txt", "r") as f:
    content = f.read()

# Read line by line
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())

# Read all lines
with open("file.txt", "r") as f:
    lines = f.readlines()`
      },
      {
        title: 'Writing Files',
        content: `# Write to file
with open("file.txt", "w") as f:
    f.write("Hello\\n")
    f.write("World")

# Append to file
with open("file.txt", "a") as f:
    f.write("New line\\n")

# Write multiple lines
lines = ["Line 1", "Line 2"]
with open("file.txt", "w") as f:
    f.writelines(lines)`
      }
    ]
  },
  {
    id: 8,
    title: 'Error Handling',
    description: 'Try-except blocks and exception handling',
    sections: [
      {
        title: 'Basic Error Handling',
        content: `# Try-except
try:
    # code that might raise error
    result = 10 / 0
except ZeroDivisionError:
    # handle error
    print("Cannot divide by zero")

# Multiple exceptions
try:
    # code
except ValueError:
    # handle ValueError
except TypeError:
    # handle TypeError
except Exception as e:
    # handle any other exception
    print(f"Error: {e}")`
      },
      {
        title: 'Finally and Else',
        content: `try:
    # code
except Exception:
    # handle error
else:
    # runs if no exception
    print("Success")
finally:
    # always runs
    print("Cleanup")`
      },
      {
        title: 'Raising Exceptions',
        content: `# Raise exception
raise ValueError("Invalid value")

# Raise with custom message
if not condition:
    raise Exception("Error message")

# Re-raise exception
try:
    # code
except Exception:
    # handle
    raise  # Re-raise the exception`
      }
    ]
  }
]

const filteredSheets = computed(() => {
  // API already filters by search, so just return all if loaded
  return cheatSheets.value
})

const copySheet = (sheet: any) => {
  const content = sheet.sections
    .map((s: any) => `${s.title}\n${s.content}`)
    .join('\n\n')
  
  navigator.clipboard.writeText(content)
  alert('Cheat sheet copied to clipboard!')
}

// Watch for search query changes
let debounceTimer: ReturnType<typeof setTimeout> | null = null
watch(searchQuery, () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    loadCheatSheets()
  }, 300)
})

onMounted(() => {
  loadCheatSheets()
})
</script>
