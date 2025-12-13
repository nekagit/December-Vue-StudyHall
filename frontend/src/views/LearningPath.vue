<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Learning Paths</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Structured learning paths to master Python step by step</p>
    </div>

    <!-- View Toggle -->
    <div class="mb-6 flex gap-2">
      <button
        @click="viewMode = 'world'"
        :class="[
          'px-4 py-2 rounded-lg text-sm font-semibold transition-colors font-sans',
          viewMode === 'world' 
            ? 'bg-msit-accent text-msit-dark' 
            : 'bg-msit-dark-800 text-msit-dark-200 hover:bg-msit-dark-700 border border-msit-dark-700'
        ]"
      >
        World Map
      </button>
      <button
        @click="viewMode = 'grid'"
        :class="[
          'px-4 py-2 rounded-lg text-sm font-semibold transition-colors font-sans',
          viewMode === 'grid' 
            ? 'bg-msit-accent text-msit-dark' 
            : 'bg-msit-dark-800 text-msit-dark-200 hover:bg-msit-dark-700 border border-msit-dark-700'
        ]"
      >
        Grid View
      </button>
    </div>

    <!-- World Map View -->
    <div v-if="viewMode === 'world'" class="space-y-8">
      <div
        v-for="path in learningPaths"
        :key="path.id"
        class="bg-msit-dark-800 rounded-lg overflow-hidden border border-msit-dark-700"
      >
        <div class="p-4 sm:p-6 border-b border-msit-dark-700">
          <div class="flex items-start justify-between mb-2">
            <div class="flex-1">
              <h3 class="text-xl sm:text-2xl font-semibold text-msit-dark-50 mb-1 font-serif">{{ path.title }}</h3>
              <p class="text-sm text-msit-dark-200 font-sans">{{ path.description }}</p>
            </div>
            <span
              :class="[
                'inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold font-sans',
                path.level === 'Beginner' ? 'bg-green-500/20 text-green-400' :
                path.level === 'Intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                'bg-red-500/20 text-red-400'
              ]"
            >
              {{ path.level }}
            </span>
          </div>
        </div>
        
        <!-- World Map Path -->
        <div class="p-6 sm:p-8 relative overflow-x-auto">
          <div class="world-path-container" :style="{ minWidth: `${path.lessons.length * 120}px` }">
            <!-- Background Path -->
            <svg class="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none" style="pointer-events: none; z-index: 0;">
              <path
                v-for="(lesson, idx) in path.lessons.slice(0, -1)"
                :key="`path-${path.id}-${idx}`"
                :d="getPathD(idx, path.lessons.length)"
                stroke="rgba(131, 230, 91, 0.4)"
                stroke-width="0.5"
                fill="none"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="path-animation"
                :style="{ animationDelay: `${idx * 0.1}s` }"
              />
            </svg>
            
            <!-- Lesson Nodes -->
            <div class="relative" style="z-index: 1; height: 100px;">
              <div
                v-for="(lesson, idx) in path.lessons"
                :key="idx"
                class="lesson-node-container"
                :style="getNodePosition(idx, path.lessons.length)"
              >
                <!-- Node Circle -->
                <div
                  @click="selectLesson(lesson, path)"
                  :class="[
                    'lesson-node',
                    isLessonUnlocked(idx) ? 'lesson-unlocked' : 'lesson-locked',
                    selectedLesson?.title === lesson.title ? 'lesson-selected' : ''
                  ]"
                  :title="lesson.title"
                >
                  <!-- Node Icon -->
                  <div class="node-icon">
                    <svg v-if="lesson.type === 'Video'" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <svg v-else-if="lesson.type === 'Practice'" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <svg v-else-if="lesson.type === 'Project'" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    <svg v-else class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                  
                  <!-- Lesson Number -->
                  <div class="node-number">{{ idx + 1 }}</div>
                  
                  <!-- Checkmark for completed -->
                  <div v-if="isLessonCompleted(idx)" class="node-checkmark">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </div>
                
                <!-- Lesson Title Tooltip -->
                <div class="node-tooltip">
                  <div class="text-xs font-semibold text-msit-dark-50 mb-1 font-sans">{{ lesson.title }}</div>
                  <div class="text-xs text-msit-dark-300 font-sans">{{ lesson.duration }} min</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Grid View -->
    <div v-if="viewMode === 'grid'" class="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <div
        v-for="path in learningPaths"
        :key="path.id"
        class="bg-msit-dark-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent"
      >
        <div class="p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <h3 class="text-xl sm:text-2xl font-semibold text-msit-dark-50 mb-2 font-serif">{{ path.title }}</h3>
              <p class="text-sm text-msit-dark-200 mb-4 font-sans">{{ path.description }}</p>
            </div>
            <div class="ml-4">
              <span
                :class="[
                  'inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold font-sans',
                  path.level === 'Beginner' ? 'bg-green-500/20 text-green-400' :
                  path.level === 'Intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                  'bg-red-500/20 text-red-400'
                ]"
              >
                {{ path.level }}
              </span>
            </div>
          </div>

          <div class="mb-4">
            <div class="flex items-center justify-between text-xs text-msit-dark-300 mb-2 font-sans">
              <span>Progress</span>
              <span>{{ path.completedLessons }}/{{ path.totalLessons }} lessons</span>
            </div>
            <div class="w-full bg-msit-dark-700 rounded-full h-2">
              <div
                class="bg-msit-accent h-2 rounded-full transition-all duration-300"
                :style="{ width: `${(path.completedLessons / path.totalLessons) * 100}%` }"
              ></div>
            </div>
          </div>

          <div class="mb-4">
            <p class="text-xs font-semibold text-msit-dark-50 mb-2 font-sans">What you'll learn:</p>
            <ul class="space-y-1">
              <li
                v-for="(skill, idx) in path.skills"
                :key="idx"
                class="text-xs text-msit-dark-200 flex items-start font-sans"
              >
                <svg class="h-4 w-4 text-msit-accent mr-2 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                {{ skill }}
              </li>
            </ul>
          </div>

          <div class="flex items-center justify-between pt-4 border-t border-msit-dark-700">
            <div class="text-xs text-msit-dark-300 font-sans">
              <span>{{ path.estimatedTime }} hours</span>
              <span class="mx-2">•</span>
              <span>{{ path.totalLessons }} lessons</span>
            </div>
            <button
              @click="startPath(path)"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
            >
              Start Path
              <svg class="ml-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Path Detail Modal -->
    <div
      v-if="selectedPath"
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
      @click.self="selectedPath = null"
    >
      <div class="bg-msit-dark-800 rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto border border-msit-dark-700">
        <div class="p-6 border-b border-msit-dark-700">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h2 class="text-2xl font-bold text-msit-dark-50 mb-2 font-serif">{{ selectedPath.title }}</h2>
              <p class="text-sm text-msit-dark-200 font-sans">{{ selectedPath.description }}</p>
            </div>
            <button
              @click="selectedPath = null"
              class="text-msit-dark-300 hover:text-msit-dark-50 transition-colors ml-4 shrink-0"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <h3 class="text-lg font-semibold text-msit-dark-50 mb-4 font-sans">Lessons</h3>
          <div class="space-y-3">
            <div
              v-for="(lesson, idx) in selectedPath.lessons"
              :key="idx"
              @click="navigateToLesson(lesson)"
              class="flex items-start p-4 bg-msit-dark-900 rounded-lg border border-msit-dark-700 cursor-pointer hover:border-msit-accent hover:bg-msit-dark-800 transition-all"
            >
              <div class="shrink-0 w-8 h-8 rounded-full bg-msit-accent/20 flex items-center justify-center mr-4">
                <span class="text-sm font-semibold text-msit-accent font-sans">{{ idx + 1 }}</span>
              </div>
              <div class="flex-1">
                <h4 class="text-sm font-semibold text-msit-dark-50 mb-1 font-sans">{{ lesson.title }}</h4>
                <p class="text-xs text-msit-dark-300 font-sans">{{ lesson.description }}</p>
                <div class="mt-2 flex items-center gap-3 text-xs text-msit-dark-400 font-sans">
                  <span>{{ lesson.duration }} min</span>
                  <span v-if="lesson.type" class="px-2 py-0.5 bg-msit-dark-700 rounded">{{ lesson.type }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-6 border-t border-msit-dark-700 flex justify-end gap-3">
          <button
            @click="selectedPath = null"
            class="px-4 py-2 border border-msit-dark-600 text-msit-dark-50 rounded-md hover:bg-msit-dark-700 transition-colors font-sans"
          >
            Close
          </button>
          <button
            @click="startPath(selectedPath)"
            class="px-4 py-2 border border-transparent text-sm font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Start First Lesson
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
const selectedPath = ref<any>(null)
const viewMode = ref<'world' | 'grid'>('world')
const selectedLesson = ref<{ title: string; description: string; duration: number; type: string } | null>(null)

const learningPaths = [
  {
    id: 1,
    title: 'Python Basics',
    level: 'Beginner',
    description: 'Learn the fundamentals of Python programming from scratch.',
    totalLessons: 29,
    completedLessons: 0,
    estimatedTime: 15,
    skills: [
      'Variables and data types',
      'Basic operations and expressions',
      'Control flow (if/else, loops)',
      'Functions and modules',
      'Working with strings and lists',
      'File handling',
      'Error handling',
      'Code organization'
    ],
    lessons: [
      { title: 'Introduction to Python', description: 'What is Python and why learn it?', duration: 15, type: 'Video' },
      { title: 'Setting Up Python', description: 'Install Python and choose an IDE', duration: 20, type: 'Tutorial' },
      { title: 'Your First Program', description: 'Write and run your first Python script', duration: 25, type: 'Interactive' },
      { title: 'Variables and Data Types', description: 'Learn about integers, floats, strings, and booleans', duration: 30, type: 'Interactive' },
      { title: 'Type Conversion', description: 'Converting between different data types', duration: 25, type: 'Practice' },
      { title: 'Basic Operations', description: 'Arithmetic, comparison, and logical operators', duration: 25, type: 'Practice' },
      { title: 'String Basics', description: 'Introduction to string operations', duration: 30, type: 'Interactive' },
      { title: 'String Methods', description: 'String manipulation and formatting', duration: 35, type: 'Interactive' },
      { title: 'String Formatting', description: 'f-strings, format(), and % formatting', duration: 30, type: 'Practice' },
      { title: 'Lists Introduction', description: 'Creating and accessing lists', duration: 30, type: 'Interactive' },
      { title: 'List Methods', description: 'Working with list operations', duration: 35, type: 'Practice' },
      { title: 'Tuples and Sets', description: 'Working with tuples and sets', duration: 30, type: 'Interactive' },
      { title: 'Dictionaries', description: 'Key-value pairs and data structures', duration: 35, type: 'Interactive' },
      { title: 'Dictionary Operations', description: 'Accessing and modifying dictionaries', duration: 30, type: 'Practice' },
      { title: 'Conditional Statements', description: 'if, elif, else statements', duration: 30, type: 'Practice' },
      { title: 'Nested Conditionals', description: 'Complex conditional logic', duration: 25, type: 'Interactive' },
      { title: 'For Loops', description: 'Iterating with for loops', duration: 35, type: 'Interactive' },
      { title: 'While Loops', description: 'Using while loops effectively', duration: 30, type: 'Practice' },
      { title: 'Loop Control', description: 'break, continue, and else clauses', duration: 25, type: 'Interactive' },
      { title: 'Functions Basics', description: 'Defining and calling functions', duration: 40, type: 'Practice' },
      { title: 'Function Parameters', description: 'Arguments, defaults, and keyword arguments', duration: 35, type: 'Interactive' },
      { title: 'Return Values', description: 'Returning data from functions', duration: 30, type: 'Practice' },
      { title: 'Scope and Namespaces', description: 'Understanding variable scope', duration: 25, type: 'Tutorial' },
      { title: 'Lambda Functions', description: 'Anonymous functions and functional programming', duration: 30, type: 'Interactive' },
      { title: 'Modules and Packages', description: 'Importing and using libraries', duration: 30, type: 'Tutorial' },
      { title: 'File Handling', description: 'Reading and writing files', duration: 40, type: 'Practice' },
      { title: 'Error Handling', description: 'try, except, and exception handling', duration: 35, type: 'Interactive' },
      { title: 'Code Organization', description: 'Best practices for organizing code', duration: 25, type: 'Tutorial' },
      { title: 'Final Project', description: 'Build a simple Python application', duration: 90, type: 'Project' }
    ]
  },
  {
    id: 2,
    title: 'Object-Oriented Programming',
    level: 'Intermediate',
    description: 'Master classes, objects, inheritance, and polymorphism in Python.',
    totalLessons: 25,
    completedLessons: 0,
    estimatedTime: 20,
    skills: [
      'Classes and objects',
      'Inheritance and polymorphism',
      'Encapsulation',
      'Special methods',
      'Design patterns',
      'Abstract classes',
      'Composition vs inheritance',
      'Metaclasses'
    ],
    lessons: [
      { title: 'Introduction to OOP', description: 'Concepts of object-oriented programming', duration: 20, type: 'Video' },
      { title: 'OOP Principles', description: 'Encapsulation, inheritance, polymorphism, abstraction', duration: 25, type: 'Tutorial' },
      { title: 'Classes and Objects', description: 'Creating your first class', duration: 35, type: 'Interactive' },
      { title: 'Instance Attributes', description: 'Working with instance variables', duration: 30, type: 'Practice' },
      { title: 'Instance Methods', description: 'Defining methods in classes', duration: 35, type: 'Interactive' },
      { title: 'Class Attributes', description: 'Understanding class variables', duration: 30, type: 'Practice' },
      { title: 'Class Methods', description: 'Using @classmethod decorator', duration: 30, type: 'Interactive' },
      { title: 'Static Methods', description: 'Using @staticmethod decorator', duration: 25, type: 'Practice' },
      { title: 'Constructors', description: '__init__ and object initialization', duration: 30, type: 'Interactive' },
      { title: 'Destructors', description: '__del__ and cleanup methods', duration: 25, type: 'Tutorial' },
      { title: 'Properties', description: 'Using @property decorator', duration: 35, type: 'Interactive' },
      { title: 'Getter and Setter', description: 'Controlled attribute access', duration: 30, type: 'Practice' },
      { title: 'Inheritance Basics', description: 'Extending classes', duration: 40, type: 'Interactive' },
      { title: 'Multiple Inheritance', description: 'Inheriting from multiple classes', duration: 35, type: 'Practice' },
      { title: 'Method Resolution Order', description: 'Understanding MRO in Python', duration: 30, type: 'Tutorial' },
      { title: 'Polymorphism', description: 'Method overriding and duck typing', duration: 40, type: 'Interactive' },
      { title: 'Abstract Base Classes', description: 'Using abc module', duration: 35, type: 'Practice' },
      { title: 'Encapsulation', description: 'Private attributes and name mangling', duration: 35, type: 'Interactive' },
      { title: 'Special Methods', description: '__str__, __repr__, and more', duration: 40, type: 'Practice' },
      { title: 'Operator Overloading', description: 'Customizing operators with special methods', duration: 45, type: 'Interactive' },
      { title: 'Composition vs Inheritance', description: 'When to use composition', duration: 30, type: 'Tutorial' },
      { title: 'Design Patterns', description: 'Common OOP design patterns', duration: 50, type: 'Tutorial' },
      { title: 'Decorators in Classes', description: 'Using decorators with classes', duration: 35, type: 'Interactive' },
      { title: 'Data Classes', description: 'Using @dataclass decorator', duration: 30, type: 'Practice' },
      { title: 'OOP Project', description: 'Build an OOP-based application', duration: 120, type: 'Project' }
    ]
  },
  {
    id: 3,
    title: 'Data Structures & Algorithms',
    level: 'Intermediate',
    description: 'Learn essential data structures and algorithms for problem-solving.',
    totalLessons: 40,
    completedLessons: 0,
    estimatedTime: 35,
    skills: [
      'Arrays and linked lists',
      'Stacks and queues',
      'Trees and graphs',
      'Sorting algorithms',
      'Search algorithms',
      'Hash tables',
      'Recursion',
      'Dynamic programming'
    ],
    lessons: [
      { title: 'Introduction to Algorithms', description: 'What are algorithms and why they matter', duration: 25, type: 'Video' },
      { title: 'Algorithm Analysis', description: 'Understanding algorithm efficiency', duration: 30, type: 'Tutorial' },
      { title: 'Time Complexity', description: 'Big O notation and algorithm analysis', duration: 35, type: 'Tutorial' },
      { title: 'Space Complexity', description: 'Analyzing memory usage', duration: 25, type: 'Tutorial' },
      { title: 'Arrays and Lists', description: 'Working with arrays', duration: 30, type: 'Practice' },
      { title: 'Array Operations', description: 'Insertion, deletion, and searching', duration: 35, type: 'Interactive' },
      { title: 'Linked Lists Basics', description: 'Introduction to linked lists', duration: 40, type: 'Interactive' },
      { title: 'Singly Linked Lists', description: 'Implementing singly linked lists', duration: 45, type: 'Practice' },
      { title: 'Doubly Linked Lists', description: 'Implementing doubly linked lists', duration: 45, type: 'Interactive' },
      { title: 'Stacks', description: 'LIFO data structure', duration: 35, type: 'Practice' },
      { title: 'Stack Applications', description: 'Using stacks to solve problems', duration: 40, type: 'Interactive' },
      { title: 'Queues', description: 'FIFO data structure', duration: 35, type: 'Interactive' },
      { title: 'Priority Queues', description: 'Heap-based priority queues', duration: 40, type: 'Practice' },
      { title: 'Trees Introduction', description: 'Tree data structure basics', duration: 35, type: 'Tutorial' },
      { title: 'Binary Trees', description: 'Binary tree structure and properties', duration: 40, type: 'Interactive' },
      { title: 'Tree Traversal', description: 'Inorder, preorder, postorder traversal', duration: 50, type: 'Practice' },
      { title: 'Binary Search Trees', description: 'BST operations and properties', duration: 45, type: 'Interactive' },
      { title: 'AVL Trees', description: 'Self-balancing binary search trees', duration: 50, type: 'Tutorial' },
      { title: 'Graphs Introduction', description: 'Graph representation and types', duration: 40, type: 'Tutorial' },
      { title: 'Graph Representation', description: 'Adjacency list and matrix', duration: 35, type: 'Interactive' },
      { title: 'Graph Traversal', description: 'BFS and DFS algorithms', duration: 50, type: 'Practice' },
      { title: 'Shortest Path Algorithms', description: 'Dijkstra and Bellman-Ford', duration: 55, type: 'Interactive' },
      { title: 'Sorting Algorithms Basics', description: 'Introduction to sorting', duration: 30, type: 'Tutorial' },
      { title: 'Bubble and Selection Sort', description: 'Simple sorting algorithms', duration: 40, type: 'Practice' },
      { title: 'Insertion and Merge Sort', description: 'More efficient sorting methods', duration: 45, type: 'Interactive' },
      { title: 'Quick Sort', description: 'Divide and conquer sorting', duration: 50, type: 'Practice' },
      { title: 'Heap Sort', description: 'Heap-based sorting algorithm', duration: 45, type: 'Interactive' },
      { title: 'Search Algorithms', description: 'Linear and binary search', duration: 40, type: 'Interactive' },
      { title: 'Hash Tables', description: 'Dictionaries and hash maps', duration: 45, type: 'Practice' },
      { title: 'Hash Functions', description: 'Designing good hash functions', duration: 35, type: 'Tutorial' },
      { title: 'Collision Resolution', description: 'Handling hash collisions', duration: 40, type: 'Interactive' },
      { title: 'Recursion Basics', description: 'Understanding recursion', duration: 40, type: 'Tutorial' },
      { title: 'Recursive Problems', description: 'Solving problems with recursion', duration: 50, type: 'Interactive' },
      { title: 'Tail Recursion', description: 'Optimizing recursive functions', duration: 35, type: 'Practice' },
      { title: 'Dynamic Programming Intro', description: 'Introduction to DP', duration: 40, type: 'Tutorial' },
      { title: 'Memoization', description: 'Top-down DP approach', duration: 45, type: 'Interactive' },
      { title: 'Tabulation', description: 'Bottom-up DP approach', duration: 45, type: 'Practice' },
      { title: 'DP Patterns', description: 'Common DP patterns and problems', duration: 60, type: 'Tutorial' },
      { title: 'Greedy Algorithms', description: 'Greedy problem-solving strategies', duration: 45, type: 'Practice' },
      { title: 'Algorithm Project', description: 'Solve complex algorithmic problems', duration: 150, type: 'Project' }
    ]
  },
  {
    id: 4,
    title: 'Web Development with Python',
    level: 'Advanced',
    description: 'Build web applications using Flask and Django frameworks.',
    totalLessons: 30,
    completedLessons: 0,
    estimatedTime: 35,
    skills: [
      'Flask framework',
      'Django framework',
      'REST APIs',
      'Database integration',
      'Authentication',
      'Deployment',
      'Testing',
      'API design'
    ],
    lessons: [
      { title: 'Introduction to Web Development', description: 'HTTP, servers, and web architecture', duration: 30, type: 'Video' },
      { title: 'HTML and CSS Basics', description: 'Frontend fundamentals', duration: 40, type: 'Tutorial' },
      { title: 'JavaScript Basics', description: 'Client-side scripting', duration: 45, type: 'Tutorial' },
      { title: 'Flask Introduction', description: 'Getting started with Flask', duration: 35, type: 'Video' },
      { title: 'Flask Basics', description: 'Setting up your first Flask app', duration: 40, type: 'Interactive' },
      { title: 'Routing and Views', description: 'URL routing and view functions', duration: 35, type: 'Practice' },
      { title: 'Request and Response', description: 'Handling HTTP requests and responses', duration: 40, type: 'Interactive' },
      { title: 'Templates', description: 'Jinja2 templating engine', duration: 45, type: 'Interactive' },
      { title: 'Template Inheritance', description: 'Reusable templates and layouts', duration: 35, type: 'Practice' },
      { title: 'Forms and Validation', description: 'Handling user input', duration: 40, type: 'Practice' },
      { title: 'WTForms', description: 'Using WTForms for form handling', duration: 45, type: 'Interactive' },
      { title: 'Database Integration', description: 'SQLAlchemy and database models', duration: 60, type: 'Interactive' },
      { title: 'Database Migrations', description: 'Managing database schema changes', duration: 40, type: 'Practice' },
      { title: 'REST APIs', description: 'Building RESTful APIs', duration: 50, type: 'Practice' },
      { title: 'API Design', description: 'Best practices for API design', duration: 45, type: 'Tutorial' },
      { title: 'Authentication', description: 'User authentication and sessions', duration: 55, type: 'Interactive' },
      { title: 'Authorization', description: 'Role-based access control', duration: 45, type: 'Practice' },
      { title: 'Introduction to Django', description: 'Django framework overview', duration: 45, type: 'Video' },
      { title: 'Django Setup', description: 'Creating Django projects and apps', duration: 40, type: 'Interactive' },
      { title: 'Django Models', description: 'Database models in Django', duration: 50, type: 'Practice' },
      { title: 'Django ORM', description: 'Querying the database', duration: 45, type: 'Interactive' },
      { title: 'Django Views', description: 'Function and class-based views', duration: 45, type: 'Interactive' },
      { title: 'Django Templates', description: 'Template system and inheritance', duration: 40, type: 'Practice' },
      { title: 'Django Forms', description: 'Form handling in Django', duration: 45, type: 'Practice' },
      { title: 'Django Admin', description: 'Using Django admin interface', duration: 35, type: 'Tutorial' },
      { title: 'Django REST Framework', description: 'Building APIs with DRF', duration: 55, type: 'Interactive' },
      { title: 'Testing Web Apps', description: 'Unit and integration testing', duration: 50, type: 'Practice' },
      { title: 'Deployment Basics', description: 'Preparing apps for deployment', duration: 45, type: 'Tutorial' },
      { title: 'Deployment', description: 'Deploying Python web apps', duration: 60, type: 'Tutorial' },
      { title: 'Web Development Project', description: 'Build a full-stack web application', duration: 180, type: 'Project' }
    ]
  },
  {
    id: 5,
    title: 'Python for Data Science',
    level: 'Advanced',
    description: 'Learn data analysis, visualization, and machine learning with Python.',
    totalLessons: 24,
    completedLessons: 0,
    estimatedTime: 40,
    skills: [
      'NumPy and Pandas',
      'Data visualization',
      'Statistical analysis',
      'Machine learning basics',
      'Data cleaning and preprocessing',
      'Feature engineering',
      'Model evaluation',
      'Deep learning basics'
    ],
    lessons: [
      { title: 'Introduction to Data Science', description: 'Overview of data science workflow', duration: 25, type: 'Video' },
      { title: 'Python for Data Science', description: 'Essential libraries and tools', duration: 30, type: 'Tutorial' },
      { title: 'NumPy Introduction', description: 'Getting started with NumPy', duration: 35, type: 'Interactive' },
      { title: 'NumPy Arrays', description: 'Creating and manipulating arrays', duration: 40, type: 'Practice' },
      { title: 'NumPy Operations', description: 'Array operations and broadcasting', duration: 45, type: 'Interactive' },
      { title: 'NumPy Advanced', description: 'Advanced NumPy techniques', duration: 40, type: 'Practice' },
      { title: 'Pandas Introduction', description: 'Introduction to Pandas', duration: 35, type: 'Tutorial' },
      { title: 'Pandas Series', description: 'Working with Series', duration: 40, type: 'Interactive' },
      { title: 'Pandas DataFrames', description: 'DataFrames and basic operations', duration: 45, type: 'Practice' },
      { title: 'Data Loading', description: 'Reading CSV, JSON, and Excel files', duration: 40, type: 'Interactive' },
      { title: 'Data Inspection', description: 'Exploring and understanding data', duration: 35, type: 'Practice' },
      { title: 'Data Cleaning', description: 'Handling missing values and outliers', duration: 55, type: 'Practice' },
      { title: 'Data Transformation', description: 'Filtering, grouping, and aggregating data', duration: 50, type: 'Interactive' },
      { title: 'Data Merging', description: 'Combining datasets', duration: 45, type: 'Practice' },
      { title: 'Feature Engineering', description: 'Creating new features', duration: 50, type: 'Interactive' },
      { title: 'Matplotlib Basics', description: 'Creating basic plots and charts', duration: 45, type: 'Practice' },
      { title: 'Matplotlib Advanced', description: 'Customizing plots and subplots', duration: 50, type: 'Interactive' },
      { title: 'Seaborn Introduction', description: 'Statistical data visualization', duration: 40, type: 'Tutorial' },
      { title: 'Seaborn Visualization', description: 'Advanced visualization techniques', duration: 50, type: 'Interactive' },
      { title: 'Statistical Analysis', description: 'Descriptive statistics and distributions', duration: 55, type: 'Tutorial' },
      { title: 'Hypothesis Testing', description: 'Statistical tests and significance', duration: 50, type: 'Practice' },
      { title: 'Correlation Analysis', description: 'Understanding relationships in data', duration: 40, type: 'Practice' },
      { title: 'Introduction to Machine Learning', description: 'ML concepts and types', duration: 45, type: 'Video' },
      { title: 'Scikit-learn Basics', description: 'Using scikit-learn for ML', duration: 50, type: 'Interactive' },
      { title: 'Data Preprocessing', description: 'Scaling, encoding, and transformation', duration: 45, type: 'Practice' },
      { title: 'Regression Models', description: 'Linear and polynomial regression', duration: 60, type: 'Practice' },
      { title: 'Classification Models', description: 'Logistic regression and decision trees', duration: 60, type: 'Interactive' },
      { title: 'Ensemble Methods', description: 'Random forests and boosting', duration: 55, type: 'Practice' },
      { title: 'Model Evaluation', description: 'Metrics and cross-validation', duration: 50, type: 'Tutorial' },
      { title: 'Hyperparameter Tuning', description: 'Optimizing model parameters', duration: 45, type: 'Interactive' },
      { title: 'Introduction to Deep Learning', description: 'Neural networks basics', duration: 50, type: 'Video' },
      { title: 'Data Science Project', description: 'Complete end-to-end data analysis project', duration: 180, type: 'Project' }
    ]
  },
  {
    id: 6,
    title: 'Testing and Debugging',
    level: 'Intermediate',
    description: 'Master testing methodologies and debugging techniques in Python.',
    totalLessons: 20,
    completedLessons: 0,
    estimatedTime: 22,
    skills: [
      'Unit testing with pytest',
      'Test-driven development',
      'Debugging techniques',
      'Code coverage',
      'Mocking and fixtures',
      'Integration testing',
      'Performance testing',
      'Test automation'
    ],
    lessons: [
      { title: 'Introduction to Testing', description: 'Why testing matters and testing principles', duration: 20, type: 'Video' },
      { title: 'Testing Fundamentals', description: 'Test concepts and best practices', duration: 30, type: 'Tutorial' },
      { title: 'unittest Framework', description: 'Python built-in testing framework', duration: 35, type: 'Interactive' },
      { title: 'Writing Your First Test', description: 'Basic test structure and assertions', duration: 30, type: 'Interactive' },
      { title: 'Test Organization', description: 'Structuring test files and suites', duration: 35, type: 'Practice' },
      { title: 'pytest Framework', description: 'Setting up and using pytest', duration: 35, type: 'Practice' },
      { title: 'pytest Features', description: 'Fixtures, parametrization, and markers', duration: 45, type: 'Interactive' },
      { title: 'Test Fixtures', description: 'Reusable test setup and teardown', duration: 40, type: 'Interactive' },
      { title: 'Parametrized Tests', description: 'Testing multiple inputs efficiently', duration: 35, type: 'Practice' },
      { title: 'Mocking and Patching', description: 'Isolating code with mocks', duration: 45, type: 'Interactive' },
      { title: 'Test Doubles', description: 'Mocks, stubs, and fakes', duration: 40, type: 'Tutorial' },
      { title: 'Test Coverage', description: 'Measuring and improving test coverage', duration: 30, type: 'Tutorial' },
      { title: 'Coverage Tools', description: 'Using coverage.py and pytest-cov', duration: 35, type: 'Practice' },
      { title: 'Debugging Techniques', description: 'Using debugger and print statements', duration: 40, type: 'Practice' },
      { title: 'Python Debugger', description: 'pdb and advanced debugging', duration: 45, type: 'Interactive' },
      { title: 'Error Handling Tests', description: 'Testing exceptions and error cases', duration: 35, type: 'Interactive' },
      { title: 'Integration Testing', description: 'Testing complete workflows', duration: 45, type: 'Practice' },
      { title: 'Test-Driven Development', description: 'TDD workflow and practices', duration: 50, type: 'Interactive' },
      { title: 'Performance Testing', description: 'Testing application performance', duration: 40, type: 'Tutorial' },
      { title: 'Testing Project', description: 'Write comprehensive tests for an application', duration: 120, type: 'Project' }
    ]
  },
  {
    id: 7,
    title: 'File Handling and I/O',
    level: 'Beginner',
    description: 'Learn to read, write, and manipulate files in Python.',
    totalLessons: 18,
    completedLessons: 0,
    estimatedTime: 15,
    skills: [
      'Reading and writing files',
      'CSV and JSON handling',
      'File paths and directories',
      'Context managers',
      'Binary file operations',
      'Excel files',
      'PDF processing',
      'File compression'
    ],
    lessons: [
      { title: 'Introduction to File I/O', description: 'Understanding file operations', duration: 20, type: 'Video' },
      { title: 'File Modes', description: 'Understanding file open modes', duration: 25, type: 'Tutorial' },
      { title: 'Reading Text Files', description: 'Opening and reading file contents', duration: 30, type: 'Interactive' },
      { title: 'Reading Methods', description: 'read(), readline(), readlines()', duration: 35, type: 'Practice' },
      { title: 'Writing Text Files', description: 'Creating and writing to files', duration: 30, type: 'Practice' },
      { title: 'Appending to Files', description: 'Adding content to existing files', duration: 25, type: 'Interactive' },
      { title: 'Context Managers', description: 'Using with statements for file handling', duration: 25, type: 'Interactive' },
      { title: 'Custom Context Managers', description: 'Creating your own context managers', duration: 40, type: 'Practice' },
      { title: 'Working with CSV Files', description: 'Reading and writing CSV data', duration: 40, type: 'Practice' },
      { title: 'CSV Advanced', description: 'Custom delimiters and dialects', duration: 35, type: 'Interactive' },
      { title: 'JSON File Operations', description: 'Parsing and creating JSON files', duration: 35, type: 'Interactive' },
      { title: 'JSON Advanced', description: 'Custom serialization and encoding', duration: 40, type: 'Practice' },
      { title: 'File Paths and Directories', description: 'os.path and pathlib module', duration: 40, type: 'Practice' },
      { title: 'pathlib Module', description: 'Modern path handling with pathlib', duration: 45, type: 'Interactive' },
      { title: 'Directory Operations', description: 'Creating, listing, and removing directories', duration: 40, type: 'Practice' },
      { title: 'Binary Files', description: 'Working with binary data', duration: 35, type: 'Interactive' },
      { title: 'Excel Files', description: 'Reading and writing Excel with openpyxl', duration: 50, type: 'Interactive' },
      { title: 'File Compression', description: 'Working with zip and tar files', duration: 40, type: 'Practice' },
      { title: 'File Handling Project', description: 'Build a file processing application', duration: 90, type: 'Project' }
    ]
  },
  {
    id: 8,
    title: 'Regular Expressions',
    level: 'Intermediate',
    description: 'Master pattern matching and text processing with regex.',
    totalLessons: 18,
    completedLessons: 0,
    estimatedTime: 16,
    skills: [
      'Regex patterns and syntax',
      'Pattern matching',
      'Text search and replace',
      'Grouping and capturing',
      'Advanced regex techniques',
      'Regex optimization',
      'Real-world patterns',
      'Text processing'
    ],
    lessons: [
      { title: 'Introduction to Regex', description: 'What are regular expressions?', duration: 20, type: 'Video' },
      { title: 'Regex Module', description: 'Using re module in Python', duration: 25, type: 'Tutorial' },
      { title: 'Basic Patterns', description: 'Matching characters and sequences', duration: 35, type: 'Interactive' },
      { title: 'Character Classes', description: 'Matching sets of characters', duration: 30, type: 'Practice' },
      { title: 'Special Characters', description: 'Escaping and special sequences', duration: 35, type: 'Interactive' },
      { title: 'Quantifiers', description: 'Matching multiple occurrences', duration: 35, type: 'Interactive' },
      { title: 'Greedy vs Non-Greedy', description: 'Understanding quantifier behavior', duration: 30, type: 'Practice' },
      { title: 'Anchors and Boundaries', description: 'Start, end, and word boundaries', duration: 30, type: 'Practice' },
      { title: 'Groups and Capturing', description: 'Extracting matched groups', duration: 40, type: 'Interactive' },
      { title: 'Named Groups', description: 'Using named capture groups', duration: 35, type: 'Practice' },
      { title: 'Non-Capturing Groups', description: 'Grouping without capturing', duration: 30, type: 'Interactive' },
      { title: 'Lookahead and Lookbehind', description: 'Advanced pattern matching', duration: 45, type: 'Practice' },
      { title: 'Search and Replace', description: 'Finding and replacing text', duration: 35, type: 'Interactive' },
      { title: 'Regex Flags', description: 'Using flags for case sensitivity and more', duration: 30, type: 'Practice' },
      { title: 'Compiled Regex', description: 'Pre-compiling patterns for performance', duration: 35, type: 'Interactive' },
      { title: 'Common Regex Patterns', description: 'Email, phone, URL patterns', duration: 40, type: 'Tutorial' },
      { title: 'Regex Debugging', description: 'Testing and debugging regex patterns', duration: 35, type: 'Practice' },
      { title: 'Regex Project', description: 'Build a text processing tool with regex', duration: 90, type: 'Project' }
    ]
  },
  {
    id: 9,
    title: 'API Development',
    level: 'Advanced',
    description: 'Build RESTful APIs and work with external APIs in Python.',
    totalLessons: 22,
    completedLessons: 0,
    estimatedTime: 28,
    skills: [
      'REST API design',
      'Flask RESTful',
      'API authentication',
      'Request/response handling',
      'API documentation',
      'GraphQL APIs',
      'WebSocket APIs',
      'API testing'
    ],
    lessons: [
      { title: 'Introduction to APIs', description: 'What are APIs and REST principles', duration: 25, type: 'Video' },
      { title: 'REST Architecture', description: 'Understanding RESTful design', duration: 30, type: 'Tutorial' },
      { title: 'Building REST APIs with Flask', description: 'Creating API endpoints', duration: 45, type: 'Interactive' },
      { title: 'Flask-RESTful', description: 'Using Flask-RESTful extension', duration: 50, type: 'Practice' },
      { title: 'HTTP Methods', description: 'GET, POST, PUT, DELETE operations', duration: 40, type: 'Practice' },
      { title: 'Request Parsing', description: 'Handling JSON and form data', duration: 35, type: 'Interactive' },
      { title: 'Request Validation', description: 'Validating incoming requests', duration: 40, type: 'Practice' },
      { title: 'Response Formatting', description: 'JSON responses and status codes', duration: 30, type: 'Practice' },
      { title: 'Response Serialization', description: 'Custom serializers and formatting', duration: 45, type: 'Interactive' },
      { title: 'API Authentication', description: 'Token-based and OAuth authentication', duration: 50, type: 'Interactive' },
      { title: 'JWT Tokens', description: 'JSON Web Token implementation', duration: 45, type: 'Practice' },
      { title: 'API Authorization', description: 'Role-based access control', duration: 40, type: 'Interactive' },
      { title: 'Error Handling', description: 'Proper error responses and validation', duration: 40, type: 'Practice' },
      { title: 'API Versioning', description: 'Versioning strategies for APIs', duration: 35, type: 'Tutorial' },
      { title: 'Consuming External APIs', description: 'Using requests library', duration: 45, type: 'Interactive' },
      { title: 'Async API Calls', description: 'Making asynchronous API requests', duration: 40, type: 'Practice' },
      { title: 'API Rate Limiting', description: 'Implementing rate limits', duration: 40, type: 'Practice' },
      { title: 'Caching Strategies', description: 'API response caching', duration: 35, type: 'Interactive' },
      { title: 'API Documentation', description: 'Swagger/OpenAPI documentation', duration: 45, type: 'Tutorial' },
      { title: 'GraphQL Basics', description: 'Introduction to GraphQL APIs', duration: 50, type: 'Tutorial' },
      { title: 'WebSocket APIs', description: 'Real-time communication', duration: 55, type: 'Interactive' },
      { title: 'API Project', description: 'Build a complete REST API', duration: 150, type: 'Project' }
    ]
  },
  {
    id: 10,
    title: 'Database Programming',
    level: 'Intermediate',
    description: 'Learn to work with databases using SQLAlchemy and raw SQL.',
    totalLessons: 11,
    completedLessons: 0,
    estimatedTime: 12,
    skills: [
      'SQL basics',
      'SQLAlchemy ORM',
      'Database queries',
      'Relationships and joins',
      'Database migrations'
    ],
    lessons: [
      { title: 'Introduction to Databases', description: 'Database concepts and SQL basics', duration: 30, type: 'Video' },
      { title: 'SQL Basics', description: 'SELECT, INSERT, UPDATE, DELETE', duration: 40, type: 'Interactive' },
      { title: 'SQLAlchemy Setup', description: 'Connecting to databases', duration: 35, type: 'Practice' },
      { title: 'Defining Models', description: 'Creating database models', duration: 40, type: 'Interactive' },
      { title: 'Creating Tables', description: 'Schema creation and migrations', duration: 35, type: 'Practice' },
      { title: 'Querying Data', description: 'Filtering and querying records', duration: 45, type: 'Interactive' },
      { title: 'Relationships', description: 'One-to-many and many-to-many relationships', duration: 50, type: 'Practice' },
      { title: 'Joins and Aggregations', description: 'Complex queries and aggregations', duration: 45, type: 'Interactive' },
      { title: 'Transactions', description: 'Managing database transactions', duration: 40, type: 'Practice' },
      { title: 'Database Migrations', description: 'Alembic for schema changes', duration: 45, type: 'Tutorial' },
      { title: 'Database Project', description: 'Build an application with database', duration: 120, type: 'Project' }
    ]
  },
  {
    id: 11,
    title: 'Async Programming',
    level: 'Advanced',
    description: 'Master asynchronous programming with asyncio and async/await.',
    totalLessons: 20,
    completedLessons: 0,
    estimatedTime: 25,
    skills: [
      'Async/await syntax',
      'asyncio library',
      'Concurrent execution',
      'Async HTTP requests',
      'Event loops',
      'Async databases',
      'WebSockets',
      'Async testing'
    ],
    lessons: [
      { title: 'Introduction to Async', description: 'Why async programming?', duration: 25, type: 'Video' },
      { title: 'Concurrency vs Parallelism', description: 'Understanding the difference', duration: 30, type: 'Tutorial' },
      { title: 'Async/Await Basics', description: 'Understanding async functions', duration: 40, type: 'Interactive' },
      { title: 'Coroutines', description: 'Creating and using coroutines', duration: 35, type: 'Practice' },
      { title: 'Event Loops', description: 'How event loops work', duration: 35, type: 'Practice' },
      { title: 'Running Async Code', description: 'asyncio.run and coroutines', duration: 30, type: 'Interactive' },
      { title: 'Creating Tasks', description: 'asyncio.create_task()', duration: 35, type: 'Practice' },
      { title: 'Concurrent Tasks', description: 'Running multiple tasks concurrently', duration: 45, type: 'Practice' },
      { title: 'asyncio.gather()', description: 'Running tasks in parallel', duration: 40, type: 'Interactive' },
      { title: 'Async Context Managers', description: 'Async with statements', duration: 35, type: 'Interactive' },
      { title: 'Async Iterators', description: 'Creating async iterators', duration: 40, type: 'Practice' },
      { title: 'Async Generators', description: 'Creating async generators', duration: 40, type: 'Practice' },
      { title: 'Async HTTP Requests', description: 'aiohttp for async web requests', duration: 45, type: 'Interactive' },
      { title: 'Async Database Operations', description: 'Async database libraries', duration: 50, type: 'Practice' },
      { title: 'Async File I/O', description: 'Asynchronous file operations', duration: 40, type: 'Interactive' },
      { title: 'WebSockets', description: 'Real-time async communication', duration: 50, type: 'Practice' },
      { title: 'Error Handling', description: 'Handling errors in async code', duration: 35, type: 'Tutorial' },
      { title: 'Async Timeouts', description: 'Managing timeouts in async code', duration: 35, type: 'Interactive' },
      { title: 'Async Testing', description: 'Testing async code', duration: 40, type: 'Practice' },
      { title: 'Async Project', description: 'Build a high-performance async application', duration: 150, type: 'Project' }
    ]
  },
  {
    id: 12,
    title: 'Error Handling and Exceptions',
    level: 'Beginner',
    description: 'Learn to handle errors gracefully and write robust code.',
    totalLessons: 8,
    completedLessons: 0,
    estimatedTime: 5,
    skills: [
      'Exception handling',
      'Try/except blocks',
      'Custom exceptions',
      'Error logging',
      'Best practices'
    ],
    lessons: [
      { title: 'Introduction to Exceptions', description: 'What are exceptions?', duration: 15, type: 'Video' },
      { title: 'Try/Except Blocks', description: 'Catching and handling errors', duration: 30, type: 'Interactive' },
      { title: 'Multiple Exceptions', description: 'Handling different error types', duration: 35, type: 'Practice' },
      { title: 'Finally and Else', description: 'Cleanup and conditional execution', duration: 30, type: 'Interactive' },
      { title: 'Raising Exceptions', description: 'Creating and raising custom errors', duration: 35, type: 'Practice' },
      { title: 'Custom Exceptions', description: 'Defining your own exception classes', duration: 40, type: 'Interactive' },
      { title: 'Error Logging', description: 'Logging errors and debugging', duration: 35, type: 'Tutorial' },
      { title: 'Error Handling Project', description: 'Build robust error handling', duration: 60, type: 'Project' }
    ]
  },
  {
    id: 13,
    title: 'Python Best Practices',
    level: 'Intermediate',
    description: 'Learn Pythonic code, PEP 8, and professional development practices.',
    totalLessons: 10,
    completedLessons: 0,
    estimatedTime: 8,
    skills: [
      'PEP 8 style guide',
      'Code organization',
      'Documentation',
      'Code reviews',
      'Performance optimization'
    ],
    lessons: [
      { title: 'Pythonic Code', description: 'Writing idiomatic Python', duration: 25, type: 'Video' },
      { title: 'PEP 8 Style Guide', description: 'Code formatting standards', duration: 35, type: 'Tutorial' },
      { title: 'Code Organization', description: 'Structuring Python projects', duration: 40, type: 'Interactive' },
      { title: 'Documentation', description: 'Docstrings and comments', duration: 35, type: 'Practice' },
      { title: 'List Comprehensions', description: 'Efficient data transformations', duration: 30, type: 'Interactive' },
      { title: 'Generators', description: 'Memory-efficient iteration', duration: 40, type: 'Practice' },
      { title: 'Decorators', description: 'Function and class decorators', duration: 45, type: 'Interactive' },
      { title: 'Context Managers', description: 'Resource management patterns', duration: 35, type: 'Practice' },
      { title: 'Code Reviews', description: 'Reviewing and improving code', duration: 40, type: 'Tutorial' },
      { title: 'Best Practices Project', description: 'Refactor code following best practices', duration: 90, type: 'Project' }
    ]
  },
  {
    id: 14,
    title: 'Python Automation & Scripting',
    level: 'Intermediate',
    description: 'Automate tasks and build powerful scripts with Python.',
    totalLessons: 18,
    completedLessons: 0,
    estimatedTime: 20,
    skills: [
      'File operations',
      'System automation',
      'Web scraping',
      'API integration',
      'Task scheduling',
      'Email automation',
      'Data processing',
      'System administration'
    ],
    lessons: [
      { title: 'Introduction to Automation', description: 'Automation concepts and use cases', duration: 25, type: 'Video' },
      { title: 'File Operations', description: 'Reading, writing, and organizing files', duration: 40, type: 'Interactive' },
      { title: 'Directory Management', description: 'Working with directories and paths', duration: 35, type: 'Practice' },
      { title: 'CSV and JSON Processing', description: 'Processing structured data files', duration: 40, type: 'Interactive' },
      { title: 'Excel Automation', description: 'Working with Excel files', duration: 45, type: 'Practice' },
      { title: 'PDF Processing', description: 'Reading and creating PDFs', duration: 40, type: 'Interactive' },
      { title: 'Web Scraping Basics', description: 'Introduction to web scraping', duration: 45, type: 'Tutorial' },
      { title: 'BeautifulSoup', description: 'Parsing HTML with BeautifulSoup', duration: 50, type: 'Interactive' },
      { title: 'Selenium Basics', description: 'Automating web browsers', duration: 55, type: 'Practice' },
      { title: 'API Integration', description: 'Working with REST APIs', duration: 45, type: 'Interactive' },
      { title: 'HTTP Requests', description: 'Making API calls with requests', duration: 40, type: 'Practice' },
      { title: 'Email Automation', description: 'Sending and reading emails', duration: 45, type: 'Interactive' },
      { title: 'Task Scheduling', description: 'Automating recurring tasks', duration: 40, type: 'Tutorial' },
      { title: 'System Commands', description: 'Running system commands from Python', duration: 35, type: 'Interactive' },
      { title: 'Process Management', description: 'Managing system processes', duration: 40, type: 'Practice' },
      { title: 'Database Automation', description: 'Automating database tasks', duration: 45, type: 'Interactive' },
      { title: 'Error Handling in Scripts', description: 'Robust error handling', duration: 35, type: 'Tutorial' },
      { title: 'Automation Project', description: 'Build a comprehensive automation script', duration: 120, type: 'Project' }
    ]
  },
  {
    id: 15,
    title: 'Python for DevOps',
    level: 'Advanced',
    description: 'Use Python for infrastructure automation, CI/CD, and cloud operations.',
    totalLessons: 20,
    completedLessons: 0,
    estimatedTime: 30,
    skills: [
      'Infrastructure as Code',
      'CI/CD pipelines',
      'Cloud automation',
      'Container management',
      'Monitoring and logging',
      'Configuration management',
      'API development',
      'DevOps tools integration'
    ],
    lessons: [
      { title: 'Python in DevOps', description: 'Role of Python in DevOps', duration: 25, type: 'Video' },
      { title: 'Environment Setup', description: 'Setting up Python for DevOps', duration: 30, type: 'Tutorial' },
      { title: 'Configuration Management', description: 'Managing config files and secrets', duration: 40, type: 'Interactive' },
      { title: 'YAML and JSON Processing', description: 'Working with config formats', duration: 35, type: 'Practice' },
      { title: 'Environment Variables', description: 'Managing environment configuration', duration: 30, type: 'Interactive' },
      { title: 'Docker Integration', description: 'Working with Docker from Python', duration: 45, type: 'Practice' },
      { title: 'Container Management', description: 'Managing containers programmatically', duration: 50, type: 'Interactive' },
      { title: 'Kubernetes Basics', description: 'Kubernetes API and Python', duration: 55, type: 'Tutorial' },
      { title: 'CI/CD Pipelines', description: 'Building CI/CD with Python', duration: 50, type: 'Interactive' },
      { title: 'Git Operations', description: 'Automating Git workflows', duration: 40, type: 'Practice' },
      { title: 'AWS Automation', description: 'Automating AWS services', duration: 55, type: 'Interactive' },
      { title: 'Cloud APIs', description: 'Working with cloud provider APIs', duration: 50, type: 'Practice' },
      { title: 'Infrastructure as Code', description: 'Terraform and Python integration', duration: 45, type: 'Tutorial' },
      { title: 'Monitoring and Logging', description: 'Setting up monitoring systems', duration: 50, type: 'Interactive' },
      { title: 'Log Analysis', description: 'Processing and analyzing logs', duration: 45, type: 'Practice' },
      { title: 'Metrics Collection', description: 'Collecting system metrics', duration: 40, type: 'Interactive' },
      { title: 'Alerting Systems', description: 'Building alerting mechanisms', duration: 45, type: 'Practice' },
      { title: 'API Development', description: 'Building DevOps APIs', duration: 50, type: 'Interactive' },
      { title: 'Security Best Practices', description: 'Securing Python DevOps tools', duration: 45, type: 'Tutorial' },
      { title: 'DevOps Project', description: 'Complete DevOps automation project', duration: 180, type: 'Project' }
    ]
  },
  {
    id: 16,
    title: 'Python GUI Development',
    level: 'Intermediate',
    description: 'Build desktop applications with Tkinter, PyQt, and modern GUI frameworks.',
    totalLessons: 16,
    completedLessons: 0,
    estimatedTime: 20,
    skills: [
      'Tkinter basics',
      'PyQt/PySide',
      'Event handling',
      'Widget customization',
      'Layout management',
      'Modern GUI frameworks',
      'Desktop app deployment'
    ],
    lessons: [
      { title: 'Introduction to GUI', description: 'GUI programming concepts', duration: 20, type: 'Video' },
      { title: 'Tkinter Basics', description: 'Getting started with Tkinter', duration: 40, type: 'Interactive' },
      { title: 'Widgets and Layouts', description: 'Creating and organizing widgets', duration: 45, type: 'Practice' },
      { title: 'Event Handling', description: 'Responding to user events', duration: 40, type: 'Interactive' },
      { title: 'Dialogs and Menus', description: 'Creating dialogs and menu bars', duration: 45, type: 'Practice' },
      { title: 'Canvas and Graphics', description: 'Drawing and graphics in Tkinter', duration: 50, type: 'Interactive' },
      { title: 'Custom Widgets', description: 'Creating custom GUI components', duration: 45, type: 'Practice' },
      { title: 'PyQt Introduction', description: 'Introduction to PyQt/PySide', duration: 40, type: 'Tutorial' },
      { title: 'PyQt Widgets', description: 'Working with PyQt widgets', duration: 50, type: 'Interactive' },
      { title: 'PyQt Signals and Slots', description: 'Event-driven programming in PyQt', duration: 45, type: 'Practice' },
      { title: 'Modern GUI Frameworks', description: 'Kivy, Dear PyGui, and others', duration: 50, type: 'Tutorial' },
      { title: 'State Management', description: 'Managing application state', duration: 40, type: 'Interactive' },
      { title: 'Data Binding', description: 'Connecting data to UI', duration: 45, type: 'Practice' },
      { title: 'Styling and Themes', description: 'Customizing appearance', duration: 40, type: 'Interactive' },
      { title: 'Packaging GUI Apps', description: 'Distributing desktop applications', duration: 50, type: 'Tutorial' },
      { title: 'GUI Project', description: 'Build a complete desktop application', duration: 150, type: 'Project' }
    ]
  },
  {
    id: 17,
    title: 'Python Security',
    level: 'Advanced',
    description: 'Learn security best practices, cryptography, and secure coding in Python.',
    totalLessons: 14,
    completedLessons: 0,
    estimatedTime: 18,
    skills: [
      'Secure coding practices',
      'Cryptography',
      'Authentication and authorization',
      'Input validation',
      'Security vulnerabilities',
      'Penetration testing',
      'Secure APIs'
    ],
    lessons: [
      { title: 'Security Fundamentals', description: 'Introduction to Python security', duration: 25, type: 'Video' },
      { title: 'Common Vulnerabilities', description: 'OWASP Top 10 and Python-specific issues', duration: 40, type: 'Tutorial' },
      { title: 'Input Validation', description: 'Sanitizing and validating user input', duration: 45, type: 'Interactive' },
      { title: 'SQL Injection Prevention', description: 'Secure database queries', duration: 40, type: 'Practice' },
      { title: 'XSS Prevention', description: 'Cross-site scripting protection', duration: 35, type: 'Interactive' },
      { title: 'Cryptography Basics', description: 'Encryption and hashing', duration: 50, type: 'Tutorial' },
      { title: 'Hashing and Salting', description: 'Secure password storage', duration: 45, type: 'Practice' },
      { title: 'Symmetric Encryption', description: 'AES and symmetric ciphers', duration: 50, type: 'Interactive' },
      { title: 'Asymmetric Encryption', description: 'RSA and public key cryptography', duration: 55, type: 'Practice' },
      { title: 'Authentication Methods', description: 'Token-based and session auth', duration: 45, type: 'Interactive' },
      { title: 'Authorization Patterns', description: 'RBAC and permission systems', duration: 40, type: 'Practice' },
      { title: 'Secure APIs', description: 'API security best practices', duration: 50, type: 'Tutorial' },
      { title: 'Security Testing', description: 'Penetration testing and audits', duration: 45, type: 'Interactive' },
      { title: 'Security Project', description: 'Build a secure application', duration: 120, type: 'Project' }
    ]
  },
  {
    id: 18,
    title: 'Python Performance Optimization',
    level: 'Advanced',
    description: 'Optimize Python code for speed and efficiency using profiling and optimization techniques.',
    totalLessons: 15,
    completedLessons: 0,
    estimatedTime: 18,
    skills: [
      'Profiling and benchmarking',
      'Performance optimization',
      'Memory management',
      'Cython and Numba',
      'Parallel processing',
      'Caching strategies',
      'Algorithm optimization'
    ],
    lessons: [
      { title: 'Performance Basics', description: 'Understanding Python performance', duration: 25, type: 'Video' },
      { title: 'Profiling Tools', description: 'cProfile and line_profiler', duration: 40, type: 'Interactive' },
      { title: 'Benchmarking', description: 'Measuring code performance', duration: 35, type: 'Practice' },
      { title: 'Algorithm Optimization', description: 'Choosing efficient algorithms', duration: 45, type: 'Tutorial' },
      { title: 'Data Structure Optimization', description: 'Selecting optimal data structures', duration: 40, type: 'Interactive' },
      { title: 'Memory Management', description: 'Understanding Python memory', duration: 45, type: 'Tutorial' },
      { title: 'Memory Profiling', description: 'Identifying memory leaks', duration: 40, type: 'Practice' },
      { title: 'Caching Strategies', description: 'Memoization and caching', duration: 45, type: 'Interactive' },
      { title: 'List vs Generator', description: 'Memory-efficient iteration', duration: 35, type: 'Practice' },
      { title: 'NumPy Optimization', description: 'Vectorized operations', duration: 50, type: 'Interactive' },
      { title: 'Cython Introduction', description: 'Compiling Python to C', duration: 55, type: 'Tutorial' },
      { title: 'Numba JIT', description: 'Just-in-time compilation', duration: 50, type: 'Interactive' },
      { title: 'Parallel Processing', description: 'multiprocessing and threading', duration: 55, type: 'Practice' },
      { title: 'Async Performance', description: 'Optimizing async code', duration: 45, type: 'Interactive' },
      { title: 'Performance Project', description: 'Optimize a real-world application', duration: 120, type: 'Project' }
    ]
  },
  {
    id: 19,
    title: 'Python for Machine Learning',
    level: 'Advanced',
    description: 'Deep dive into machine learning with scikit-learn, TensorFlow, and PyTorch.',
    totalLessons: 15,
    completedLessons: 0,
    estimatedTime: 25,
    skills: [
      'Supervised learning',
      'Unsupervised learning',
      'Neural networks',
      'Deep learning',
      'Model deployment'
    ],
    lessons: [
      { title: 'ML Fundamentals Review', description: 'Recap of machine learning basics', duration: 30, type: 'Video' },
      { title: 'Feature Engineering', description: 'Creating and selecting features', duration: 50, type: 'Interactive' },
      { title: 'Model Selection', description: 'Choosing the right algorithm', duration: 45, type: 'Practice' },
      { title: 'Ensemble Methods', description: 'Random forests and gradient boosting', duration: 55, type: 'Interactive' },
      { title: 'Neural Networks Basics', description: 'Introduction to neural networks', duration: 60, type: 'Tutorial' },
      { title: 'TensorFlow Introduction', description: 'Getting started with TensorFlow', duration: 50, type: 'Interactive' },
      { title: 'Building Neural Networks', description: 'Creating models with TensorFlow', duration: 65, type: 'Practice' },
      { title: 'PyTorch Basics', description: 'Introduction to PyTorch', duration: 55, type: 'Interactive' },
      { title: 'Convolutional Neural Networks', description: 'CNNs for image processing', duration: 70, type: 'Tutorial' },
      { title: 'Recurrent Neural Networks', description: 'RNNs and LSTMs for sequences', duration: 65, type: 'Interactive' },
      { title: 'Transfer Learning', description: 'Using pre-trained models', duration: 60, type: 'Practice' },
      { title: 'Model Evaluation', description: 'Advanced evaluation metrics', duration: 50, type: 'Interactive' },
      { title: 'Model Deployment', description: 'Deploying ML models to production', duration: 70, type: 'Tutorial' },
      { title: 'MLOps Basics', description: 'ML operations and pipelines', duration: 55, type: 'Interactive' },
      { title: 'ML Project', description: 'Build and deploy a complete ML system', duration: 180, type: 'Project' }
    ]
  },
  {
    id: 20,
    title: 'Python Package Development',
    level: 'Intermediate',
    description: 'Create, publish, and maintain Python packages and libraries.',
    totalLessons: 11,
    completedLessons: 0,
    estimatedTime: 14,
    skills: [
      'Package structure',
      'Setup.py and pyproject.toml',
      'Publishing to PyPI',
      'Documentation',
      'Version management'
    ],
    lessons: [
      { title: 'Package Structure', description: 'Organizing Python packages', duration: 30, type: 'Video' },
      { title: 'Setup Configuration', description: 'setup.py and setup.cfg', duration: 40, type: 'Interactive' },
      { title: 'Modern Packaging', description: 'pyproject.toml and build systems', duration: 45, type: 'Practice' },
      { title: 'Package Metadata', description: 'Version, dependencies, and info', duration: 35, type: 'Interactive' },
      { title: 'Entry Points', description: 'Creating command-line tools', duration: 40, type: 'Practice' },
      { title: 'Documentation', description: 'Sphinx and docstrings', duration: 50, type: 'Tutorial' },
      { title: 'Testing Packages', description: 'Testing your package', duration: 40, type: 'Interactive' },
      { title: 'Version Management', description: 'Semantic versioning', duration: 30, type: 'Practice' },
      { title: 'Publishing to PyPI', description: 'Uploading your package', duration: 45, type: 'Tutorial' },
      { title: 'Package Maintenance', description: 'Updates and bug fixes', duration: 35, type: 'Interactive' },
      { title: 'Package Project', description: 'Create and publish your own package', duration: 120, type: 'Project' }
    ]
  },
  {
    id: 21,
    title: 'Python Networking',
    level: 'Intermediate',
    description: 'Network programming, sockets, HTTP clients, and server development.',
    totalLessons: 12,
    completedLessons: 0,
    estimatedTime: 16,
    skills: [
      'Socket programming',
      'HTTP clients and servers',
      'WebSockets',
      'Network protocols',
      'Async networking'
    ],
    lessons: [
      { title: 'Networking Basics', description: 'TCP/IP and network protocols', duration: 30, type: 'Video' },
      { title: 'Socket Programming', description: 'Creating sockets in Python', duration: 45, type: 'Interactive' },
      { title: 'TCP Sockets', description: 'Reliable connection-oriented sockets', duration: 50, type: 'Practice' },
      { title: 'UDP Sockets', description: 'Connectionless sockets', duration: 40, type: 'Interactive' },
      { title: 'HTTP Clients', description: 'requests library and urllib', duration: 45, type: 'Practice' },
      { title: 'HTTP Servers', description: 'Building HTTP servers', duration: 50, type: 'Interactive' },
      { title: 'WebSockets', description: 'Real-time bidirectional communication', duration: 55, type: 'Tutorial' },
      { title: 'RESTful Clients', description: 'Consuming REST APIs', duration: 40, type: 'Practice' },
      { title: 'Async Networking', description: 'asyncio for network operations', duration: 50, type: 'Interactive' },
      { title: 'Network Security', description: 'SSL/TLS and secure connections', duration: 45, type: 'Tutorial' },
      { title: 'Network Protocols', description: 'FTP, SMTP, and other protocols', duration: 50, type: 'Practice' },
      { title: 'Networking Project', description: 'Build a network application', duration: 120, type: 'Project' }
    ]
  },
  {
    id: 22,
    title: 'Python for Game Development',
    level: 'Intermediate',
    description: 'Create games using Pygame and other Python game development libraries.',
    totalLessons: 13,
    completedLessons: 0,
    estimatedTime: 18,
    skills: [
      'Pygame basics',
      'Game loops',
      'Sprite management',
      'Collision detection',
      'Game physics'
    ],
    lessons: [
      { title: 'Game Development Intro', description: 'Python for game development', duration: 25, type: 'Video' },
      { title: 'Pygame Setup', description: 'Installing and setting up Pygame', duration: 30, type: 'Tutorial' },
      { title: 'Game Window', description: 'Creating the game window', duration: 35, type: 'Interactive' },
      { title: 'Game Loop', description: 'Main game loop structure', duration: 40, type: 'Practice' },
      { title: 'Sprites', description: 'Creating and managing sprites', duration: 45, type: 'Interactive' },
      { title: 'Input Handling', description: 'Keyboard and mouse input', duration: 40, type: 'Practice' },
      { title: 'Collision Detection', description: 'Detecting sprite collisions', duration: 50, type: 'Interactive' },
      { title: 'Game Physics', description: 'Movement and gravity', duration: 45, type: 'Practice' },
      { title: 'Sound and Music', description: 'Adding audio to games', duration: 40, type: 'Interactive' },
      { title: 'Game States', description: 'Menus, pause, and game over', duration: 45, type: 'Practice' },
      { title: 'Tile Maps', description: 'Creating game levels', duration: 50, type: 'Tutorial' },
      { title: 'Animation', description: 'Sprite animation techniques', duration: 45, type: 'Interactive' },
      { title: 'Game Project', description: 'Build a complete game', duration: 150, type: 'Project' }
    ]
  },
  {
    id: 23,
    title: 'Python for Scientific Computing',
    level: 'Advanced',
    description: 'Scientific computing with NumPy, SciPy, SymPy, and specialized libraries.',
    totalLessons: 14,
    completedLessons: 0,
    estimatedTime: 22,
    skills: [
      'Numerical computing',
      'Scientific libraries',
      'Mathematical modeling',
      'Simulation',
      'Scientific visualization'
    ],
    lessons: [
      { title: 'Scientific Computing Overview', description: 'Python in scientific computing', duration: 30, type: 'Video' },
      { title: 'NumPy Advanced', description: 'Advanced NumPy operations', duration: 50, type: 'Interactive' },
      { title: 'SciPy Basics', description: 'Scientific computing with SciPy', duration: 45, type: 'Practice' },
      { title: 'Linear Algebra', description: 'Matrix operations and linear systems', duration: 55, type: 'Interactive' },
      { title: 'Optimization', description: 'Numerical optimization methods', duration: 50, type: 'Practice' },
      { title: 'Integration', description: 'Numerical integration techniques', duration: 45, type: 'Interactive' },
      { title: 'Differential Equations', description: 'Solving ODEs and PDEs', duration: 60, type: 'Tutorial' },
      { title: 'SymPy', description: 'Symbolic mathematics', duration: 55, type: 'Interactive' },
      { title: 'Statistical Computing', description: 'Statistical analysis with SciPy', duration: 50, type: 'Practice' },
      { title: 'Signal Processing', description: 'Signal analysis and filtering', duration: 55, type: 'Interactive' },
      { title: 'Image Processing', description: 'Scientific image analysis', duration: 50, type: 'Practice' },
      { title: 'Simulation', description: 'Monte Carlo and other simulations', duration: 60, type: 'Tutorial' },
      { title: 'Scientific Visualization', description: 'Advanced plotting techniques', duration: 45, type: 'Interactive' },
      { title: 'Scientific Computing Project', description: 'Complete scientific computing project', duration: 180, type: 'Project' }
    ]
  },
  {
    id: 24,
    title: 'Python for Blockchain',
    level: 'Advanced',
    description: 'Build blockchain applications and smart contracts with Python.',
    totalLessons: 12,
    completedLessons: 0,
    estimatedTime: 20,
    skills: [
      'Blockchain fundamentals',
      'Cryptography',
      'Smart contracts',
      'Blockchain APIs',
      'Decentralized applications'
    ],
    lessons: [
      { title: 'Blockchain Basics', description: 'Understanding blockchain technology', duration: 40, type: 'Video' },
      { title: 'Cryptography for Blockchain', description: 'Hashing and digital signatures', duration: 50, type: 'Tutorial' },
      { title: 'Building a Blockchain', description: 'Creating a simple blockchain', duration: 60, type: 'Interactive' },
      { title: 'Proof of Work', description: 'Implementing consensus mechanisms', duration: 55, type: 'Practice' },
      { title: 'Transactions', description: 'Creating and validating transactions', duration: 50, type: 'Interactive' },
      { title: 'Wallets', description: 'Creating cryptocurrency wallets', duration: 60, type: 'Practice' },
      { title: 'Smart Contracts', description: 'Introduction to smart contracts', duration: 65, type: 'Tutorial' },
      { title: 'Web3.py', description: 'Interacting with Ethereum', duration: 70, type: 'Interactive' },
      { title: 'Deploying Smart Contracts', description: 'Deploying contracts to blockchain', duration: 65, type: 'Practice' },
      { title: 'Blockchain APIs', description: 'Using blockchain APIs', duration: 55, type: 'Interactive' },
      { title: 'DApps Development', description: 'Building decentralized applications', duration: 70, type: 'Tutorial' },
      { title: 'Blockchain Project', description: 'Build a complete blockchain application', duration: 180, type: 'Project' }
    ]
  },
  {
    id: 24,
    title: 'Python for Finance',
    level: 'Advanced',
    description: 'Financial data analysis, algorithmic trading, and quantitative finance with Python.',
    totalLessons: 20,
    completedLessons: 0,
    estimatedTime: 30,
    skills: [
      'Financial data analysis',
      'Stock market data',
      'Algorithmic trading',
      'Risk analysis',
      'Portfolio optimization',
      'Time series analysis',
      'Financial modeling'
    ],
    lessons: [
      { title: 'Python in Finance', description: 'Introduction to financial programming', duration: 25, type: 'Video' },
      { title: 'Financial Data Sources', description: 'APIs and data providers', duration: 35, type: 'Tutorial' },
      { title: 'Stock Data Retrieval', description: 'Fetching stock market data', duration: 45, type: 'Interactive' },
      { title: 'Pandas for Finance', description: 'Financial data manipulation', duration: 50, type: 'Practice' },
      { title: 'Time Series Analysis', description: 'Analyzing financial time series', duration: 55, type: 'Interactive' },
      { title: 'Technical Indicators', description: 'Moving averages, RSI, MACD', duration: 60, type: 'Practice' },
      { title: 'Candlestick Charts', description: 'Visualizing price data', duration: 45, type: 'Interactive' },
      { title: 'Portfolio Analysis', description: 'Analyzing investment portfolios', duration: 50, type: 'Practice' },
      { title: 'Risk Metrics', description: 'Calculating risk measures', duration: 55, type: 'Interactive' },
      { title: 'Portfolio Optimization', description: 'Modern portfolio theory', duration: 60, type: 'Practice' },
      { title: 'Backtesting', description: 'Testing trading strategies', duration: 65, type: 'Interactive' },
      { title: 'Algorithmic Trading', description: 'Automated trading systems', duration: 70, type: 'Practice' },
      { title: 'Options Pricing', description: 'Black-Scholes model', duration: 60, type: 'Tutorial' },
      { title: 'Monte Carlo Simulation', description: 'Financial simulations', duration: 55, type: 'Interactive' },
      { title: 'Cryptocurrency Analysis', description: 'Analyzing crypto markets', duration: 50, type: 'Practice' },
      { title: 'Financial APIs', description: 'Integrating with broker APIs', duration: 60, type: 'Interactive' },
      { title: 'Risk Management', description: 'Implementing risk controls', duration: 55, type: 'Practice' },
      { title: 'Regulatory Compliance', description: 'Financial regulations', duration: 45, type: 'Tutorial' },
      { title: 'Real-time Data', description: 'Streaming financial data', duration: 50, type: 'Interactive' },
      { title: 'Finance Project', description: 'Build a trading analysis system', duration: 180, type: 'Project' }
    ]
  },
  {
    id: 25,
    title: 'Python Image Processing',
    level: 'Intermediate',
    description: 'Process, manipulate, and analyze images using PIL, OpenCV, and scikit-image.',
    totalLessons: 18,
    completedLessons: 0,
    estimatedTime: 22,
    skills: [
      'Image manipulation',
      'OpenCV basics',
      'Image filtering',
      'Feature detection',
      'Image recognition',
      'Computer vision',
      'Image enhancement'
    ],
    lessons: [
      { title: 'Image Processing Intro', description: 'Introduction to image processing', duration: 25, type: 'Video' },
      { title: 'PIL/Pillow Basics', description: 'Working with PIL library', duration: 40, type: 'Interactive' },
      { title: 'Image Loading', description: 'Loading and saving images', duration: 35, type: 'Practice' },
      { title: 'Image Manipulation', description: 'Resizing, cropping, rotating', duration: 45, type: 'Interactive' },
      { title: 'Image Filters', description: 'Applying filters and effects', duration: 50, type: 'Practice' },
      { title: 'OpenCV Introduction', description: 'Getting started with OpenCV', duration: 40, type: 'Tutorial' },
      { title: 'OpenCV Basics', description: 'Image operations in OpenCV', duration: 45, type: 'Interactive' },
      { title: 'Color Spaces', description: 'RGB, HSV, grayscale conversion', duration: 40, type: 'Practice' },
      { title: 'Image Thresholding', description: 'Binary and adaptive thresholding', duration: 45, type: 'Interactive' },
      { title: 'Edge Detection', description: 'Canny and Sobel edge detection', duration: 50, type: 'Practice' },
      { title: 'Feature Detection', description: 'Detecting corners and features', duration: 55, type: 'Interactive' },
      { title: 'Image Segmentation', description: 'Segmenting images', duration: 50, type: 'Practice' },
      { title: 'Object Detection', description: 'Detecting objects in images', duration: 60, type: 'Interactive' },
      { title: 'Face Recognition', description: 'Face detection and recognition', duration: 55, type: 'Practice' },
      { title: 'Image Enhancement', description: 'Improving image quality', duration: 45, type: 'Interactive' },
      { title: 'OCR with Python', description: 'Optical character recognition', duration: 50, type: 'Practice' },
      { title: 'Video Processing', description: 'Processing video files', duration: 55, type: 'Interactive' },
      { title: 'Image Processing Project', description: 'Build an image processing application', duration: 150, type: 'Project' }
    ]
  },
  {
    id: 26,
    title: 'Python Microservices',
    level: 'Advanced',
    description: 'Build scalable microservices architecture with Python, Docker, and Kubernetes.',
    totalLessons: 22,
    completedLessons: 0,
    estimatedTime: 35,
    skills: [
      'Microservices architecture',
      'Service communication',
      'API gateways',
      'Containerization',
      'Service discovery',
      'Distributed systems',
      'Message queues'
    ],
    lessons: [
      { title: 'Microservices Intro', description: 'Microservices architecture', duration: 30, type: 'Video' },
      { title: 'Monolith vs Microservices', description: 'When to use microservices', duration: 35, type: 'Tutorial' },
      { title: 'Service Design', description: 'Designing microservices', duration: 40, type: 'Interactive' },
      { title: 'RESTful Services', description: 'Building REST microservices', duration: 50, type: 'Practice' },
      { title: 'Service Communication', description: 'Inter-service communication', duration: 45, type: 'Interactive' },
      { title: 'API Gateway', description: 'Implementing API gateway', duration: 55, type: 'Practice' },
      { title: 'Message Queues', description: 'RabbitMQ and message brokers', duration: 60, type: 'Interactive' },
      { title: 'Event-Driven Architecture', description: 'Event-based communication', duration: 55, type: 'Practice' },
      { title: 'Service Discovery', description: 'Service registration and discovery', duration: 50, type: 'Interactive' },
      { title: 'Docker Basics', description: 'Containerizing services', duration: 45, type: 'Tutorial' },
      { title: 'Docker Compose', description: 'Orchestrating containers', duration: 50, type: 'Practice' },
      { title: 'Kubernetes Intro', description: 'Container orchestration', duration: 55, type: 'Tutorial' },
      { title: 'Kubernetes Deployments', description: 'Deploying to Kubernetes', duration: 60, type: 'Interactive' },
      { title: 'Service Mesh', description: 'Istio and service mesh', duration: 65, type: 'Tutorial' },
      { title: 'Load Balancing', description: 'Distributing traffic', duration: 50, type: 'Practice' },
      { title: 'Circuit Breaker', description: 'Fault tolerance patterns', duration: 45, type: 'Interactive' },
      { title: 'Distributed Tracing', description: 'Monitoring microservices', duration: 55, type: 'Practice' },
      { title: 'Service Monitoring', description: 'Health checks and metrics', duration: 50, type: 'Interactive' },
      { title: 'Database per Service', description: 'Data management patterns', duration: 55, type: 'Tutorial' },
      { title: 'Security in Microservices', description: 'Securing distributed systems', duration: 60, type: 'Practice' },
      { title: 'Testing Microservices', description: 'Testing distributed systems', duration: 55, type: 'Interactive' },
      { title: 'Microservices Project', description: 'Build a microservices system', duration: 200, type: 'Project' }
    ]
  },
  {
    id: 27,
    title: 'Python Natural Language Processing',
    level: 'Advanced',
    description: 'Process, analyze, and understand human language with NLP libraries and techniques.',
    totalLessons: 20,
    completedLessons: 0,
    estimatedTime: 30,
    skills: [
      'Text preprocessing',
      'Tokenization',
      'Sentiment analysis',
      'Named entity recognition',
      'Text classification',
      'Language models',
      'Chatbots'
    ],
    lessons: [
      { title: 'NLP Introduction', description: 'Introduction to natural language processing', duration: 30, type: 'Video' },
      { title: 'Text Preprocessing', description: 'Cleaning and normalizing text', duration: 45, type: 'Interactive' },
      { title: 'Tokenization', description: 'Splitting text into tokens', duration: 40, type: 'Practice' },
      { title: 'Stop Words', description: 'Removing stop words', duration: 35, type: 'Interactive' },
      { title: 'Stemming and Lemmatization', description: 'Reducing words to root forms', duration: 45, type: 'Practice' },
      { title: 'N-grams', description: 'Creating word sequences', duration: 40, type: 'Interactive' },
      { title: 'TF-IDF', description: 'Term frequency-inverse document frequency', duration: 50, type: 'Practice' },
      { title: 'Word Embeddings', description: 'Word2Vec and GloVe', duration: 55, type: 'Interactive' },
      { title: 'Sentiment Analysis', description: 'Analyzing text sentiment', duration: 50, type: 'Practice' },
      { title: 'Named Entity Recognition', description: 'Identifying entities in text', duration: 55, type: 'Interactive' },
      { title: 'Text Classification', description: 'Classifying text documents', duration: 60, type: 'Practice' },
      { title: 'spaCy Library', description: 'Advanced NLP with spaCy', duration: 55, type: 'Interactive' },
      { title: 'NLTK Basics', description: 'Natural Language Toolkit', duration: 50, type: 'Tutorial' },
      { title: 'Language Models', description: 'Introduction to language models', duration: 60, type: 'Tutorial' },
      { title: 'Transformers', description: 'Transformer architecture', duration: 65, type: 'Interactive' },
      { title: 'BERT and GPT', description: 'Pre-trained language models', duration: 70, type: 'Practice' },
      { title: 'Text Generation', description: 'Generating text with models', duration: 65, type: 'Interactive' },
      { title: 'Chatbots', description: 'Building conversational agents', duration: 70, type: 'Practice' },
      { title: 'Translation', description: 'Machine translation', duration: 60, type: 'Interactive' },
      { title: 'NLP Project', description: 'Build a complete NLP application', duration: 180, type: 'Project' }
    ]
  },
  {
    id: 28,
    title: 'Python IoT Development',
    level: 'Advanced',
    description: 'Build Internet of Things applications with Python, Raspberry Pi, and sensors.',
    totalLessons: 18,
    completedLessons: 0,
    estimatedTime: 25,
    skills: [
      'Raspberry Pi programming',
      'Sensor integration',
      'GPIO control',
      'IoT protocols',
      'Data collection',
      'Remote monitoring',
      'Edge computing'
    ],
    lessons: [
      { title: 'IoT Introduction', description: 'Introduction to Internet of Things', duration: 30, type: 'Video' },
      { title: 'Raspberry Pi Setup', description: 'Setting up Raspberry Pi', duration: 40, type: 'Tutorial' },
      { title: 'Python on Raspberry Pi', description: 'Running Python on embedded systems', duration: 35, type: 'Interactive' },
      { title: 'GPIO Basics', description: 'General Purpose Input/Output', duration: 45, type: 'Practice' },
      { title: 'GPIO Control', description: 'Controlling GPIO pins', duration: 50, type: 'Interactive' },
      { title: 'Sensors Introduction', description: 'Working with sensors', duration: 40, type: 'Tutorial' },
      { title: 'Temperature Sensors', description: 'Reading temperature data', duration: 45, type: 'Practice' },
      { title: 'Motion Sensors', description: 'Detecting motion', duration: 40, type: 'Interactive' },
      { title: 'Light Sensors', description: 'Measuring light levels', duration: 35, type: 'Practice' },
      { title: 'IoT Protocols', description: 'MQTT and CoAP', duration: 50, type: 'Tutorial' },
      { title: 'MQTT Communication', description: 'Publishing and subscribing', duration: 55, type: 'Interactive' },
      { title: 'Data Collection', description: 'Collecting sensor data', duration: 50, type: 'Practice' },
      { title: 'Data Storage', description: 'Storing IoT data', duration: 45, type: 'Interactive' },
      { title: 'Remote Monitoring', description: 'Monitoring devices remotely', duration: 55, type: 'Practice' },
      { title: 'Web Dashboard', description: 'Creating IoT dashboards', duration: 60, type: 'Interactive' },
      { title: 'Edge Computing', description: 'Processing at the edge', duration: 55, type: 'Tutorial' },
      { title: 'Security in IoT', description: 'Securing IoT devices', duration: 50, type: 'Practice' },
      { title: 'IoT Project', description: 'Build a complete IoT system', duration: 180, type: 'Project' }
    ]
  }
]

const navigateToLesson = (lesson: any) => {
  // Close modal first
  selectedPath.value = null
  
  // Navigate based on lesson type
  if (lesson.type === 'Practice' || lesson.type === 'Interactive' || lesson.type === 'Project') {
    router.push('/compiler')
  } else if (lesson.type === 'Video' || lesson.type === 'Tutorial') {
    router.push('/materials')
  } else {
    // Default to compiler for any other type
    router.push('/compiler')
  }
}

const startPath = (path: any) => {
  // Navigate to the first lesson or compiler
  if (path.lessons && path.lessons.length > 0) {
    const firstLesson = path.lessons[0]
    navigateToLesson(firstLesson)
  } else {
    // If no lessons, navigate to compiler
    router.push('/compiler')
  }
}

// World map helper functions
const getNodePosition = (index: number, total: number) => {
  const percentage = (index / (total - 1)) * 100
  // Add slight vertical variation to make it look more organic
  const verticalOffset = index % 2 === 0 ? 0 : 5
  return {
    left: `${percentage}%`,
    top: `${50 + verticalOffset}%`,
    transform: 'translate(-50%, -50%)'
  }
}

const getPathD = (index: number, total: number) => {
  // #region agent log
  console.log('[DEBUG] getPathD entry', { index, total, timestamp: Date.now() });
  // #endregion
  
  // Use viewBox coordinates (0-100) - NO PERCENTAGE SIGNS
  // Ensure we have valid numbers
  if (!total || total <= 1 || index < 0 || index >= total - 1) {
    console.warn('[DEBUG] getPathD invalid params', { index, total });
    return ''
  }
  
  // Calculate positions in viewBox coordinate system (0-100)
  const startX = (index / (total - 1)) * 100
  const endX = ((index + 1) / (total - 1)) * 100
  const midY = 50
  
  // Validate numbers are finite
  if (!Number.isFinite(startX) || !Number.isFinite(endX) || !Number.isFinite(midY)) {
    console.error('[DEBUG] getPathD invalid coordinates', { startX, endX, midY, index, total });
    return ''
  }
  
  // Create a wavy/curved path like a world map journey
  // Alternate between upward and downward curves for visual interest
  const curveDirection = index % 2 === 0 ? -15 : 15
  const controlX = (startX + endX) / 2
  const controlY = midY + curveDirection
  
  // Ensure all values are valid numbers
  if (!Number.isFinite(controlX) || !Number.isFinite(controlY)) {
    console.error('[DEBUG] getPathD invalid control points', { controlX, controlY, startX, endX });
    return ''
  }
  
  // Format path with proper number formatting - ABSOLUTELY NO % SIGNS
  // Use simple number format (SVG will handle decimals)
  const pathD = `M ${startX} ${midY} Q ${controlX} ${controlY} ${endX} ${midY}`
  
  // #region agent log
  const hasPercent = pathD.includes('%');
  console.log('[DEBUG] getPathD exit', { 
    pathD, 
    startX, 
    endX, 
    midY, 
    controlX, 
    controlY, 
    hasPercent,
    pathLength: pathD.length,
    timestamp: Date.now()
  });
  if (hasPercent) {
    console.error('[DEBUG] ERROR: Path still contains % sign!', pathD);
  }
  // #endregion
  
  return pathD
}

const isLessonUnlocked = (index: number) => {
  // First lesson is always unlocked, others unlock sequentially
  // For MVP, all lessons are unlocked (can be changed later)
  return true
}

const isLessonCompleted = (index: number) => {
  // For MVP, no lessons are completed (can be changed later)
  return false
}

const selectLesson = (lesson: any, path: any) => {
  selectedLesson.value = lesson
  selectedPath.value = path
  // Navigate to the lesson
  navigateToLesson(lesson)
}
</script>

<style scoped>
/* World Path Container */
.world-path-container {
  position: relative;
  min-height: 200px;
  padding: 40px 0;
  background: linear-gradient(180deg, rgba(26, 49, 43, 0.3) 0%, rgba(42, 63, 53, 0.2) 100%);
  border-radius: 12px;
  overflow: visible;
}

/* Path Animation */
.path-animation {
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  animation: drawPath 2s ease-in-out forwards;
}

@keyframes drawPath {
  to {
    stroke-dashoffset: 0;
  }
}

/* Lesson Node Container */
.lesson-node-container {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  z-index: 10;
}

/* Lesson Node */
.lesson-node {
  position: relative;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  border: 3px solid;
  background: var(--msit-dark-800);
}

.lesson-unlocked {
  border-color: #83E65B;
  background: linear-gradient(135deg, rgba(131, 230, 91, 0.2) 0%, rgba(131, 230, 91, 0.1) 100%);
  box-shadow: 0 4px 12px rgba(131, 230, 91, 0.3);
}

.lesson-unlocked:hover {
  transform: scale(1.15);
  box-shadow: 0 6px 20px rgba(131, 230, 91, 0.5);
  border-color: #83E65B;
}

.lesson-locked {
  border-color: rgba(131, 230, 91, 0.3);
  background: rgba(42, 63, 53, 0.5);
  opacity: 0.6;
  cursor: not-allowed;
}

.lesson-selected {
  transform: scale(1.2);
  box-shadow: 0 8px 24px rgba(131, 230, 91, 0.6);
  border-width: 4px;
}

/* Node Icon */
.node-icon {
  color: #83E65B;
  z-index: 2;
}

.lesson-locked .node-icon {
  color: rgba(131, 230, 91, 0.5);
}

/* Node Number */
.node-number {
  position: absolute;
  bottom: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #83E65B;
  color: #1a3127;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  font-family: 'Inter', sans-serif;
  border: 2px solid var(--msit-dark-800);
  z-index: 3;
}

.lesson-locked .node-number {
  background: rgba(131, 230, 91, 0.3);
  color: rgba(131, 230, 91, 0.7);
}

/* Node Checkmark */
.node-checkmark {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #83E65B;
  color: #1a3127;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 4;
  border: 2px solid var(--msit-dark-800);
}

/* Node Tooltip */
.node-tooltip {
  position: absolute;
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(26, 49, 43, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(131, 230, 91, 0.3);
  border-radius: 8px;
  padding: 8px 12px;
  min-width: 150px;
  max-width: 200px;
  text-align: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
  z-index: 20;
  white-space: normal;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.lesson-node-container:hover .node-tooltip {
  opacity: 1;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .lesson-node {
    width: 48px;
    height: 48px;
  }
  
  .node-icon {
    width: 20px;
    height: 20px;
  }
  
  .node-number {
    width: 20px;
    height: 20px;
    font-size: 10px;
    bottom: -6px;
    right: -6px;
  }
  
  .node-tooltip {
    top: 60px;
    min-width: 120px;
    padding: 6px 10px;
    font-size: 11px;
  }
}
</style>
