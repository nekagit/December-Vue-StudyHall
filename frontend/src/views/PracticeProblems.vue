<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Practice Problems</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Solve coding challenges to improve your Python skills</p>
    </div>

    <!-- Search and Filter -->
    <div class="mb-6 bg-msit-dark-800 p-4 sm:p-6 rounded-lg shadow border border-msit-dark-700">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div>
          <label for="search" class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Search</label>
          <input
            id="search"
            v-model="searchQuery"
            type="text"
            placeholder="Search problems..."
            class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 placeholder-msit-dark-300 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-3 py-2.5 border font-sans"
          />
        </div>
        <div>
          <label for="difficulty" class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Difficulty</label>
          <select
            id="difficulty"
            v-model="selectedDifficulty"
            class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-3 py-2.5 border font-sans"
          >
            <option value="">All Levels</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
        <div>
          <label for="topic" class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Topic</label>
          <select
            id="topic"
            v-model="selectedTopic"
            class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-3 py-2.5 border font-sans"
          >
            <option value="">All Topics</option>
            <option v-for="topic in topics" :key="topic" :value="topic">{{ topic }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Problems Grid -->
    <div v-if="filteredProblems.length === 0" class="text-center py-12">
      <p class="text-msit-dark-200 font-sans">No problems found</p>
    </div>

    <div v-else class="grid grid-cols-1 gap-4 sm:gap-6 lg:grid-cols-2">
      <div
        v-for="problem in filteredProblems"
        :key="problem.id"
        class="bg-msit-dark-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent"
      >
        <div class="p-4 sm:p-6">
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <h3 class="text-lg sm:text-xl font-semibold text-msit-dark-50 mb-2 font-sans">
                {{ problem.title }}
              </h3>
              <div class="flex flex-wrap gap-2 mb-3">
                <span
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium font-sans',
                    problem.difficulty === 'beginner' ? 'bg-green-500/20 text-green-400' :
                    problem.difficulty === 'intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-red-500/20 text-red-400'
                  ]"
                >
                  {{ problem.difficulty }}
                </span>
                <span
                  v-for="tag in problem.tags"
                  :key="tag"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-msit-accent/20 text-msit-accent font-sans"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
          
          <p class="text-sm text-msit-dark-200 mb-4 font-sans">
            {{ problem.description }}
          </p>

          <div class="flex items-center justify-between pt-4 border-t border-msit-dark-700">
            <div class="text-xs text-msit-dark-300 font-sans">
              <span>{{ problem.points }} points</span>
              <span class="mx-2">•</span>
              <span>{{ problem.estimatedTime }} min</span>
            </div>
            <button
              @click="openProblem(problem)"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
            >
              Start Problem
              <svg class="ml-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Problem Detail Modal -->
    <div
      v-if="selectedProblem"
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
      @click.self="selectedProblem = null"
    >
      <div class="bg-msit-dark-800 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-msit-dark-700">
        <div class="p-6 border-b border-msit-dark-700">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h2 class="text-2xl font-bold text-msit-dark-50 mb-2 font-serif">{{ selectedProblem.title }}</h2>
              <div class="flex flex-wrap gap-2">
                <span
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium font-sans',
                    selectedProblem.difficulty === 'beginner' ? 'bg-green-500/20 text-green-400' :
                    selectedProblem.difficulty === 'intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-red-500/20 text-red-400'
                  ]"
                >
                  {{ selectedProblem.difficulty }}
                </span>
                <span
                  v-for="tag in selectedProblem.tags"
                  :key="tag"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-msit-accent/20 text-msit-accent font-sans"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
            <button
              @click="selectedProblem = null"
              class="text-msit-dark-300 hover:text-msit-dark-50 transition-colors"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-6 space-y-6">
          <div>
            <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">Description</h3>
            <p class="text-sm text-msit-dark-200 whitespace-pre-wrap font-sans">{{ selectedProblem.fullDescription }}</p>
          </div>
          
          <div v-if="selectedProblem.examples && selectedProblem.examples.length > 0">
            <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">Examples</h3>
            <div class="space-y-3">
              <div
                v-for="(example, idx) in selectedProblem.examples"
                :key="idx"
                class="bg-msit-dark-900 p-4 rounded border border-msit-dark-700"
              >
                <p class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Example {{ idx + 1 }}:</p>
                <pre class="text-xs text-msit-dark-200 font-mono mb-2"><code>Input: {{ example.input }}</code></pre>
                <pre class="text-xs text-msit-dark-200 font-mono"><code>Output: {{ example.output }}</code></pre>
              </div>
            </div>
          </div>
          
          <div v-if="selectedProblem.constraints">
            <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">Constraints</h3>
            <ul class="list-disc list-inside text-sm text-msit-dark-200 space-y-1 font-sans">
              <li v-for="(constraint, idx) in selectedProblem.constraints" :key="idx">{{ constraint }}</li>
            </ul>
          </div>
        </div>
        
        <div class="p-6 border-t border-msit-dark-700 flex justify-end gap-3">
          <button
            @click="selectedProblem = null"
            class="px-4 py-2 border border-msit-dark-600 text-msit-dark-50 rounded-md hover:bg-msit-dark-700 transition-colors font-sans"
          >
            Close
          </button>
          <button
            @click="solveProblem(selectedProblem)"
            class="px-4 py-2 border border-transparent text-sm font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Solve in Compiler
          </button>
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
const selectedDifficulty = ref('')
const selectedTopic = ref('')
const selectedProblem = ref<any>(null)

const problems = [
  {
    id: 1,
    title: 'Sum of Two Numbers',
    difficulty: 'beginner',
    tags: ['Basics', 'Math'],
    description: 'Write a function that takes two numbers and returns their sum.',
    fullDescription: 'Create a function called `add_numbers` that takes two parameters `a` and `b` and returns their sum.\n\nExample:\n- add_numbers(5, 3) should return 8\n- add_numbers(-1, 1) should return 0',
    points: 10,
    estimatedTime: 5,
    examples: [
      { input: 'add_numbers(5, 3)', output: '8' },
      { input: 'add_numbers(-1, 1)', output: '0' }
    ],
    constraints: ['Both inputs are integers', 'Result should be an integer']
  },
  {
    id: 2,
    title: 'Find Maximum in List',
    difficulty: 'beginner',
    tags: ['Lists', 'Loops'],
    description: 'Find the maximum value in a list without using the built-in max() function.',
    fullDescription: 'Write a function `find_max` that takes a list of numbers and returns the maximum value. Do not use Python\'s built-in `max()` function.\n\nExample:\n- find_max([1, 5, 3, 9, 2]) should return 9\n- find_max([-5, -2, -10]) should return -2',
    points: 15,
    estimatedTime: 10,
    examples: [
      { input: 'find_max([1, 5, 3, 9, 2])', output: '9' },
      { input: 'find_max([-5, -2, -10])', output: '-2' }
    ],
    constraints: ['List contains at least one element', 'All elements are numbers']
  },
  {
    id: 3,
    title: 'Reverse a String',
    difficulty: 'beginner',
    tags: ['Strings', 'Algorithms'],
    description: 'Reverse a string without using the built-in reverse() method.',
    fullDescription: 'Write a function `reverse_string` that takes a string and returns it reversed. Do not use Python\'s built-in string reversal methods.\n\nExample:\n- reverse_string("hello") should return "olleh"\n- reverse_string("Python") should return "nohtyP"',
    points: 15,
    estimatedTime: 10,
    examples: [
      { input: 'reverse_string("hello")', output: '"olleh"' },
      { input: 'reverse_string("Python")', output: '"nohtyP"' }
    ],
    constraints: ['Input is a non-empty string']
  },
  {
    id: 4,
    title: 'Count Vowels',
    difficulty: 'beginner',
    tags: ['Strings', 'Loops'],
    description: 'Count the number of vowels in a given string.',
    fullDescription: 'Write a function `count_vowels` that takes a string and returns the count of vowels (a, e, i, o, u). The function should be case-insensitive.\n\nExample:\n- count_vowels("Hello") should return 2\n- count_vowels("Python Programming") should return 5',
    points: 20,
    estimatedTime: 15,
    examples: [
      { input: 'count_vowels("Hello")', output: '2' },
      { input: 'count_vowels("Python Programming")', output: '5' }
    ],
    constraints: ['Input is a string', 'Case-insensitive matching']
  },
  {
    id: 5,
    title: 'Check Palindrome',
    difficulty: 'intermediate',
    tags: ['Strings', 'Algorithms'],
    description: 'Check if a string is a palindrome (reads the same forwards and backwards).',
    fullDescription: 'Write a function `is_palindrome` that takes a string and returns True if it is a palindrome, False otherwise. Ignore case and non-alphanumeric characters.\n\nExample:\n- is_palindrome("racecar") should return True\n- is_palindrome("Hello") should return False\n- is_palindrome("A man a plan a canal Panama") should return True',
    points: 25,
    estimatedTime: 20,
    examples: [
      { input: 'is_palindrome("racecar")', output: 'True' },
      { input: 'is_palindrome("Hello")', output: 'False' }
    ],
    constraints: ['Ignore case', 'Ignore spaces and punctuation']
  },
  {
    id: 6,
    title: 'Fibonacci Sequence',
    difficulty: 'intermediate',
    tags: ['Recursion', 'Algorithms'],
    description: 'Generate the first n numbers in the Fibonacci sequence.',
    fullDescription: 'Write a function `fibonacci` that takes an integer n and returns a list containing the first n Fibonacci numbers. The Fibonacci sequence starts with 0 and 1, and each subsequent number is the sum of the two preceding ones.\n\nExample:\n- fibonacci(5) should return [0, 1, 1, 2, 3]\n- fibonacci(10) should return [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]',
    points: 30,
    estimatedTime: 25,
    examples: [
      { input: 'fibonacci(5)', output: '[0, 1, 1, 2, 3]' },
      { input: 'fibonacci(10)', output: '[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]' }
    ],
    constraints: ['n is a positive integer', 'n >= 1']
  },
  {
    id: 7,
    title: 'Two Sum',
    difficulty: 'intermediate',
    tags: ['Arrays', 'Algorithms'],
    description: 'Find two numbers in an array that add up to a target value.',
    fullDescription: 'Write a function `two_sum` that takes a list of integers and a target integer. Return the indices of the two numbers that add up to the target. You may assume that each input has exactly one solution.\n\nExample:\n- two_sum([2, 7, 11, 15], 9) should return [0, 1] (because 2 + 7 = 9)\n- two_sum([3, 2, 4], 6) should return [1, 2]',
    points: 35,
    estimatedTime: 30,
    examples: [
      { input: 'two_sum([2, 7, 11, 15], 9)', output: '[0, 1]' },
      { input: 'two_sum([3, 2, 4], 6)', output: '[1, 2]' }
    ],
    constraints: ['Each input has exactly one solution', 'Cannot use the same element twice']
  },
  {
    id: 8,
    title: 'Anagram Checker',
    difficulty: 'intermediate',
    tags: ['Strings', 'Algorithms'],
    description: 'Check if two strings are anagrams of each other.',
    fullDescription: 'Write a function `are_anagrams` that takes two strings and returns True if they are anagrams (contain the same characters in different order), False otherwise. The function should be case-insensitive.\n\nExample:\n- are_anagrams("listen", "silent") should return True\n- are_anagrams("hello", "world") should return False',
    points: 30,
    estimatedTime: 20,
    examples: [
      { input: 'are_anagrams("listen", "silent")', output: 'True' },
      { input: 'are_anagrams("hello", "world")', output: 'False' }
    ],
    constraints: ['Case-insensitive', 'Ignore spaces']
  },
  {
    id: 9,
    title: 'Merge Sorted Lists',
    difficulty: 'advanced',
    tags: ['Lists', 'Algorithms'],
    description: 'Merge two sorted lists into one sorted list.',
    fullDescription: 'Write a function `merge_sorted` that takes two sorted lists and returns a new sorted list containing all elements from both lists.\n\nExample:\n- merge_sorted([1, 3, 5], [2, 4, 6]) should return [1, 2, 3, 4, 5, 6]\n- merge_sorted([1, 2], [3, 4]) should return [1, 2, 3, 4]',
    points: 40,
    estimatedTime: 35,
    examples: [
      { input: 'merge_sorted([1, 3, 5], [2, 4, 6])', output: '[1, 2, 3, 4, 5, 6]' },
      { input: 'merge_sorted([1, 2], [3, 4])', output: '[1, 2, 3, 4]' }
    ],
    constraints: ['Both input lists are sorted', 'Result should be sorted']
  },
  {
    id: 10,
    title: 'Binary Search',
    difficulty: 'advanced',
    tags: ['Algorithms', 'Search'],
    description: 'Implement binary search algorithm to find an element in a sorted list.',
    fullDescription: 'Write a function `binary_search` that takes a sorted list and a target value. Return the index of the target if found, or -1 if not found.\n\nExample:\n- binary_search([1, 2, 3, 4, 5], 3) should return 2\n- binary_search([1, 2, 3, 4, 5], 6) should return -1',
    points: 45,
    estimatedTime: 40,
    examples: [
      { input: 'binary_search([1, 2, 3, 4, 5], 3)', output: '2' },
      { input: 'binary_search([1, 2, 3, 4, 5], 6)', output: '-1' }
    ],
    constraints: ['Input list is sorted', 'Time complexity should be O(log n)']
  },
  {
    id: 11,
    title: 'Valid Parentheses',
    difficulty: 'intermediate',
    tags: ['Stacks', 'Strings'],
    description: 'Check if a string containing parentheses is valid.',
    fullDescription: 'Write a function `is_valid_parentheses` that takes a string containing only parentheses characters and returns True if the parentheses are balanced, False otherwise.\n\nExample:\n- is_valid_parentheses("()") should return True\n- is_valid_parentheses("()[]{}") should return True\n- is_valid_parentheses("(]") should return False',
    points: 35,
    estimatedTime: 25,
    examples: [
      { input: 'is_valid_parentheses("()")', output: 'True' },
      { input: 'is_valid_parentheses("()[]{}")', output: 'True' },
      { input: 'is_valid_parentheses("(]")', output: 'False' }
    ],
    constraints: ['String contains only parentheses characters', 'Use a stack data structure']
  },
  {
    id: 12,
    title: 'Remove Duplicates',
    difficulty: 'beginner',
    tags: ['Lists', 'Algorithms'],
    description: 'Remove duplicates from a list while preserving order.',
    fullDescription: 'Write a function `remove_duplicates` that takes a list and returns a new list with duplicates removed, preserving the original order.\n\nExample:\n- remove_duplicates([1, 2, 2, 3, 4, 4, 5]) should return [1, 2, 3, 4, 5]\n- remove_duplicates(["a", "b", "a", "c"]) should return ["a", "b", "c"]',
    points: 20,
    estimatedTime: 15,
    examples: [
      { input: 'remove_duplicates([1, 2, 2, 3, 4, 4, 5])', output: '[1, 2, 3, 4, 5]' },
      { input: 'remove_duplicates(["a", "b", "a", "c"])', output: '["a", "b", "c"]' }
    ],
    constraints: ['Preserve original order', 'Return a new list']
  },
  {
    id: 13,
    title: 'Bubble Sort',
    difficulty: 'intermediate',
    tags: ['Algorithms', 'Sorting'],
    description: 'Implement the bubble sort algorithm.',
    fullDescription: 'Write a function `bubble_sort` that takes a list of numbers and sorts them using the bubble sort algorithm.\n\nExample:\n- bubble_sort([64, 34, 25, 12, 22, 11, 90]) should return [11, 12, 22, 25, 34, 64, 90]',
    points: 40,
    estimatedTime: 30,
    examples: [
      { input: 'bubble_sort([64, 34, 25, 12, 22, 11, 90])', output: '[11, 12, 22, 25, 34, 64, 90]' }
    ],
    constraints: ['Sort in-place or return new list', 'Use bubble sort algorithm']
  },
  {
    id: 14,
    title: 'Prime Number Checker',
    difficulty: 'beginner',
    tags: ['Math', 'Algorithms'],
    description: 'Check if a number is prime.',
    fullDescription: 'Write a function `is_prime` that takes a number and returns True if it is prime, False otherwise.\n\nExample:\n- is_prime(7) should return True\n- is_prime(10) should return False\n- is_prime(1) should return False',
    points: 25,
    estimatedTime: 20,
    examples: [
      { input: 'is_prime(7)', output: 'True' },
      { input: 'is_prime(10)', output: 'False' },
      { input: 'is_prime(1)', output: 'False' }
    ],
    constraints: ['Handle edge cases (1, 2, negative numbers)', 'Optimize for large numbers']
  },
  {
    id: 15,
    title: 'Matrix Transpose',
    difficulty: 'intermediate',
    tags: ['Lists', 'Algorithms'],
    description: 'Transpose a matrix (2D list).',
    fullDescription: 'Write a function `transpose_matrix` that takes a 2D list (matrix) and returns its transpose.\n\nExample:\n- transpose_matrix([[1, 2, 3], [4, 5, 6]]) should return [[1, 4], [2, 5], [3, 6]]',
    points: 35,
    estimatedTime: 25,
    examples: [
      { input: 'transpose_matrix([[1, 2, 3], [4, 5, 6]])', output: '[[1, 4], [2, 5], [3, 6]]' }
    ],
    constraints: ['Handle rectangular matrices', 'Return a new matrix']
  }
]

const topics = computed(() => {
  const topicSet = new Set<string>()
  problems.forEach(p => p.tags.forEach(tag => topicSet.add(tag)))
  return Array.from(topicSet).sort()
})

const filteredProblems = computed(() => {
  let result = problems
  
  if (selectedDifficulty.value) {
    result = result.filter(p => p.difficulty === selectedDifficulty.value)
  }
  
  if (selectedTopic.value) {
    result = result.filter(p => p.tags.includes(selectedTopic.value))
  }
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(p => 
      p.title.toLowerCase().includes(query) ||
      p.description.toLowerCase().includes(query) ||
      p.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }
  
  return result
})

const openProblem = (problem: any) => {
  selectedProblem.value = problem
}

const solveProblem = (problem: any) => {
  const starterCode = `# ${problem.title}\n# ${problem.description}\n\ndef solution():\n    # Your code here\n    pass\n\n# Test your solution\nprint(solution())`
  localStorage.setItem('compiler_code', starterCode)
  selectedProblem.value = null
  router.push('/compiler')
}
</script>
