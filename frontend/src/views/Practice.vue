<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Practice Exercises</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Sharpen your Python skills with hands-on exercises</p>
    </div>

    <!-- Difficulty Filter -->
    <div class="mb-6">
      <div class="flex flex-wrap gap-2">
        <button
          v-for="difficulty in difficulties"
          :key="difficulty"
          @click="selectedDifficulty = selectedDifficulty === difficulty ? '' : difficulty"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors font-sans',
            selectedDifficulty === difficulty
              ? 'bg-msit-accent text-msit-dark'
              : 'bg-msit-dark-800 text-msit-dark-200 border border-msit-dark-700 hover:border-msit-accent'
          ]"
        >
          {{ difficulty }}
        </button>
      </div>
    </div>

    <!-- Exercises List -->
    <div v-if="filteredExercises.length === 0" class="text-center py-12">
      <p class="text-msit-dark-300 font-sans">No exercises found</p>
    </div>

    <div v-else class="space-y-6">
      <div
        v-for="exercise in filteredExercises"
        :key="exercise.id"
        class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <h3 class="text-xl font-semibold text-msit-dark-50 font-sans">{{ exercise.title }}</h3>
              <span :class="[
                'px-2.5 py-0.5 rounded-full text-xs font-medium font-sans',
                exercise.difficulty === 'Beginner' ? 'bg-green-500/20 text-green-400' :
                exercise.difficulty === 'Intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                'bg-red-500/20 text-red-400'
              ]">
                {{ exercise.difficulty }}
              </span>
            </div>
            <p class="text-sm text-msit-dark-200 mb-3 font-sans">{{ exercise.description }}</p>
          </div>
        </div>

        <!-- Problem Statement -->
        <div class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4 mb-4">
          <h4 class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Problem:</h4>
          <p class="text-sm text-msit-dark-200 whitespace-pre-line font-sans">{{ exercise.problem }}</p>
        </div>

        <!-- Example -->
        <div v-if="exercise.example" class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4 mb-4">
          <h4 class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Example:</h4>
          <pre class="text-sm text-msit-dark-200 font-mono overflow-x-auto"><code>{{ exercise.example }}</code></pre>
        </div>

        <!-- Hints -->
        <div v-if="exercise.hints && exercise.hints.length > 0" class="mb-4">
          <button
            @click="toggleHints(exercise.id)"
            class="text-sm text-msit-accent hover:text-msit-accent-300 font-sans"
          >
            {{ showHints[exercise.id] ? 'Hide' : 'Show' }} Hints ({{ exercise.hints.length }})
          </button>
          <div v-if="showHints[exercise.id]" class="mt-2 space-y-2">
            <div
              v-for="(hint, index) in exercise.hints"
              :key="index"
              class="bg-msit-dark-900 border border-msit-dark-700 rounded p-3 text-sm text-msit-dark-200 font-sans"
            >
              <strong class="text-msit-accent">Hint {{ index + 1 }}:</strong> {{ hint }}
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-3">
          <button
            @click="openInCompiler(exercise)"
            class="inline-flex items-center px-4 py-2 bg-msit-accent text-msit-dark rounded-lg hover:bg-msit-accent-500 transition-colors text-sm font-medium font-sans"
          >
            <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
            Solve in Compiler
          </button>
          <button
            @click="viewSolution(exercise)"
            class="inline-flex items-center px-4 py-2 bg-msit-dark-700 text-msit-dark-200 rounded-lg hover:bg-msit-dark-600 transition-colors text-sm font-medium border border-msit-dark-600 font-sans"
          >
            View Solution
          </button>
        </div>

        <!-- Solution (shown when clicked) -->
        <div v-if="showSolution[exercise.id]" class="mt-4 bg-msit-dark-900 border border-msit-accent rounded-lg p-4">
          <h4 class="text-sm font-semibold text-msit-accent mb-2 font-sans">Solution:</h4>
          <pre class="text-sm text-msit-dark-200 font-mono overflow-x-auto"><code>{{ exercise.solution }}</code></pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedDifficulty = ref('')
const showHints = ref<Record<number, boolean>>({})
const showSolution = ref<Record<number, boolean>>({})

const exercises = [
  {
    id: 1,
    title: 'Hello, World!',
    difficulty: 'Beginner',
    description: 'Write a program that prints "Hello, World!" to the console.',
    problem: 'Create a Python program that prints the message "Hello, World!"',
    example: 'Output:\nHello, World!',
    hints: ['Use the print() function', 'Pass a string as an argument'],
    solution: 'print("Hello, World!")'
  },
  {
    id: 2,
    title: 'Sum of Two Numbers',
    difficulty: 'Beginner',
    description: 'Write a function that takes two numbers and returns their sum.',
    problem: 'Create a function called add_numbers that takes two parameters (a and b) and returns their sum.',
    example: 'add_numbers(5, 3) should return 8\nadd_numbers(10, -5) should return 5',
    hints: ['Use the + operator', 'Return the result'],
    solution: 'def add_numbers(a, b):\n    return a + b'
  },
  {
    id: 3,
    title: 'Find Maximum',
    difficulty: 'Beginner',
    description: 'Write a function that finds the maximum of three numbers.',
    problem: 'Create a function that takes three numbers and returns the largest one.',
    example: 'find_max(3, 7, 2) should return 7\nfind_max(1, 1, 1) should return 1',
    hints: ['Use comparison operators', 'You can use if-elif-else statements', 'Or use the built-in max() function'],
    solution: 'def find_max(a, b, c):\n    return max(a, b, c)\n\n# Or:\ndef find_max(a, b, c):\n    if a >= b and a >= c:\n        return a\n    elif b >= c:\n        return b\n    else:\n        return c'
  },
  {
    id: 4,
    title: 'Count Vowels',
    difficulty: 'Intermediate',
    description: 'Write a function that counts the number of vowels in a string.',
    problem: 'Create a function that takes a string and returns the count of vowels (a, e, i, o, u) in it. Case-insensitive.',
    example: 'count_vowels("Hello") should return 2\ncount_vowels("Python") should return 1',
    hints: ['Convert string to lowercase', 'Use a loop to iterate through characters', 'Check if character is in a list of vowels'],
    solution: 'def count_vowels(text):\n    vowels = "aeiou"\n    count = 0\n    for char in text.lower():\n        if char in vowels:\n            count += 1\n    return count'
  },
  {
    id: 5,
    title: 'Reverse a String',
    difficulty: 'Beginner',
    description: 'Write a function that reverses a string without using built-in reverse methods.',
    problem: 'Create a function that takes a string and returns it reversed. Do not use [::-1] or reversed().',
    example: 'reverse_string("hello") should return "olleh"\nreverse_string("Python") should return "nohtyP"',
    hints: ['Use a loop', 'Build the reversed string character by character', 'Start from the end of the string'],
    solution: 'def reverse_string(text):\n    reversed_text = ""\n    for i in range(len(text) - 1, -1, -1):\n        reversed_text += text[i]\n    return reversed_text'
  },
  {
    id: 6,
    title: 'Factorial',
    difficulty: 'Intermediate',
    description: 'Write a function that calculates the factorial of a number.',
    problem: 'Create a function that calculates n! (n factorial). Use recursion.',
    example: 'factorial(5) should return 120\nfactorial(0) should return 1',
    hints: ['Factorial of n is n * factorial(n-1)', 'Base case: factorial(0) = 1'],
    solution: 'def factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    return n * factorial(n - 1)'
  },
  {
    id: 7,
    title: 'Check Palindrome',
    difficulty: 'Intermediate',
    description: 'Write a function that checks if a string is a palindrome.',
    problem: 'A palindrome reads the same forwards and backwards. Create a function that returns True if a string is a palindrome, False otherwise.',
    example: 'is_palindrome("racecar") should return True\nis_palindrome("hello") should return False',
    hints: ['Compare characters from start and end', 'Move towards the center', 'Ignore case if needed'],
    solution: 'def is_palindrome(text):\n    text = text.lower().replace(" ", "")\n    left = 0\n    right = len(text) - 1\n    while left < right:\n        if text[left] != text[right]:\n            return False\n        left += 1\n        right -= 1\n    return True'
  },
  {
    id: 8,
    title: 'List Sum',
    difficulty: 'Beginner',
    description: 'Write a function that sums all numbers in a list.',
    problem: 'Create a function that takes a list of numbers and returns their sum.',
    example: 'sum_list([1, 2, 3, 4]) should return 10\nsum_list([5, -3, 2]) should return 4',
    hints: ['Use a loop', 'Initialize a sum variable', 'Add each number to the sum'],
    solution: 'def sum_list(numbers):\n    total = 0\n    for num in numbers:\n        total += num\n    return total\n\n# Or using built-in:\ndef sum_list(numbers):\n    return sum(numbers)'
  },
  {
    id: 9,
    title: 'FizzBuzz',
    difficulty: 'Intermediate',
    description: 'Classic FizzBuzz problem.',
    problem: 'Write a program that prints numbers from 1 to n. For multiples of 3, print "Fizz". For multiples of 5, print "Buzz". For multiples of both, print "FizzBuzz".',
    example: 'For n=15: 1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz',
    hints: ['Use modulo operator (%)', 'Check for multiples of 15 first', 'Then check for 3 and 5'],
    solution: 'def fizzbuzz(n):\n    for i in range(1, n + 1):\n        if i % 15 == 0:\n            print("FizzBuzz")\n        elif i % 3 == 0:\n            print("Fizz")\n        elif i % 5 == 0:\n            print("Buzz")\n        else:\n            print(i)'
  },
  {
    id: 10,
    title: 'Find Duplicates',
    difficulty: 'Intermediate',
    description: 'Write a function that finds duplicate elements in a list.',
    problem: 'Create a function that takes a list and returns a list of duplicate elements.',
    example: 'find_duplicates([1, 2, 2, 3, 4, 4, 5]) should return [2, 4]',
    hints: ['Use a dictionary or set to track counts', 'Iterate through the list', 'Return elements that appear more than once'],
    solution: 'def find_duplicates(lst):\n    seen = {}\n    duplicates = []\n    for item in lst:\n        if item in seen:\n            if item not in duplicates:\n                duplicates.append(item)\n        else:\n            seen[item] = 1\n    return duplicates'
  }
]

const difficulties = computed(() => {
  const diffs = new Set(exercises.map(e => e.difficulty))
  return Array.from(diffs)
})

const filteredExercises = computed(() => {
  if (!selectedDifficulty.value) {
    return exercises
  }
  return exercises.filter(e => e.difficulty === selectedDifficulty.value)
})

const toggleHints = (id: number) => {
  showHints.value[id] = !showHints.value[id]
}

const viewSolution = (exercise: any) => {
  showSolution.value[exercise.id] = !showSolution.value[exercise.id]
}

const openInCompiler = (exercise: any) => {
  const code = `# ${exercise.title}\n# ${exercise.description}\n\n# Your solution here:\n\n`
  localStorage.setItem('compiler_code', code)
  router.push('/compiler')
}
</script>
