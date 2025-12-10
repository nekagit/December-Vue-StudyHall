<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Learning Paths</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Structured learning paths to master Python step by step</p>
    </div>

    <!-- Learning Paths Grid -->
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
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
              class="flex items-start p-4 bg-msit-dark-900 rounded-lg border border-msit-dark-700"
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
            Start Learning Path
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedPath = ref<any>(null)

const learningPaths = [
  {
    id: 1,
    title: 'Python Basics',
    level: 'Beginner',
    description: 'Learn the fundamentals of Python programming from scratch.',
    totalLessons: 12,
    completedLessons: 0,
    estimatedTime: 8,
    skills: [
      'Variables and data types',
      'Basic operations and expressions',
      'Control flow (if/else, loops)',
      'Functions and modules',
      'Working with strings and lists'
    ],
    lessons: [
      { title: 'Introduction to Python', description: 'What is Python and why learn it?', duration: 15, type: 'Video' },
      { title: 'Setting Up Python', description: 'Install Python and choose an IDE', duration: 20, type: 'Tutorial' },
      { title: 'Variables and Data Types', description: 'Learn about integers, floats, strings, and booleans', duration: 30, type: 'Interactive' },
      { title: 'Basic Operations', description: 'Arithmetic, comparison, and logical operators', duration: 25, type: 'Practice' },
      { title: 'Strings', description: 'String manipulation and formatting', duration: 35, type: 'Interactive' },
      { title: 'Lists and Tuples', description: 'Working with collections', duration: 40, type: 'Practice' },
      { title: 'Dictionaries', description: 'Key-value pairs and data structures', duration: 35, type: 'Interactive' },
      { title: 'Conditional Statements', description: 'if, elif, else statements', duration: 30, type: 'Practice' },
      { title: 'Loops', description: 'for and while loops', duration: 40, type: 'Interactive' },
      { title: 'Functions', description: 'Defining and calling functions', duration: 45, type: 'Practice' },
      { title: 'Modules and Packages', description: 'Importing and using libraries', duration: 30, type: 'Tutorial' },
      { title: 'Final Project', description: 'Build a simple Python application', duration: 60, type: 'Project' }
    ]
  },
  {
    id: 2,
    title: 'Object-Oriented Programming',
    level: 'Intermediate',
    description: 'Master classes, objects, inheritance, and polymorphism in Python.',
    totalLessons: 10,
    completedLessons: 0,
    estimatedTime: 12,
    skills: [
      'Classes and objects',
      'Inheritance and polymorphism',
      'Encapsulation',
      'Special methods',
      'Design patterns'
    ],
    lessons: [
      { title: 'Introduction to OOP', description: 'Concepts of object-oriented programming', duration: 20, type: 'Video' },
      { title: 'Classes and Objects', description: 'Creating your first class', duration: 35, type: 'Interactive' },
      { title: 'Attributes and Methods', description: 'Instance and class attributes', duration: 40, type: 'Practice' },
      { title: 'Constructors', description: '__init__ and object initialization', duration: 30, type: 'Interactive' },
      { title: 'Inheritance', description: 'Extending classes', duration: 45, type: 'Practice' },
      { title: 'Polymorphism', description: 'Method overriding and duck typing', duration: 40, type: 'Interactive' },
      { title: 'Encapsulation', description: 'Private attributes and properties', duration: 35, type: 'Practice' },
      { title: 'Special Methods', description: '__str__, __repr__, and more', duration: 40, type: 'Interactive' },
      { title: 'Design Patterns', description: 'Common OOP design patterns', duration: 50, type: 'Tutorial' },
      { title: 'OOP Project', description: 'Build an OOP-based application', duration: 90, type: 'Project' }
    ]
  },
  {
    id: 3,
    title: 'Data Structures & Algorithms',
    level: 'Intermediate',
    description: 'Learn essential data structures and algorithms for problem-solving.',
    totalLessons: 15,
    completedLessons: 0,
    estimatedTime: 20,
    skills: [
      'Arrays and linked lists',
      'Stacks and queues',
      'Trees and graphs',
      'Sorting algorithms',
      'Search algorithms'
    ],
    lessons: [
      { title: 'Introduction to Algorithms', description: 'What are algorithms and why they matter', duration: 25, type: 'Video' },
      { title: 'Time Complexity', description: 'Big O notation and algorithm analysis', duration: 35, type: 'Tutorial' },
      { title: 'Arrays and Lists', description: 'Working with arrays', duration: 30, type: 'Practice' },
      { title: 'Linked Lists', description: 'Implementing linked lists', duration: 45, type: 'Interactive' },
      { title: 'Stacks', description: 'LIFO data structure', duration: 35, type: 'Practice' },
      { title: 'Queues', description: 'FIFO data structure', duration: 35, type: 'Interactive' },
      { title: 'Trees', description: 'Binary trees and tree traversal', duration: 50, type: 'Practice' },
      { title: 'Graphs', description: 'Graph representation and algorithms', duration: 55, type: 'Interactive' },
      { title: 'Sorting Algorithms', description: 'Bubble, merge, quick sort', duration: 60, type: 'Practice' },
      { title: 'Search Algorithms', description: 'Linear and binary search', duration: 40, type: 'Interactive' },
      { title: 'Hash Tables', description: 'Dictionaries and hash maps', duration: 45, type: 'Practice' },
      { title: 'Recursion', description: 'Recursive thinking and problems', duration: 50, type: 'Interactive' },
      { title: 'Dynamic Programming', description: 'Memoization and DP patterns', duration: 60, type: 'Tutorial' },
      { title: 'Greedy Algorithms', description: 'Greedy problem-solving strategies', duration: 45, type: 'Practice' },
      { title: 'Algorithm Project', description: 'Solve complex algorithmic problems', duration: 120, type: 'Project' }
    ]
  },
  {
    id: 4,
    title: 'Web Development with Python',
    level: 'Advanced',
    description: 'Build web applications using Flask and Django frameworks.',
    totalLessons: 14,
    completedLessons: 0,
    estimatedTime: 25,
    skills: [
      'Flask framework',
      'Django framework',
      'REST APIs',
      'Database integration',
      'Deployment'
    ],
    lessons: [
      { title: 'Introduction to Web Development', description: 'HTTP, servers, and web architecture', duration: 30, type: 'Video' },
      { title: 'Flask Basics', description: 'Setting up your first Flask app', duration: 40, type: 'Interactive' },
      { title: 'Routing and Views', description: 'URL routing and view functions', duration: 35, type: 'Practice' },
      { title: 'Templates', description: 'Jinja2 templating engine', duration: 45, type: 'Interactive' },
      { title: 'Forms and Validation', description: 'Handling user input', duration: 40, type: 'Practice' },
      { title: 'Database Integration', description: 'SQLAlchemy and database models', duration: 60, type: 'Interactive' },
      { title: 'REST APIs', description: 'Building RESTful APIs', duration: 50, type: 'Practice' },
      { title: 'Authentication', description: 'User authentication and sessions', duration: 55, type: 'Interactive' },
      { title: 'Introduction to Django', description: 'Django framework overview', duration: 45, type: 'Video' },
      { title: 'Django Models', description: 'Database models in Django', duration: 50, type: 'Practice' },
      { title: 'Django Views', description: 'Function and class-based views', duration: 45, type: 'Interactive' },
      { title: 'Django Templates', description: 'Template system and inheritance', duration: 40, type: 'Practice' },
      { title: 'Deployment', description: 'Deploying Python web apps', duration: 60, type: 'Tutorial' },
      { title: 'Web Development Project', description: 'Build a full-stack web application', duration: 180, type: 'Project' }
    ]
  },
  {
    id: 5,
    title: 'Python for Data Science',
    level: 'Advanced',
    description: 'Learn data analysis, visualization, and machine learning with Python.',
    totalLessons: 16,
    completedLessons: 0,
    estimatedTime: 30,
    skills: [
      'NumPy and Pandas',
      'Data visualization',
      'Statistical analysis',
      'Machine learning basics',
      'Data cleaning and preprocessing'
    ],
    lessons: [
      { title: 'Introduction to Data Science', description: 'Overview of data science workflow', duration: 25, type: 'Video' },
      { title: 'NumPy Fundamentals', description: 'Working with arrays and numerical operations', duration: 45, type: 'Interactive' },
      { title: 'Pandas Basics', description: 'DataFrames and Series operations', duration: 50, type: 'Practice' },
      { title: 'Data Loading', description: 'Reading CSV, JSON, and Excel files', duration: 40, type: 'Interactive' },
      { title: 'Data Cleaning', description: 'Handling missing values and outliers', duration: 55, type: 'Practice' },
      { title: 'Data Transformation', description: 'Filtering, grouping, and aggregating data', duration: 50, type: 'Interactive' },
      { title: 'Matplotlib Basics', description: 'Creating basic plots and charts', duration: 45, type: 'Practice' },
      { title: 'Seaborn Visualization', description: 'Statistical data visualization', duration: 50, type: 'Interactive' },
      { title: 'Statistical Analysis', description: 'Descriptive statistics and distributions', duration: 55, type: 'Tutorial' },
      { title: 'Correlation Analysis', description: 'Understanding relationships in data', duration: 40, type: 'Practice' },
      { title: 'Introduction to Machine Learning', description: 'ML concepts and types', duration: 45, type: 'Video' },
      { title: 'Scikit-learn Basics', description: 'Using scikit-learn for ML', duration: 50, type: 'Interactive' },
      { title: 'Regression Models', description: 'Linear and polynomial regression', duration: 60, type: 'Practice' },
      { title: 'Classification Models', description: 'Logistic regression and decision trees', duration: 60, type: 'Interactive' },
      { title: 'Model Evaluation', description: 'Metrics and cross-validation', duration: 50, type: 'Tutorial' },
      { title: 'Data Science Project', description: 'Complete end-to-end data analysis project', duration: 180, type: 'Project' }
    ]
  }
]

const startPath = (path: any) => {
  // Show path details modal
  selectedPath.value = path
  // You can navigate to first lesson or materials related to this path
  // For now, we show the modal with all lessons
}
</script>
