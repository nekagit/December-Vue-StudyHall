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

        <!-- Code Input -->
        <div class="mb-4">
          <label class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Your Code:</label>
            <textarea
              v-model="userCode[exercise.id]"
              :placeholder="`# ${exercise.title}\n# Write your solution here\n\n`"
              class="w-full bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-3 text-sm text-msit-dark-50 font-mono focus:border-msit-accent focus:ring-1 focus:ring-msit-accent outline-none resize-y min-h-[150px]"
              rows="8"
            ></textarea>
        </div>

        <!-- Actions -->
        <div class="flex flex-wrap items-center gap-3 mb-4">
          <button
            @click="runTestsForExercise(exercise)"
            :disabled="!userCode[exercise.id] || isLoading[exercise.id]"
            class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium font-sans disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="!isLoading[exercise.id]" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ isLoading[exercise.id] ? 'Running Tests...' : 'Run Tests' }}
          </button>
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

        <!-- Test Results -->
        <div v-if="testResults[exercise.id] && testResults[exercise.id].length > 0" class="mb-4">
          <div class="flex items-center justify-between mb-2">
            <h4 class="text-sm font-semibold text-msit-dark-50 font-sans">Test Results:</h4>
            <span :class="[
              'px-2 py-1 rounded text-xs font-medium font-sans',
              allTestsPassed(exercise.id) ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
            ]">
              {{ passedTestsCount(exercise.id) }} / {{ testResults[exercise.id].length }} passed
            </span>
          </div>
          <div class="space-y-2">
            <div
              v-for="(result, idx) in testResults[exercise.id]"
              :key="idx"
              :class="[
                'p-3 rounded-lg border font-sans',
                result.passed ? 'bg-green-500/10 border-green-500/30' : 'bg-red-500/10 border-red-500/30'
              ]"
            >
              <div class="flex items-start gap-2 mb-2">
                <svg v-if="result.passed" class="h-5 w-5 text-green-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <svg v-else class="h-5 w-5 text-red-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="flex-1">
                  <div class="text-xs font-mono text-msit-dark-200 mb-1">
                    <span class="font-semibold">Test {{ idx + 1 }}:</span> {{ result.testCase.input }}
                  </div>
                  <div v-if="result.passed" class="text-xs text-green-400">
                    ✓ Passed
                  </div>
                  <div v-else class="text-xs space-y-1">
                    <div class="text-red-400">
                      ✗ Failed
                    </div>
                    <div class="text-msit-dark-300">
                      <span class="font-semibold">Expected:</span> {{ result.expected }}
                    </div>
                    <div class="text-msit-dark-300">
                      <span class="font-semibold">Got:</span> {{ result.actual }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { runTests, loadPyodide, type TestCase, type TestResult } from '../utils/testRunner'

const router = useRouter()
const selectedDifficulty = ref('')
const showHints = ref<Record<number, boolean>>({})
const showSolution = ref<Record<number, boolean>>({})
const userCode = ref<Record<number, string>>({})
const testResults = ref<Record<number, TestResult[]>>({})
const isLoading = ref<Record<number, boolean>>({})
let pyodide: any = null

const exercises = [
  {
    id: 1,
    title: 'Hello, World!',
    difficulty: 'Beginner',
    description: 'Write a program that prints "Hello, World!" to the console.',
    problem: 'Create a Python program that prints the message "Hello, World!"',
    example: 'Output:\nHello, World!',
    hints: ['Use the print() function', 'Pass a string as an argument'],
    solution: 'print("Hello, World!")',
    testCases: [
      { input: 'print("Hello, World!")', output: 'Hello, World!' }
    ]
  },
  {
    id: 2,
    title: 'Sum of Two Numbers',
    difficulty: 'Beginner',
    description: 'Write a function that takes two numbers and returns their sum.',
    problem: 'Create a function called add_numbers that takes two parameters (a and b) and returns their sum.',
    example: 'add_numbers(5, 3) should return 8\nadd_numbers(10, -5) should return 5',
    hints: ['Use the + operator', 'Return the result'],
    solution: 'def add_numbers(a, b):\n    return a + b',
    testCases: [
      { input: 'add_numbers(5, 3)', output: '8' },
      { input: 'add_numbers(10, -5)', output: '5' },
      { input: 'add_numbers(0, 0)', output: '0' },
      { input: 'add_numbers(-1, 1)', output: '0' }
    ]
  },
  {
    id: 3,
    title: 'Find Maximum',
    difficulty: 'Beginner',
    description: 'Write a function that finds the maximum of three numbers.',
    problem: 'Create a function that takes three numbers and returns the largest one.',
    example: 'find_max(3, 7, 2) should return 7\nfind_max(1, 1, 1) should return 1',
    hints: ['Use comparison operators', 'You can use if-elif-else statements', 'Or use the built-in max() function'],
    solution: 'def find_max(a, b, c):\n    return max(a, b, c)\n\n# Or:\ndef find_max(a, b, c):\n    if a >= b and a >= c:\n        return a\n    elif b >= c:\n        return b\n    else:\n        return c',
    testCases: [
      { input: 'find_max(3, 7, 2)', output: '7' },
      { input: 'find_max(1, 1, 1)', output: '1' },
      { input: 'find_max(10, 5, 8)', output: '10' },
      { input: 'find_max(-5, -2, -10)', output: '-2' }
    ]
  },
  {
    id: 4,
    title: 'Count Vowels',
    difficulty: 'Intermediate',
    description: 'Write a function that counts the number of vowels in a string.',
    problem: 'Create a function that takes a string and returns the count of vowels (a, e, i, o, u) in it. Case-insensitive.',
    example: 'count_vowels("Hello") should return 2\ncount_vowels("Python") should return 1',
    hints: ['Convert string to lowercase', 'Use a loop to iterate through characters', 'Check if character is in a list of vowels'],
    solution: 'def count_vowels(text):\n    vowels = "aeiou"\n    count = 0\n    for char in text.lower():\n        if char in vowels:\n            count += 1\n    return count',
    testCases: [
      { input: 'count_vowels("Hello")', output: '2' },
      { input: 'count_vowels("Python")', output: '1' },
      { input: 'count_vowels("AEIOU")', output: '5' },
      { input: 'count_vowels("xyz")', output: '0' }
    ]
  },
  {
    id: 5,
    title: 'Reverse a String',
    difficulty: 'Beginner',
    description: 'Write a function that reverses a string without using built-in reverse methods.',
    problem: 'Create a function that takes a string and returns it reversed. Do not use [::-1] or reversed().',
    example: 'reverse_string("hello") should return "olleh"\nreverse_string("Python") should return "nohtyP"',
    hints: ['Use a loop', 'Build the reversed string character by character', 'Start from the end of the string'],
    solution: 'def reverse_string(text):\n    reversed_text = ""\n    for i in range(len(text) - 1, -1, -1):\n        reversed_text += text[i]\n    return reversed_text',
    testCases: [
      { input: 'reverse_string("hello")', output: '"olleh"' },
      { input: 'reverse_string("Python")', output: '"nohtyP"' },
      { input: 'reverse_string("a")', output: '"a"' },
      { input: 'reverse_string("123")', output: '"321"' }
    ]
  },
  {
    id: 6,
    title: 'Factorial',
    difficulty: 'Intermediate',
    description: 'Write a function that calculates the factorial of a number.',
    problem: 'Create a function that calculates n! (n factorial). Use recursion.',
    example: 'factorial(5) should return 120\nfactorial(0) should return 1',
    hints: ['Factorial of n is n * factorial(n-1)', 'Base case: factorial(0) = 1'],
    solution: 'def factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    return n * factorial(n - 1)',
    testCases: [
      { input: 'factorial(5)', output: '120' },
      { input: 'factorial(0)', output: '1' },
      { input: 'factorial(1)', output: '1' },
      { input: 'factorial(3)', output: '6' }
    ]
  },
  {
    id: 7,
    title: 'Check Palindrome',
    difficulty: 'Intermediate',
    description: 'Write a function that checks if a string is a palindrome.',
    problem: 'A palindrome reads the same forwards and backwards. Create a function that returns True if a string is a palindrome, False otherwise.',
    example: 'is_palindrome("racecar") should return True\nis_palindrome("hello") should return False',
    hints: ['Compare characters from start and end', 'Move towards the center', 'Ignore case if needed'],
    solution: 'def is_palindrome(text):\n    text = text.lower().replace(" ", "")\n    left = 0\n    right = len(text) - 1\n    while left < right:\n        if text[left] != text[right]:\n            return False\n        left += 1\n        right -= 1\n    return True',
    testCases: [
      { input: 'is_palindrome("racecar")', output: 'True' },
      { input: 'is_palindrome("hello")', output: 'False' },
      { input: 'is_palindrome("a")', output: 'True' },
      { input: 'is_palindrome("madam")', output: 'True' }
    ]
  },
  {
    id: 8,
    title: 'List Sum',
    difficulty: 'Beginner',
    description: 'Write a function that sums all numbers in a list.',
    problem: 'Create a function that takes a list of numbers and returns their sum.',
    example: 'sum_list([1, 2, 3, 4]) should return 10\nsum_list([5, -3, 2]) should return 4',
    hints: ['Use a loop', 'Initialize a sum variable', 'Add each number to the sum'],
    solution: 'def sum_list(numbers):\n    total = 0\n    for num in numbers:\n        total += num\n    return total\n\n# Or using built-in:\ndef sum_list(numbers):\n    return sum(numbers)',
    testCases: [
      { input: 'sum_list([1, 2, 3, 4])', output: '10' },
      { input: 'sum_list([5, -3, 2])', output: '4' },
      { input: 'sum_list([0])', output: '0' },
      { input: 'sum_list([-1, -2, -3])', output: '-6' }
    ]
  },
  {
    id: 9,
    title: 'FizzBuzz',
    difficulty: 'Intermediate',
    description: 'Classic FizzBuzz problem.',
    problem: 'Write a function that returns a list of strings. For numbers from 1 to n: For multiples of 3, return "Fizz". For multiples of 5, return "Buzz". For multiples of both, return "FizzBuzz". Otherwise return the number as a string.',
    example: 'fizzbuzz(15) should return ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]',
    hints: ['Use modulo operator (%)', 'Check for multiples of 15 first', 'Then check for 3 and 5', 'Return a list of strings'],
    solution: 'def fizzbuzz(n):\n    result = []\n    for i in range(1, n + 1):\n        if i % 15 == 0:\n            result.append("FizzBuzz")\n        elif i % 3 == 0:\n            result.append("Fizz")\n        elif i % 5 == 0:\n            result.append("Buzz")\n        else:\n            result.append(str(i))\n    return result',
    testCases: [
      { input: 'fizzbuzz(15)', output: '["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]' },
      { input: 'fizzbuzz(5)', output: '["1", "2", "Fizz", "4", "Buzz"]' },
      { input: 'fizzbuzz(3)', output: '["1", "2", "Fizz"]' }
    ]
  },
  {
    id: 10,
    title: 'Find Duplicates',
    difficulty: 'Intermediate',
    description: 'Write a function that finds duplicate elements in a list.',
    problem: 'Create a function that takes a list and returns a list of duplicate elements.',
    example: 'find_duplicates([1, 2, 2, 3, 4, 4, 5]) should return [2, 4]',
    hints: ['Use a dictionary or set to track counts', 'Iterate through the list', 'Return elements that appear more than once'],
    solution: 'def find_duplicates(lst):\n    seen = {}\n    duplicates = []\n    for item in lst:\n        if item in seen:\n            if item not in duplicates:\n                duplicates.append(item)\n        else:\n            seen[item] = 1\n    return duplicates',
    testCases: [
      { input: 'find_duplicates([1, 2, 2, 3, 4, 4, 5])', output: '[2, 4]' },
      { input: 'find_duplicates([1, 2, 3])', output: '[]' },
      { input: 'find_duplicates([1, 1, 1, 2, 2])', output: '[1, 2]' }
    ]
  },
  {
    id: 11,
    title: 'List Comprehension - Squares',
    difficulty: 'Beginner',
    description: 'Use list comprehension to create a list of squares.',
    problem: 'Write a function that takes a list of numbers and returns a list of their squares using list comprehension.',
    example: 'squares([1, 2, 3, 4]) should return [1, 4, 9, 16]',
    hints: ['Use list comprehension syntax: [expression for item in list]', 'Square a number using ** operator'],
    solution: 'def squares(numbers):\n    return [n ** 2 for n in numbers]',
    testCases: [
      { input: 'squares([1, 2, 3, 4])', output: '[1, 4, 9, 16]' },
      { input: 'squares([0, 5, 10])', output: '[0, 25, 100]' },
      { input: 'squares([-2, -1, 0, 1, 2])', output: '[4, 1, 0, 1, 4]' }
    ]
  },
  {
    id: 12,
    title: 'Filter Even Numbers',
    difficulty: 'Beginner',
    description: 'Filter even numbers from a list.',
    problem: 'Write a function that takes a list of numbers and returns only the even numbers.',
    example: 'filter_even([1, 2, 3, 4, 5, 6]) should return [2, 4, 6]',
    hints: ['Use modulo operator (%) to check if number is even', 'Use filter() or list comprehension'],
    solution: 'def filter_even(numbers):\n    return [n for n in numbers if n % 2 == 0]\n\n# Or using filter:\ndef filter_even(numbers):\n    return list(filter(lambda n: n % 2 == 0, numbers))',
    testCases: [
      { input: 'filter_even([1, 2, 3, 4, 5, 6])', output: '[2, 4, 6]' },
      { input: 'filter_even([1, 3, 5])', output: '[]' },
      { input: 'filter_even([0, 2, 4, 6, 8])', output: '[0, 2, 4, 6, 8]' }
    ]
  },
  {
    id: 13,
    title: 'Dictionary Merge',
    difficulty: 'Intermediate',
    description: 'Merge two dictionaries with conflict resolution.',
    problem: 'Write a function that merges two dictionaries. If there are duplicate keys, the value from the second dictionary should be used.',
    example: 'merge_dicts({"a": 1, "b": 2}, {"b": 3, "c": 4}) should return {"a": 1, "b": 3, "c": 4}',
    hints: ['Use dictionary unpacking **', 'Or use update() method', 'Second dict values take precedence'],
    solution: 'def merge_dicts(dict1, dict2):\n    return {**dict1, **dict2}\n\n# Or:\ndef merge_dicts(dict1, dict2):\n    result = dict1.copy()\n    result.update(dict2)\n    return result',
    testCases: [
      { input: 'merge_dicts({"a": 1, "b": 2}, {"b": 3, "c": 4})', output: "{'a': 1, 'b': 3, 'c': 4}" },
      { input: 'merge_dicts({"x": 10}, {"y": 20})', output: "{'x': 10, 'y': 20}" },
      { input: 'merge_dicts({}, {"a": 1})', output: "{'a': 1}" }
    ]
  },
  {
    id: 14,
    title: 'Count Words',
    difficulty: 'Intermediate',
    description: 'Count word frequency in a string.',
    problem: 'Write a function that takes a string and returns a dictionary with word frequencies (case-insensitive).',
    example: 'count_words("Hello hello world") should return {"hello": 2, "world": 1}',
    hints: ['Convert to lowercase', 'Split by spaces', 'Use dictionary to count'],
    solution: 'def count_words(text):\n    words = text.lower().split()\n    count = {}\n    for word in words:\n        count[word] = count.get(word, 0) + 1\n    return count',
    testCases: [
      { input: 'count_words("Hello hello world")', output: "{'hello': 2, 'world': 1}" },
      { input: 'count_words("Python is great Python")', output: "{'python': 2, 'is': 1, 'great': 1}" },
      { input: 'count_words("")', output: '{}' }
    ]
  },
  {
    id: 15,
    title: 'Binary Search',
    difficulty: 'Hard',
    description: 'Implement binary search algorithm.',
    problem: 'Write a function that performs binary search on a sorted list. Return the index if found, -1 otherwise.',
    example: 'binary_search([1, 3, 5, 7, 9], 5) should return 2',
    hints: ['Use two pointers (left and right)', 'Calculate middle index', 'Compare and adjust pointers'],
    solution: 'def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1',
    testCases: [
      { input: 'binary_search([1, 3, 5, 7, 9], 5)', output: '2' },
      { input: 'binary_search([1, 3, 5, 7, 9], 10)', output: '-1' },
      { input: 'binary_search([1, 2, 3, 4, 5], 1)', output: '0' },
      { input: 'binary_search([1, 2, 3, 4, 5], 5)', output: '4' }
    ]
  },
  {
    id: 16,
    title: 'Remove Duplicates',
    difficulty: 'Beginner',
    description: 'Remove duplicates from a list while preserving order.',
    problem: 'Write a function that removes duplicate elements from a list while maintaining the original order.',
    example: 'remove_duplicates([1, 2, 2, 3, 3, 3, 4]) should return [1, 2, 3, 4]',
    hints: ['Use a set to track seen elements', 'Or use dict.fromkeys()', 'Preserve order'],
    solution: 'def remove_duplicates(lst):\n    seen = set()\n    result = []\n    for item in lst:\n        if item not in seen:\n            seen.add(item)\n            result.append(item)\n    return result\n\n# Or simpler:\ndef remove_duplicates(lst):\n    return list(dict.fromkeys(lst))',
    testCases: [
      { input: 'remove_duplicates([1, 2, 2, 3, 3, 3, 4])', output: '[1, 2, 3, 4]' },
      { input: 'remove_duplicates([1, 1, 1])', output: '[1]' },
      { input: 'remove_duplicates([1, 2, 3])', output: '[1, 2, 3]' }
    ]
  },
  {
    id: 17,
    title: 'Prime Number Check',
    difficulty: 'Intermediate',
    description: 'Check if a number is prime.',
    problem: 'Write a function that checks if a number is prime (only divisible by 1 and itself).',
    example: 'is_prime(7) should return True, is_prime(10) should return False',
    hints: ['Check divisibility from 2 to sqrt(n)', 'Return False if divisible by any number', 'Handle edge cases (1, 2)'],
    solution: 'import math\n\ndef is_prime(n):\n    if n < 2:\n        return False\n    if n == 2:\n        return True\n    if n % 2 == 0:\n        return False\n    for i in range(3, int(math.sqrt(n)) + 1, 2):\n        if n % i == 0:\n            return False\n    return True',
    testCases: [
      { input: 'is_prime(7)', output: 'True' },
      { input: 'is_prime(10)', output: 'False' },
      { input: 'is_prime(2)', output: 'True' },
      { input: 'is_prime(1)', output: 'False' },
      { input: 'is_prime(17)', output: 'True' }
    ]
  },
  {
    id: 18,
    title: 'String Anagrams',
    difficulty: 'Intermediate',
    description: 'Check if two strings are anagrams.',
    problem: 'Write a function that checks if two strings are anagrams (contain the same characters in different order).',
    example: 'is_anagram("listen", "silent") should return True',
    hints: ['Sort both strings and compare', 'Or count character frequencies', 'Case-insensitive comparison'],
    solution: 'def is_anagram(s1, s2):\n    return sorted(s1.lower().replace(" ", "")) == sorted(s2.lower().replace(" ", ""))',
    testCases: [
      { input: 'is_anagram("listen", "silent")', output: 'True' },
      { input: 'is_anagram("hello", "world")', output: 'False' },
      { input: 'is_anagram("rail safety", "fairy tales")', output: 'True' },
      { input: 'is_anagram("python", "typhon")', output: 'True' }
    ]
  },
  {
    id: 19,
    title: 'Matrix Transpose',
    difficulty: 'Intermediate',
    description: 'Transpose a matrix (2D list).',
    problem: 'Write a function that transposes a matrix (swaps rows and columns).',
    example: 'transpose([[1, 2, 3], [4, 5, 6]]) should return [[1, 4], [2, 5], [3, 6]]',
    hints: ['Use nested list comprehension', 'Swap row and column indices', 'zip() can be helpful'],
    solution: 'def transpose(matrix):\n    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]\n\n# Or using zip:\ndef transpose(matrix):\n    return list(map(list, zip(*matrix)))',
    testCases: [
      { input: 'transpose([[1, 2, 3], [4, 5, 6]])', output: '[[1, 4], [2, 5], [3, 6]]' },
      { input: 'transpose([[1, 2], [3, 4]])', output: '[[1, 3], [2, 4]]' },
      { input: 'transpose([[1]])', output: '[[1]]' }
    ]
  },
  {
    id: 20,
    title: 'Flatten Nested List',
    difficulty: 'Hard',
    description: 'Flatten a nested list of any depth.',
    problem: 'Write a function that flattens a nested list structure of any depth into a single list.',
    example: 'flatten([1, [2, 3], [4, [5, 6]]]) should return [1, 2, 3, 4, 5, 6]',
    hints: ['Use recursion', 'Check if element is a list', 'Handle nested structures'],
    solution: 'def flatten(nested_list):\n    result = []\n    for item in nested_list:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result',
    testCases: [
      { input: 'flatten([1, [2, 3], [4, [5, 6]]])', output: '[1, 2, 3, 4, 5, 6]' },
      { input: 'flatten([1, 2, 3])', output: '[1, 2, 3]' },
      { input: 'flatten([[1], [2], [3]])', output: '[1, 2, 3]' }
    ]
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
  const code = userCode.value[exercise.id] || `# ${exercise.title}\n# ${exercise.description}\n\n# Your solution here:\n\n`
  localStorage.setItem('compiler_code', code)
  router.push('/compiler')
}

const runTestsForExercise = async (exercise: any) => {
  if (!userCode.value[exercise.id] || !exercise.testCases) return

  isLoading.value[exercise.id] = true

  try {
    if (!pyodide) {
      pyodide = await loadPyodide()
    }

    const results = await runTests(pyodide, userCode.value[exercise.id], exercise.testCases)
    testResults.value[exercise.id] = results
  } catch (error: any) {
    console.error('Test execution error:', error)
    testResults.value[exercise.id] = exercise.testCases.map((testCase: TestCase) => ({
      passed: false,
      expected: testCase.output,
      actual: `Error: ${error.message || String(error)}`,
      testCase
    }))
  } finally {
    isLoading.value[exercise.id] = false
  }
}

const passedTestsCount = (exerciseId: number): number => {
  if (!testResults.value[exerciseId]) return 0
  return testResults.value[exerciseId].filter(r => r.passed).length
}

const allTestsPassed = (exerciseId: number): boolean => {
  if (!testResults.value[exerciseId] || testResults.value[exerciseId].length === 0) return false
  return testResults.value[exerciseId].every(r => r.passed)
}

onMounted(async () => {
  // Initialize user code for each exercise
  exercises.forEach(exercise => {
    if (!userCode.value[exercise.id]) {
      userCode.value[exercise.id] = `# ${exercise.title}\n# ${exercise.description}\n\n# Your solution here:\n\n`
    }
  })
  
  // Preload Pyodide
  try {
    pyodide = await loadPyodide()
  } catch (error) {
    console.error('Failed to load Pyodide:', error)
  }
})
</script>
