<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Code Snippets Library</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Browse and use ready-to-use Python code templates</p>
    </div>

    <!-- Search -->
    <div class="mb-6 bg-msit-dark-800 p-4 sm:p-6 rounded-lg shadow border border-msit-dark-700">
      <label for="search" class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Search Snippets</label>
      <input
        id="search"
        v-model="searchQuery"
        type="text"
        placeholder="Search snippets..."
        class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 placeholder-msit-dark-300 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-3 py-2.5 border font-sans"
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
            'px-4 py-2 rounded-md text-sm font-medium transition-colors font-sans',
            selectedCategory === category
              ? 'bg-msit-accent text-msit-dark'
              : 'bg-msit-dark-800 text-msit-dark-200 border border-msit-dark-700 hover:border-msit-accent'
          ]"
        >
          {{ category }}
        </button>
      </div>
    </div>

    <!-- Snippets Grid -->
    <div v-if="filteredSnippets.length === 0" class="text-center py-12">
      <p class="text-msit-dark-200 font-sans">No snippets found</p>
    </div>
    
    <div v-else class="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="snippet in filteredSnippets"
        :key="snippet.id"
        class="bg-msit-dark-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent"
      >
        <div class="p-4 sm:p-6">
          <div class="flex items-start justify-between mb-3">
            <div>
              <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">{{ snippet.name }}</h3>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-msit-accent/20 text-msit-accent mt-2 font-sans">
                {{ snippet.category }}
              </span>
            </div>
          </div>
          
          <p class="text-sm text-msit-dark-200 mb-4 font-sans">{{ snippet.description }}</p>
          
          <div class="bg-msit-dark-900 text-msit-accent p-3 rounded font-mono text-xs overflow-x-auto mb-4 max-h-40 overflow-y-auto border border-msit-dark-700">
            <pre class="whitespace-pre-wrap font-sans">{{ snippet.code }}</pre>
          </div>
          
          <div class="flex items-center gap-2">
            <button
              @click="copySnippet(snippet.code)"
              class="flex-1 inline-flex items-center justify-center px-3 py-2 border border-msit-dark-600 text-sm font-medium rounded-md text-msit-dark-200 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
            >
              <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Copy
            </button>
            <button
              @click="useInCompiler(snippet.code)"
              class="flex-1 inline-flex items-center justify-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
            >
              <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
              Use
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

const snippets = [
  {
    id: 1,
    name: 'Hello World',
    category: 'Basics',
    description: 'Basic print statement',
    code: 'print("Hello, World!")'
  },
  {
    id: 2,
    name: 'Variables and Types',
    category: 'Basics',
    description: 'Variable assignment and type checking',
    code: `name = "StudyHall"
age = 25
height = 5.9
is_student = True

print(f"Name: {name}, Type: {type(name).__name__}")
print(f"Age: {age}, Type: {type(age).__name__}")
print(f"Height: {height}, Type: {type(height).__name__}")
print(f"Is Student: {is_student}, Type: {type(is_student).__name__}")`
  },
  {
    id: 3,
    name: 'Lists Operations',
    category: 'Data Structures',
    description: 'Common list operations',
    code: `numbers = [1, 2, 3, 4, 5]
print(f"Original: {numbers}")
print(f"First: {numbers[0]}")
print(f"Last: {numbers[-1]}")
print(f"Sum: {sum(numbers)}")
print(f"Length: {len(numbers)}")
print(f"Max: {max(numbers)}")
print(f"Min: {min(numbers)}")`
  },
  {
    id: 4,
    name: 'List Methods',
    category: 'Data Structures',
    description: 'Adding, removing, and modifying list elements',
    code: `fruits = ["apple", "banana"]
fruits.append("orange")
fruits.insert(1, "grape")
fruits.remove("banana")
print(f"Fruits: {fruits}")

numbers = [3, 1, 4, 1, 5]
numbers.sort()
print(f"Sorted: {numbers}")
numbers.reverse()
print(f"Reversed: {numbers}")`
  },
  {
    id: 5,
    name: 'For Loops',
    category: 'Control Flow',
    description: 'Iterating with for loops',
    code: `# Iterate over range
for i in range(5):
    print(f"Number: {i}")

# Iterate over list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"Fruit: {fruit}")

# Iterate with index
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")`
  },
  {
    id: 6,
    name: 'While Loops',
    category: 'Control Flow',
    description: 'Conditional iteration',
    code: `# Basic while loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# Break and continue
num = 0
while num < 10:
    num += 1
    if num % 2 == 0:
        continue
    if num > 7:
        break
    print(f"Odd number: {num}")`
  },
  {
    id: 7,
    name: 'If-Else Statements',
    category: 'Control Flow',
    description: 'Conditional logic',
    code: `age = 20

if age < 18:
    print("Minor")
elif age < 65:
    print("Adult")
else:
    print("Senior")

# Ternary operator
status = "adult" if age >= 18 else "minor"
print(f"Status: {status}")`
  },
  {
    id: 8,
    name: 'Functions',
    category: 'Functions',
    description: 'Define and call functions',
    code: `def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

def multiply(a, b=1):
    return a * b

print(greet("StudyHall"))
print(f"5 + 3 = {add(5, 3)}")
print(f"5 * 3 = {multiply(5, 3)}")
print(f"5 * 1 = {multiply(5)}")`
  },
  {
    id: 9,
    name: 'Lambda Functions',
    category: 'Functions',
    description: 'Anonymous functions',
    code: `# Basic lambda
square = lambda x: x ** 2
print(f"5 squared: {square(5)}")

# Lambda with map
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(f"Squared: {squared}")

# Lambda with filter
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")`
  },
  {
    id: 10,
    name: 'Dictionaries',
    category: 'Data Structures',
    description: 'Key-value pairs',
    code: `student = {
    "name": "Alice",
    "age": 20,
    "courses": ["Python", "Web Dev"]
}

print(f"Name: {student['name']}")
print(f"Age: {student.get('age')}")
print(f"Courses: {', '.join(student['courses'])}")

# Iterate dictionary
for key, value in student.items():
    print(f"{key}: {value}")`
  },
  {
    id: 11,
    name: 'List Comprehension',
    category: 'Pythonic',
    description: 'Pythonic list operations',
    code: `# Square numbers
squares = [x**2 for x in range(10)]
print(f"Squares: {squares}")

# Filter even numbers
evens = [x for x in range(20) if x % 2 == 0]
print(f"Evens: {evens}")

# Nested comprehension
matrix = [[i*j for j in range(3)] for i in range(3)]
print(f"Matrix: {matrix}")`
  },
  {
    id: 12,
    name: 'Dictionary Comprehension',
    category: 'Pythonic',
    description: 'Create dictionaries efficiently',
    code: `# Square dictionary
squares = {x: x**2 for x in range(5)}
print(f"Squares dict: {squares}")

# Filter dictionary
numbers = {i: i*2 for i in range(10) if i % 2 == 0}
print(f"Even doubles: {numbers}")`
  },
  {
    id: 13,
    name: 'File Reading',
    category: 'File I/O',
    description: 'Read from files',
    code: `# Read entire file
with open("example.txt", "r") as f:
    content = f.read()
    print(content)

# Read line by line
with open("example.txt", "r") as f:
    for line in f:
        print(line.strip())

# Read all lines
with open("example.txt", "r") as f:
    lines = f.readlines()
    print(f"Total lines: {len(lines)}")`
  },
  {
    id: 14,
    name: 'File Writing',
    category: 'File I/O',
    description: 'Write to files',
    code: `# Write to file
with open("output.txt", "w") as f:
    f.write("Hello from StudyHall!\\n")
    f.write("This is line 2")

# Append to file
with open("output.txt", "a") as f:
    f.write("\\nThis is appended")

print("File written successfully!")`
  },
  {
    id: 15,
    name: 'String Methods',
    category: 'Strings',
    description: 'Common string operations',
    code: `text = "  Hello StudyHall  "

print(f"Original: '{text}'")
print(f"Upper: '{text.upper()}'")
print(f"Lower: '{text.lower()}'")
print(f"Strip: '{text.strip()}'")
print(f"Replace: '{text.replace('StudyHall', 'Python')}'")
print(f"Split: {text.strip().split()}")
print(f"Join: {'-'.join(['a', 'b', 'c'])}")`
  },
  {
    id: 16,
    name: 'Error Handling',
    category: 'Advanced',
    description: 'Try-except blocks',
    code: `# Basic error handling
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Multiple exceptions
try:
    value = int("not a number")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Other error: {e}")
finally:
    print("This always runs")`
  },
  {
    id: 17,
    name: 'Classes',
    category: 'OOP',
    description: 'Object-oriented programming',
    code: `class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"I'm {self.name}, {self.age} years old"

student = Student("Alice", 20)
print(student.introduce())`
  },
  {
    id: 18,
    name: 'Generators',
    category: 'Advanced',
    description: 'Memory-efficient iteration',
    code: `# Generator function
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for num in countdown(5):
    print(num)

# Generator expression
squares = (x**2 for x in range(5))
print(list(squares))`
  }
]

const categories = computed(() => {
  const cats = new Set(snippets.map(s => s.category))
  return Array.from(cats).sort()
})

const filteredSnippets = computed(() => {
  let result = snippets
  
  if (selectedCategory.value) {
    result = result.filter(s => s.category === selectedCategory.value)
  }
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(s => 
      s.name.toLowerCase().includes(query) ||
      s.description.toLowerCase().includes(query) ||
      s.category.toLowerCase().includes(query) ||
      s.code.toLowerCase().includes(query)
    )
  }
  
  return result
})

const copySnippet = (code: string) => {
  navigator.clipboard.writeText(code)
  alert('Code copied to clipboard!')
}

const useInCompiler = (code: string) => {
  localStorage.setItem('compiler_code', code)
  router.push('/compiler')
}
</script>
