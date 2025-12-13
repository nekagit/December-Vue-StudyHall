<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Python Reference Library</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Quick reference guide for Python concepts, syntax, and common patterns</p>
    </div>

    <!-- Search -->
    <div class="mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search Python concepts..."
        class="w-full bg-msit-dark-800 border border-msit-dark-700 rounded-lg px-4 py-3 text-msit-dark-200 placeholder-msit-dark-400 focus:outline-none focus:border-msit-accent font-sans"
      />
    </div>

    <!-- Category Filter -->
    <div class="mb-6 flex flex-wrap gap-2">
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

    <!-- Reference Items -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div
        v-for="item in filteredItems"
        :key="item.id"
        class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all"
      >
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">{{ item.title }}</h3>
              <span class="px-2 py-1 rounded text-xs font-medium bg-msit-dark-700 text-msit-dark-200 font-sans">
                {{ item.category }}
              </span>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">{{ item.description }}</p>
          </div>
        </div>

        <!-- Syntax Example -->
        <div class="mb-4">
          <h4 class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Syntax:</h4>
          <div class="bg-msit-dark p-4 rounded border border-msit-dark-700 overflow-x-auto">
            <pre class="text-xs text-msit-dark-200 font-mono whitespace-pre-wrap font-sans">{{ item.syntax }}</pre>
          </div>
        </div>

        <!-- Example -->
        <div v-if="item.example" class="mb-4">
          <h4 class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Example:</h4>
          <div class="bg-msit-dark p-4 rounded border border-msit-dark-700 overflow-x-auto">
            <pre class="text-xs text-msit-dark-200 font-mono whitespace-pre-wrap font-sans">{{ item.example }}</pre>
          </div>
        </div>

        <!-- Notes -->
        <div v-if="item.notes" class="p-3 bg-msit-dark-900 rounded border border-msit-dark-700">
          <h4 class="text-xs font-semibold text-msit-dark-50 mb-1 font-sans">Notes:</h4>
          <p class="text-xs text-msit-dark-200 font-sans">{{ item.notes }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const searchQuery = ref('')
const selectedCategory = ref('')

const categories = ['Basics', 'Data Types', 'Control Flow', 'Functions', 'Data Structures', 'OOP', 'Advanced', 'Built-ins']

const items = [
  {
    id: 1,
    title: 'Variables',
    category: 'Basics',
    description: 'Variable assignment and naming conventions',
    syntax: 'variable_name = value',
    example: `# Variable assignment
name = "StudyHall"
age = 25
is_active = True
pi = 3.14159

# Multiple assignment
x, y, z = 1, 2, 3
a = b = c = 0`,
    notes: 'Python variables are dynamically typed. Use snake_case for variable names.'
  },
  {
    id: 2,
    title: 'Strings',
    category: 'Data Types',
    description: 'String operations and methods',
    syntax: `str.method()
str[index]
str[start:end:step]`,
    example: `text = "Hello StudyHall"
print(text.upper())        # HELLO STUDYHALL
print(text.lower())        # hello studyhall
print(text.replace("H", "h"))  # hello studyhall
print(text.split())        # ['Hello', 'StudyHall']
print(" ".join(['a', 'b']))  # a b
print(f"Value: {text}")     # Value: Hello StudyHall`,
    notes: 'Strings are immutable. Use f-strings for formatting (Python 3.6+).'
  },
  {
    id: 3,
    title: 'Lists',
    category: 'Data Structures',
    description: 'List creation, manipulation, and methods',
    syntax: `list = [item1, item2, ...]
list[index]
list[start:end]
list.method()`,
    example: `# Create list
numbers = [1, 2, 3, 4, 5]
fruits = ['apple', 'banana', 'orange']

# Access elements
print(numbers[0])      # 1
print(numbers[-1])     # 5 (last element)
print(numbers[1:3])    # [2, 3]

# Modify
numbers.append(6)      # Add to end
numbers.insert(0, 0)   # Insert at index
numbers.remove(3)      # Remove value
numbers.pop()          # Remove last

# List comprehension
squares = [x**2 for x in range(10)]`,
    notes: 'Lists are mutable and ordered. Use list comprehensions for efficiency.'
  },
  {
    id: 4,
    title: 'Dictionaries',
    category: 'Data Structures',
    description: 'Dictionary operations and methods',
    syntax: `dict = {key1: value1, key2: value2}
dict[key]
dict.get(key, default)
dict.keys()
dict.values()
dict.items()`,
    example: `# Create dictionary
student = {
    'name': 'Alice',
    'age': 20,
    'courses': ['Python', 'Web Dev']
}

# Access
print(student['name'])           # Alice
print(student.get('age', 0))     # 20
print(student.get('grade', 'N/A'))  # N/A

# Modify
student['age'] = 21
student['grade'] = 'A'
del student['courses']

# Iterate
for key, value in student.items():
    print(f"{key}: {value}")`,
    notes: 'Dictionaries are unordered (Python 3.7+ maintains insertion order). Keys must be hashable.'
  },
  {
    id: 5,
    title: 'If-Else Statements',
    category: 'Control Flow',
    description: 'Conditional statements',
    syntax: `if condition:
    # code
elif condition:
    # code
else:
    # code`,
    example: `age = 20

if age < 18:
    print("Minor")
elif age < 65:
    print("Adult")
else:
    print("Senior")

# Ternary operator
status = "adult" if age >= 18 else "minor"`,
    notes: 'Use elif for multiple conditions. Ternary operator for simple conditionals.'
  },
  {
    id: 6,
    title: 'For Loops',
    category: 'Control Flow',
    description: 'Iteration with for loops',
    syntax: `for item in iterable:
    # code

for i in range(start, end, step):
    # code`,
    example: `# Iterate over list
fruits = ['apple', 'banana', 'orange']
for fruit in fruits:
    print(fruit)

# With index
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

for i in range(1, 10, 2):
    print(i)  # 1, 3, 5, 7, 9`,
    notes: 'Use enumerate() to get index and value. range() generates numbers.'
  },
  {
    id: 7,
    title: 'While Loops',
    category: 'Control Flow',
    description: 'Conditional iteration',
    syntax: `while condition:
    # code
    if condition:
        break  # exit loop
    if condition:
        continue  # skip to next iteration`,
    example: `# Basic while loop
count = 0
while count < 5:
    print(count)
    count += 1

# Break and continue
num = 0
while num < 10:
    num += 1
    if num % 2 == 0:
        continue  # Skip even numbers
    if num > 7:
        break  # Exit when num > 7
    print(num)`,
    notes: 'Be careful with infinite loops. Always ensure condition becomes False.'
  },
  {
    id: 8,
    title: 'Functions',
    category: 'Functions',
    description: 'Function definition and calling',
    syntax: `def function_name(param1, param2=default):
    """Docstring"""
    # code
    return value`,
    example: `# Basic function
def greet(name):
    return f"Hello, {name}!"

# With default parameters
def add(a, b=0):
    return a + b

# With *args and **kwargs
def func(*args, **kwargs):
    print(args)   # tuple
    print(kwargs)  # dict

# Lambda function
square = lambda x: x ** 2`,
    notes: 'Use docstrings to document functions. *args for variable positional args, **kwargs for keyword args.'
  },
  {
    id: 9,
    title: 'Classes',
    category: 'OOP',
    description: 'Object-oriented programming with classes',
    syntax: `class ClassName:
    def __init__(self, param):
        self.param = param
    
    def method(self):
        # code`,
    example: `class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"I'm {self.name}, {self.age} years old"
    
    @classmethod
    def from_birth_year(cls, name, birth_year):
        age = 2024 - birth_year
        return cls(name, age)
    
    @staticmethod
    def is_adult(age):
        return age >= 18

student = Student("Alice", 20)
print(student.introduce())`,
    notes: '__init__ is the constructor. Use @classmethod for alternative constructors, @staticmethod for utility methods.'
  },
  {
    id: 10,
    title: 'List Comprehensions',
    category: 'Advanced',
    description: 'Pythonic way to create lists',
    syntax: `[expression for item in iterable if condition]
[expression for item1 in iterable1 for item2 in iterable2]`,
    example: `# Basic comprehension
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]

# Nested
matrix = [[i*j for j in range(3)] for i in range(3)]

# Dictionary comprehension
squares_dict = {x: x**2 for x in range(5)}`,
    notes: 'More readable and often faster than loops. Can be nested for multi-dimensional structures.'
  },
  {
    id: 11,
    title: 'Error Handling',
    category: 'Advanced',
    description: 'Try-except blocks for error handling',
    syntax: `try:
    # code
except ExceptionType as e:
    # handle error
finally:
    # always executes`,
    example: `try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Other error: {e}")
finally:
    print("This always runs")

# Raise exception
if age < 0:
    raise ValueError("Age cannot be negative")`,
    notes: 'Catch specific exceptions first, then general ones. Use finally for cleanup code.'
  },
  {
    id: 12,
    title: 'Generators',
    category: 'Advanced',
    description: 'Memory-efficient iteration',
    syntax: `def generator():
    yield value

gen = (expression for item in iterable)`,
    example: `# Generator function
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1

# Generator expression
squares = (x**2 for x in range(5))
print(list(squares))  # [0, 1, 4, 9, 16]`,
    notes: 'Generators are memory-efficient. Use yield instead of return. Lazy evaluation.'
  },
  {
    id: 13,
    title: 'File Operations',
    category: 'Built-ins',
    description: 'Reading and writing files',
    syntax: `with open(filename, mode) as file:
    # code

file.read()
file.readline()
file.readlines()
file.write()`,
    example: `# Read file
with open('data.txt', 'r') as f:
    content = f.read()
    print(content)

# Read line by line
with open('data.txt', 'r') as f:
    for line in f:
        print(line.strip())

# Write file
with open('output.txt', 'w') as f:
    f.write("Hello StudyHall!\\n")
    f.write("Line 2")`,
    notes: 'Always use with statement for file operations. Modes: r (read), w (write), a (append), r+ (read/write).'
  },
  {
    id: 14,
    title: 'Built-in Functions',
    category: 'Built-ins',
    description: 'Common built-in functions',
    syntax: `len(), range(), print(), input()
min(), max(), sum(), sorted()
enumerate(), zip(), map(), filter()
isinstance(), type(), dir(), help()`,
    example: `# Common functions
numbers = [3, 1, 4, 1, 5]
print(len(numbers))        # 5
print(min(numbers))        # 1
print(max(numbers))        # 5
print(sum(numbers))        # 14
print(sorted(numbers))     # [1, 1, 3, 4, 5]

# Useful functions
for i, val in enumerate(['a', 'b', 'c']):
    print(f"{i}: {val}")

zipped = zip([1, 2], ['a', 'b'])
print(list(zipped))  # [(1, 'a'), (2, 'b')]`,
    notes: 'Python has many built-in functions. Use help(function_name) to see documentation.'
  },
  {
    id: 15,
    title: 'Sets',
    category: 'Data Structures',
    description: 'Set operations and methods',
    syntax: `set = {item1, item2, ...}
set.add(item)
set.remove(item)
set.union(other)
set.intersection(other)`,
    example: `# Create set
fruits = {'apple', 'banana', 'orange'}
numbers = {1, 2, 3, 4, 5}

# Operations
fruits.add('grape')
fruits.remove('banana')

# Set operations
set1 = {1, 2, 3}
set2 = {3, 4, 5}
print(set1.union(set2))        # {1, 2, 3, 4, 5}
print(set1.intersection(set2))  # {3}
print(set1.difference(set2))    # {1, 2}`,
    notes: 'Sets are unordered and contain unique elements. Great for membership testing and set operations.'
  },
  {
    id: 16,
    title: 'Tuples',
    category: 'Data Structures',
    description: 'Immutable sequences',
    syntax: `tuple = (item1, item2, ...)
tuple[index]
tuple.count(value)
tuple.index(value)`,
    example: `# Create tuple
coordinates = (10, 20)
colors = ('red', 'green', 'blue')

# Access
print(coordinates[0])  # 10
print(colors[-1])      # blue

# Unpacking
x, y = coordinates

# Methods
print(colors.count('red'))  # 1
print(colors.index('green'))  # 1`,
    notes: 'Tuples are immutable. Use for fixed collections. Parentheses optional for single-item tuples.'
  }
]

const filteredItems = computed(() => {
  let result = items

  if (selectedCategory.value) {
    result = result.filter(item => item.category === selectedCategory.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(item =>
      item.title.toLowerCase().includes(query) ||
      item.description.toLowerCase().includes(query) ||
      item.category.toLowerCase().includes(query) ||
      item.syntax.toLowerCase().includes(query) ||
      (item.example && item.example.toLowerCase().includes(query))
    )
  }

  return result
})
</script>








