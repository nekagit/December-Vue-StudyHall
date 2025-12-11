#!/usr/bin/env python3
"""Initialize database with sample data."""
from backend.database import SessionLocal, engine, Base
from backend.models import Material, Problem

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Define all materials to add
    materials = [
            # Python Basics
            Material(
                title="Python Basics",
                content="# Python Basics\n\nWelcome to Python! Python is a high-level, interpreted programming language known for its simplicity and readability.\n\n## Key Features\n- Simple and readable syntax\n- Dynamically typed\n- Interpreted language\n- Extensive standard library\n\n## Getting Started\n```python\nprint('Hello, World!')\n```\n\nPython is perfect for beginners and experts alike.",
                category="Python",
                order_index=1
            ),
            Material(
                title="Python Functions",
                content="# Python Functions\n\nFunctions are reusable blocks of code that perform specific tasks.\n\n## Defining Functions\n```python\ndef greet(name):\n    return f'Hello, {name}!'\n```\n\n## Function Parameters\n- Positional arguments\n- Keyword arguments\n- Default values\n- *args and **kwargs\n\n## Best Practices\n- Use descriptive names\n- Keep functions focused on one task\n- Document with docstrings",
                category="Python",
                order_index=2
            ),
            Material(
                title="Python Classes and Objects",
                content="# Python Classes and Objects\n\nObject-oriented programming in Python allows you to create reusable code structures.\n\n## Defining Classes\n```python\nclass Dog:\n    def __init__(self, name, breed):\n        self.name = name\n        self.breed = breed\n    \n    def bark(self):\n        return f'{self.name} says woof!'\n```\n\n## Key Concepts\n- Classes and instances\n- Inheritance\n- Encapsulation\n- Polymorphism\n- Special methods (__init__, __str__, etc.)",
                category="Python",
                order_index=3
            ),
            Material(
                title="Data Structures",
                content="# Data Structures\n\nPython provides several built-in data structures for organizing and storing data.\n\n## Lists\n```python\nfruits = ['apple', 'banana', 'orange']\nfruits.append('grape')\n```\n\n## Dictionaries\n```python\nperson = {'name': 'John', 'age': 30}\nperson['city'] = 'New York'\n```\n\n## Tuples\n- Immutable sequences\n- Perfect for fixed data\n\n## Sets\n- Unique elements only\n- Useful for membership testing\n\n## Choosing the Right Structure\n- Lists: ordered, mutable sequences\n- Dictionaries: key-value pairs\n- Tuples: immutable sequences\n- Sets: unique unordered collections",
                category="Python",
                order_index=4
            ),
            Material(
                title="Python Modules and Packages",
                content="# Python Modules and Packages\n\nOrganize your code into reusable modules and packages.\n\n## Creating Modules\n```python\n# math_utils.py\ndef add(a, b):\n    return a + b\n\ndef multiply(a, b):\n    return a * b\n```\n\n## Importing Modules\n```python\nimport math_utils\nfrom math_utils import add\n```\n\n## Packages\n- Directory with __init__.py\n- Organize related modules\n- Create namespace hierarchy\n\n## Standard Library\nPython comes with extensive standard library modules for common tasks.",
                category="Python",
                order_index=5
            ),
            Material(
                title="Error Handling in Python",
                content="# Error Handling in Python\n\nHandle errors gracefully with try-except blocks.\n\n## Basic Error Handling\n```python\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero!')\n```\n\n## Exception Types\n- Built-in exceptions (ValueError, TypeError, etc.)\n- Custom exceptions\n- Exception hierarchy\n\n## Best Practices\n- Be specific with exception types\n- Don't catch all exceptions blindly\n- Use finally for cleanup\n- Raise meaningful exceptions",
                category="Python",
                order_index=6
            ),
            
            # Web Development
            Material(
                title="Web Development Intro",
                content="# Web Development Intro\n\nIntroduction to building web applications.\n\n## Core Technologies\n- **HTML**: Structure and content\n- **CSS**: Styling and layout\n- **JavaScript**: Interactivity and behavior\n\n## Frontend vs Backend\n- Frontend: What users see and interact with\n- Backend: Server-side logic and data management\n\n## Modern Web Development\n- Frameworks and libraries\n- Responsive design\n- API integration\n- Single Page Applications (SPAs)",
                category="Web Dev",
                order_index=10
            ),
            Material(
                title="Vue.js Fundamentals",
                content="# Vue.js Fundamentals\n\nVue.js is a progressive JavaScript framework for building user interfaces.\n\n## Key Concepts\n- **Reactive Data**: Data changes automatically update the UI\n- **Components**: Reusable, self-contained UI pieces\n- **Directives**: Special attributes (v-if, v-for, v-bind)\n- **Composition API**: Modern way to organize component logic\n\n## Basic Example\n```vue\n<template>\n  <div>{{ message }}</div>\n</template>\n\n<script setup>\nimport { ref } from 'vue'\nconst message = ref('Hello Vue!')\n</script>\n```\n\n## Why Vue?\n- Easy to learn\n- Flexible and scalable\n- Great developer experience\n- Excellent documentation",
                category="Web Dev",
                order_index=11
            ),
            Material(
                title="RESTful APIs",
                content="# RESTful APIs\n\nREST (Representational State Transfer) is an architectural style for designing web services.\n\n## HTTP Methods\n- **GET**: Retrieve data\n- **POST**: Create new resources\n- **PUT**: Update existing resources\n- **DELETE**: Remove resources\n\n## API Design Principles\n- Use nouns for endpoints (/users, /materials)\n- Use HTTP status codes appropriately\n- Return JSON data\n- Version your API\n\n## Example Endpoints\n```\nGET    /api/materials      # List all materials\nGET    /api/materials/1    # Get specific material\nPOST   /api/materials      # Create material\nPUT    /api/materials/1    # Update material\nDELETE /api/materials/1    # Delete material\n```\n\n## Best Practices\n- Consistent naming conventions\n- Proper error handling\n- Authentication and authorization\n- Rate limiting",
                category="Web Dev",
                order_index=12
            ),
            Material(
                title="Flask API Development",
                content="# Flask API Development\n\nFlask is a lightweight Python web framework perfect for building APIs.\n\n## Basic Flask App\n```python\nfrom flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.route('/api/hello')\ndef hello():\n    return jsonify({'message': 'Hello, World!'})\n```\n\n## Key Features\n- Minimal and flexible\n- Easy routing\n- Built-in development server\n- Extensive extensions ecosystem\n\n## Common Patterns\n- Blueprints for organizing routes\n- SQLAlchemy for database\n- Flask-CORS for cross-origin requests\n- Error handling middleware\n\n## Best Practices\n- Use environment variables for configuration\n- Implement proper error handling\n- Add request validation\n- Use database migrations",
                category="Web Dev",
                order_index=13
            ),
            Material(
                title="TypeScript Basics",
                content="# TypeScript Basics\n\nTypeScript adds static type checking to JavaScript.\n\n## Why TypeScript?\n- Catch errors at compile time\n- Better IDE support\n- Improved code documentation\n- Easier refactoring\n\n## Basic Types\n```typescript\nlet name: string = 'John'\nlet age: number = 30\nlet isActive: boolean = true\n```\n\n## Interfaces\n```typescript\ninterface User {\n  name: string\n  age: number\n  email?: string  // Optional\n}\n```\n\n## Type Inference\nTypeScript can often infer types automatically.\n\n## Benefits\n- Type safety\n- Better tooling\n- Self-documenting code\n- Easier maintenance",
                category="Web Dev",
                order_index=14
            ),
            
            # Algorithms & Data Structures
            Material(
                title="Algorithm Complexity",
                content="# Algorithm Complexity\n\nUnderstanding time and space complexity helps write efficient code.\n\n## Big O Notation\n- **O(1)**: Constant time\n- **O(log n)**: Logarithmic time\n- **O(n)**: Linear time\n- **O(n log n)**: Linearithmic time\n- **O(n²)**: Quadratic time\n\n## Examples\n```python\n# O(1) - Constant\ndef get_first(items):\n    return items[0]\n\n# O(n) - Linear\nfor item in items:\n    print(item)\n\n# O(n²) - Quadratic\nfor i in items:\n    for j in items:\n        print(i, j)\n```\n\n## Space Complexity\nMeasures memory usage relative to input size.\n\n## Best Practices\n- Analyze before optimizing\n- Choose appropriate data structures\n- Consider trade-offs",
                category="Algorithms",
                order_index=20
            ),
            Material(
                title="Sorting Algorithms",
                content="# Sorting Algorithms\n\nLearn different approaches to sorting data.\n\n## Common Algorithms\n- **Bubble Sort**: Simple but slow (O(n²))\n- **Quick Sort**: Fast average case (O(n log n))\n- **Merge Sort**: Consistent performance (O(n log n))\n- **Insertion Sort**: Good for small datasets\n\n## Quick Sort Example\n```python\ndef quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)\n```\n\n## When to Use Which?\n- Small arrays: Insertion sort\n- General purpose: Quick sort or merge sort\n- Nearly sorted: Insertion sort\n- Stability matters: Merge sort",
                category="Algorithms",
                order_index=21
            ),
            Material(
                title="Search Algorithms",
                content="# Search Algorithms\n\nEfficiently find data in collections.\n\n## Linear Search\n- Check each element sequentially\n- Time: O(n)\n- Works on unsorted data\n\n## Binary Search\n- Divide and conquer approach\n- Time: O(log n)\n- Requires sorted data\n\n## Binary Search Example\n```python\ndef binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n```\n\n## Hash Tables\n- O(1) average case lookup\n- Requires hash function\n- Handle collisions",
                category="Algorithms",
                order_index=22
            ),
            
            # Best Practices
            Material(
                title="Code Style and PEP 8",
                content="# Code Style and PEP 8\n\nPython's style guide helps write readable, consistent code.\n\n## Key Guidelines\n- Use 4 spaces for indentation\n- Limit lines to 79 characters\n- Use descriptive variable names\n- Follow naming conventions\n\n## Naming Conventions\n- **Functions**: snake_case (get_user_name)\n- **Classes**: PascalCase (UserAccount)\n- **Constants**: UPPER_SNAKE_CASE (MAX_SIZE)\n- **Private**: Leading underscore (_internal)\n\n## Import Organization\n```python\n# Standard library\nimport os\nimport sys\n\n# Third-party\nimport flask\nimport sqlalchemy\n\n# Local\nfrom backend.models import User\n```\n\n## Tools\n- **black**: Code formatter\n- **flake8**: Linter\n- **pylint**: Advanced linting\n- **mypy**: Type checking",
                category="Best Practices",
                order_index=30
            ),
            Material(
                title="Git Workflow",
                content="# Git Workflow\n\nVersion control is essential for collaborative development.\n\n## Basic Commands\n```bash\ngit init              # Initialize repository\ngit add .             # Stage changes\ngit commit -m 'msg'   # Commit changes\ngit push              # Push to remote\ngit pull              # Pull from remote\n```\n\n## Branching Strategy\n- **main/master**: Production-ready code\n- **develop**: Integration branch\n- **feature/**: New features\n- **bugfix/**: Bug fixes\n\n## Best Practices\n- Commit often with meaningful messages\n- Write clear commit messages\n- Use branches for features\n- Review code before merging\n- Keep commits focused\n\n## Commit Message Format\n```\nShort summary (50 chars)\n\nDetailed explanation if needed\n- Bullet points\n- More details\n```",
                category="Best Practices",
                order_index=31
            ),
            Material(
                title="Testing Fundamentals",
                content="# Testing Fundamentals\n\nWriting tests ensures your code works correctly.\n\n## Types of Tests\n- **Unit Tests**: Test individual functions\n- **Integration Tests**: Test component interactions\n- **End-to-End Tests**: Test full workflows\n\n## Python Testing with pytest\n```python\ndef test_add_numbers():\n    assert add(2, 3) == 5\n\ndef test_add_negative():\n    assert add(-1, 1) == 0\n```\n\n## Test Structure\n- Arrange: Set up test data\n- Act: Execute the code\n- Assert: Verify results\n\n## Best Practices\n- Write tests before or alongside code\n- Test edge cases\n- Keep tests independent\n- Use descriptive test names\n- Aim for good coverage\n\n## Benefits\n- Catch bugs early\n- Enable refactoring\n- Document expected behavior\n- Increase confidence",
                category="Best Practices",
                order_index=32
            ),
            
            # Database
            Material(
                title="SQL Basics",
                content="# SQL Basics\n\nStructured Query Language for managing relational databases.\n\n## Core Commands\n- **SELECT**: Retrieve data\n- **INSERT**: Add new records\n- **UPDATE**: Modify existing records\n- **DELETE**: Remove records\n\n## SELECT Examples\n```sql\nSELECT * FROM users;\nSELECT name, email FROM users WHERE age > 18;\nSELECT COUNT(*) FROM orders;\n```\n\n## JOINs\n- **INNER JOIN**: Matching records only\n- **LEFT JOIN**: All left table records\n- **RIGHT JOIN**: All right table records\n- **FULL JOIN**: All records from both\n\n## Best Practices\n- Use indexes for performance\n- Normalize database design\n- Use transactions\n- Parameterize queries (prevent SQL injection)",
                category="Database",
                order_index=40
            ),
            Material(
                title="SQLAlchemy ORM",
                content="# SQLAlchemy ORM\n\nPython's SQL toolkit and Object-Relational Mapping library.\n\n## Defining Models\n```python\nfrom sqlalchemy import Column, Integer, String\nfrom sqlalchemy.ext.declarative import declarative_base\n\nBase = declarative_base()\n\nclass User(Base):\n    __tablename__ = 'users'\n    id = Column(Integer, primary_key=True)\n    name = Column(String(50))\n    email = Column(String(100))\n```\n\n## Querying\n```python\n# Get all users\nusers = session.query(User).all()\n\n# Filter\nuser = session.query(User).filter_by(email='test@example.com').first()\n\n# Add new record\nnew_user = User(name='John', email='john@example.com')\nsession.add(new_user)\nsession.commit()\n```\n\n## Relationships\n- One-to-many\n- Many-to-many\n- Foreign keys\n\n## Benefits\n- Pythonic API\n- Database agnostic\n- Automatic query building\n- Migration support",
                category="Database",
                order_index=41
            ),
    ]
    
    # Check existing materials
    existing_count = db.query(Material).count()
    existing_titles = {m.title for m in db.query(Material.title).all()}
    
    # Only add materials if database is empty, or add new ones that don't exist
    if existing_count == 0:
        for material in materials:
            db.add(material)
        print(f"Created {len(materials)} sample materials")
    else:
        # Add only new materials that don't already exist
        new_materials = [m for m in materials if m.title not in existing_titles]
        if new_materials:
            for material in new_materials:
                db.add(material)
            print(f"Added {len(new_materials)} new materials (skipped {len(materials) - len(new_materials)} duplicates)")
        else:
            print(f"All {len(materials)} materials already exist in database")
    
    db.commit()
    print("Database initialized successfully!")
    
    # Add coding problems
    problems = [
        Problem(
            title="Sum of Two Numbers",
            description="Write a function that takes two numbers and returns their sum.",
            full_description="Create a function called `add_numbers` that takes two parameters `a` and `b` and returns their sum.\n\nExample:\n- add_numbers(5, 3) should return 8\n- add_numbers(-1, 1) should return 0",
            difficulty="beginner",
            tags=["Basics", "Math"],
            points=10,
            estimated_time=5,
            examples=[{"input": "add_numbers(5, 3)", "output": "8"}, {"input": "add_numbers(-1, 1)", "output": "0"}],
            constraints=["Both inputs are integers", "Result should be an integer"],
            test_cases=[
                {"input": "add_numbers(5, 3)", "output": "8"},
                {"input": "add_numbers(-1, 1)", "output": "0"},
                {"input": "add_numbers(10, -5)", "output": "5"},
                {"input": "add_numbers(0, 0)", "output": "0"},
                {"input": "add_numbers(100, 200)", "output": "300"}
            ],
            starter_code="def add_numbers(a, b):\n    # Your code here\n    pass",
            category="Basics",
            order_index=1
        ),
        Problem(
            title="Find Maximum in List",
            description="Find the maximum value in a list without using the built-in max() function.",
            full_description="Write a function `find_max` that takes a list of numbers and returns the maximum value. Do not use Python's built-in `max()` function.\n\nExample:\n- find_max([1, 5, 3, 9, 2]) should return 9\n- find_max([-5, -2, -10]) should return -2",
            difficulty="beginner",
            tags=["Lists", "Loops"],
            points=15,
            estimated_time=10,
            examples=[{"input": "find_max([1, 5, 3, 9, 2])", "output": "9"}, {"input": "find_max([-5, -2, -10])", "output": "-2"}],
            constraints=["List contains at least one element", "All elements are numbers"],
            test_cases=[
                {"input": "find_max([1, 5, 3, 9, 2])", "output": "9"},
                {"input": "find_max([-5, -2, -10])", "output": "-2"},
                {"input": "find_max([42])", "output": "42"},
                {"input": "find_max([1, 1, 1])", "output": "1"},
                {"input": "find_max([-1, -5, -3])", "output": "-1"}
            ],
            starter_code="def find_max(numbers):\n    # Your code here\n    pass",
            category="Lists",
            order_index=2
        ),
        Problem(
            title="Reverse a String",
            description="Reverse a string without using the built-in reverse() method.",
            full_description="Write a function `reverse_string` that takes a string and returns it reversed. Do not use Python's built-in string reversal methods.\n\nExample:\n- reverse_string(\"hello\") should return \"olleh\"\n- reverse_string(\"Python\") should return \"nohtyP\"",
            difficulty="beginner",
            tags=["Strings", "Algorithms"],
            points=15,
            estimated_time=10,
            examples=[{"input": "reverse_string(\"hello\")", "output": "\"olleh\""}, {"input": "reverse_string(\"Python\")", "output": "\"nohtyP\""}],
            constraints=["Input is a non-empty string"],
            test_cases=[
                {"input": "reverse_string(\"hello\")", "output": "\"olleh\""},
                {"input": "reverse_string(\"Python\")", "output": "\"nohtyP\""},
                {"input": "reverse_string(\"a\")", "output": "\"a\""},
                {"input": "reverse_string(\"123\")", "output": "\"321\""},
                {"input": "reverse_string(\"racecar\")", "output": "\"racecar\""}
            ],
            starter_code="def reverse_string(s):\n    # Your code here\n    pass",
            category="Strings",
            order_index=3
        ),
        Problem(
            title="Count Vowels",
            description="Count the number of vowels in a given string.",
            full_description="Write a function `count_vowels` that takes a string and returns the count of vowels (a, e, i, o, u). The function should be case-insensitive.\n\nExample:\n- count_vowels(\"Hello\") should return 2\n- count_vowels(\"Python Programming\") should return 5",
            difficulty="beginner",
            tags=["Strings", "Loops"],
            points=20,
            estimated_time=15,
            examples=[{"input": "count_vowels(\"Hello\")", "output": "2"}, {"input": "count_vowels(\"Python Programming\")", "output": "5"}],
            constraints=["Input is a string", "Case-insensitive matching"],
            test_cases=[
                {"input": "count_vowels(\"Hello\")", "output": "2"},
                {"input": "count_vowels(\"Python Programming\")", "output": "5"},
                {"input": "count_vowels(\"AEIOU\")", "output": "5"},
                {"input": "count_vowels(\"xyz\")", "output": "0"},
                {"input": "count_vowels(\"a\")", "output": "1"}
            ],
            starter_code="def count_vowels(s):\n    # Your code here\n    pass",
            category="Strings",
            order_index=4
        ),
        Problem(
            title="Check Palindrome",
            description="Check if a string is a palindrome (reads the same forwards and backwards).",
            full_description="Write a function `is_palindrome` that takes a string and returns True if it is a palindrome, False otherwise. Ignore case and non-alphanumeric characters.\n\nExample:\n- is_palindrome(\"racecar\") should return True\n- is_palindrome(\"Hello\") should return False\n- is_palindrome(\"A man a plan a canal Panama\") should return True",
            difficulty="intermediate",
            tags=["Strings", "Algorithms"],
            points=25,
            estimated_time=20,
            examples=[{"input": "is_palindrome(\"racecar\")", "output": "True"}, {"input": "is_palindrome(\"Hello\")", "output": "False"}],
            constraints=["Ignore case", "Ignore spaces and punctuation"],
            test_cases=[
                {"input": "is_palindrome(\"racecar\")", "output": "True"},
                {"input": "is_palindrome(\"Hello\")", "output": "False"},
                {"input": "is_palindrome(\"a\")", "output": "True"},
                {"input": "is_palindrome(\"madam\")", "output": "True"},
                {"input": "is_palindrome(\"python\")", "output": "False"}
            ],
            starter_code="def is_palindrome(s):\n    # Your code here\n    pass",
            category="Algorithms",
            order_index=5
        ),
        Problem(
            title="Fibonacci Sequence",
            description="Generate the first n numbers in the Fibonacci sequence.",
            full_description="Write a function `fibonacci` that takes an integer n and returns a list containing the first n Fibonacci numbers. The Fibonacci sequence starts with 0 and 1, and each subsequent number is the sum of the two preceding ones.\n\nExample:\n- fibonacci(5) should return [0, 1, 1, 2, 3]\n- fibonacci(10) should return [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]",
            difficulty="intermediate",
            tags=["Recursion", "Algorithms"],
            points=30,
            estimated_time=25,
            examples=[{"input": "fibonacci(5)", "output": "[0, 1, 1, 2, 3]"}, {"input": "fibonacci(10)", "output": "[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]"}],
            constraints=["n is a positive integer", "n >= 1"],
            test_cases=[
                {"input": "fibonacci(5)", "output": "[0, 1, 1, 2, 3]"},
                {"input": "fibonacci(10)", "output": "[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]"},
                {"input": "fibonacci(1)", "output": "[0]"},
                {"input": "fibonacci(2)", "output": "[0, 1]"},
                {"input": "fibonacci(7)", "output": "[0, 1, 1, 2, 3, 5, 8]"}
            ],
            starter_code="def fibonacci(n):\n    # Your code here\n    pass",
            category="Algorithms",
            order_index=6
        ),
        Problem(
            title="Two Sum",
            description="Find two numbers in an array that add up to a target value.",
            full_description="Write a function `two_sum` that takes a list of integers and a target integer. Return the indices of the two numbers that add up to the target. You may assume that each input has exactly one solution.\n\nExample:\n- two_sum([2, 7, 11, 15], 9) should return [0, 1] (because 2 + 7 = 9)\n- two_sum([3, 2, 4], 6) should return [1, 2]",
            difficulty="intermediate",
            tags=["Arrays", "Algorithms"],
            points=35,
            estimated_time=30,
            examples=[{"input": "two_sum([2, 7, 11, 15], 9)", "output": "[0, 1]"}, {"input": "two_sum([3, 2, 4], 6)", "output": "[1, 2]"}],
            constraints=["Each input has exactly one solution", "Cannot use the same element twice"],
            test_cases=[
                {"input": "two_sum([2, 7, 11, 15], 9)", "output": "[0, 1]"},
                {"input": "two_sum([3, 2, 4], 6)", "output": "[1, 2]"},
                {"input": "two_sum([3, 3], 6)", "output": "[0, 1]"},
                {"input": "two_sum([1, 2, 3, 4], 5)", "output": "[1, 2]"}
            ],
            starter_code="def two_sum(nums, target):\n    # Your code here\n    pass",
            category="Algorithms",
            order_index=7
        ),
        Problem(
            title="Anagram Checker",
            description="Check if two strings are anagrams of each other.",
            full_description="Write a function `are_anagrams` that takes two strings and returns True if they are anagrams (contain the same characters in different order), False otherwise. The function should be case-insensitive.\n\nExample:\n- are_anagrams(\"listen\", \"silent\") should return True\n- are_anagrams(\"hello\", \"world\") should return False",
            difficulty="intermediate",
            tags=["Strings", "Algorithms"],
            points=30,
            estimated_time=20,
            examples=[{"input": "are_anagrams(\"listen\", \"silent\")", "output": "True"}, {"input": "are_anagrams(\"hello\", \"world\")", "output": "False"}],
            constraints=["Case-insensitive", "Ignore spaces"],
            test_cases=[
                {"input": "are_anagrams(\"listen\", \"silent\")", "output": "True"},
                {"input": "are_anagrams(\"hello\", \"world\")", "output": "False"},
                {"input": "are_anagrams(\"a\", \"a\")", "output": "True"},
                {"input": "are_anagrams(\"python\", \"typhon\")", "output": "True"},
                {"input": "are_anagrams(\"test\", \"best\")", "output": "False"}
            ],
            starter_code="def are_anagrams(s1, s2):\n    # Your code here\n    pass",
            category="Strings",
            order_index=8
        ),
        Problem(
            title="Merge Sorted Lists",
            description="Merge two sorted lists into one sorted list.",
            full_description="Write a function `merge_sorted` that takes two sorted lists and returns a new sorted list containing all elements from both lists.\n\nExample:\n- merge_sorted([1, 3, 5], [2, 4, 6]) should return [1, 2, 3, 4, 5, 6]\n- merge_sorted([1, 2], [3, 4]) should return [1, 2, 3, 4]",
            difficulty="advanced",
            tags=["Lists", "Algorithms"],
            points=40,
            estimated_time=35,
            examples=[{"input": "merge_sorted([1, 3, 5], [2, 4, 6])", "output": "[1, 2, 3, 4, 5, 6]"}, {"input": "merge_sorted([1, 2], [3, 4])", "output": "[1, 2, 3, 4]"}],
            constraints=["Both input lists are sorted", "Result should be sorted"],
            test_cases=[
                {"input": "merge_sorted([1, 3, 5], [2, 4, 6])", "output": "[1, 2, 3, 4, 5, 6]"},
                {"input": "merge_sorted([1, 2], [3, 4])", "output": "[1, 2, 3, 4]"},
                {"input": "merge_sorted([], [1, 2])", "output": "[1, 2]"},
                {"input": "merge_sorted([1, 2], [])", "output": "[1, 2]"},
                {"input": "merge_sorted([1], [2])", "output": "[1, 2]"}
            ],
            starter_code="def merge_sorted(list1, list2):\n    # Your code here\n    pass",
            category="Algorithms",
            order_index=9
        ),
        Problem(
            title="Binary Search",
            description="Implement binary search algorithm to find an element in a sorted list.",
            full_description="Write a function `binary_search` that takes a sorted list and a target value. Return the index of the target if found, or -1 if not found.\n\nExample:\n- binary_search([1, 2, 3, 4, 5], 3) should return 2\n- binary_search([1, 2, 3, 4, 5], 6) should return -1",
            difficulty="advanced",
            tags=["Algorithms", "Search"],
            points=45,
            estimated_time=40,
            examples=[{"input": "binary_search([1, 2, 3, 4, 5], 3)", "output": "2"}, {"input": "binary_search([1, 2, 3, 4, 5], 6)", "output": "-1"}],
            constraints=["Input list is sorted", "Time complexity should be O(log n)"],
            test_cases=[
                {"input": "binary_search([1, 2, 3, 4, 5], 3)", "output": "2"},
                {"input": "binary_search([1, 2, 3, 4, 5], 6)", "output": "-1"},
                {"input": "binary_search([1, 2, 3, 4, 5], 1)", "output": "0"},
                {"input": "binary_search([1, 2, 3, 4, 5], 5)", "output": "4"},
                {"input": "binary_search([1, 3, 5, 7, 9], 7)", "output": "3"}
            ],
            starter_code="def binary_search(arr, target):\n    # Your code here\n    pass",
            category="Algorithms",
            order_index=10
        ),
        Problem(
            title="Valid Parentheses",
            description="Check if a string containing parentheses is valid.",
            full_description="Write a function `is_valid_parentheses` that takes a string containing only parentheses characters and returns True if the parentheses are balanced, False otherwise.\n\nExample:\n- is_valid_parentheses(\"()\") should return True\n- is_valid_parentheses(\"()[]{}\") should return True\n- is_valid_parentheses(\"(]\") should return False",
            difficulty="intermediate",
            tags=["Stacks", "Strings"],
            points=35,
            estimated_time=25,
            examples=[{"input": "is_valid_parentheses(\"()\")", "output": "True"}, {"input": "is_valid_parentheses(\"()[]{}\")", "output": "True"}, {"input": "is_valid_parentheses(\"(]\")", "output": "False"}],
            constraints=["String contains only parentheses characters", "Use a stack data structure"],
            test_cases=[
                {"input": "is_valid_parentheses(\"()\")", "output": "True"},
                {"input": "is_valid_parentheses(\"()[]{}\")", "output": "True"},
                {"input": "is_valid_parentheses(\"(]\")", "output": "False"},
                {"input": "is_valid_parentheses(\"([{}])\")", "output": "True"},
                {"input": "is_valid_parentheses(\"([)]\")", "output": "False"}
            ],
            starter_code="def is_valid_parentheses(s):\n    # Your code here\n    pass",
            category="Algorithms",
            order_index=11
        ),
        Problem(
            title="Remove Duplicates",
            description="Remove duplicates from a list while preserving order.",
            full_description="Write a function `remove_duplicates` that takes a list and returns a new list with duplicates removed, preserving the original order.\n\nExample:\n- remove_duplicates([1, 2, 2, 3, 4, 4, 5]) should return [1, 2, 3, 4, 5]\n- remove_duplicates([\"a\", \"b\", \"a\", \"c\"]) should return [\"a\", \"b\", \"c\"]",
            difficulty="beginner",
            tags=["Lists", "Algorithms"],
            points=20,
            estimated_time=15,
            examples=[{"input": "remove_duplicates([1, 2, 2, 3, 4, 4, 5])", "output": "[1, 2, 3, 4, 5]"}, {"input": "remove_duplicates([\"a\", \"b\", \"a\", \"c\"])", "output": "[\"a\", \"b\", \"c\"]"}],
            constraints=["Preserve original order", "Return a new list"],
            test_cases=[
                {"input": "remove_duplicates([1, 2, 2, 3, 4, 4, 5])", "output": "[1, 2, 3, 4, 5]"},
                {"input": "remove_duplicates([\"a\", \"b\", \"a\", \"c\"])", "output": "[\"a\", \"b\", \"c\"]"},
                {"input": "remove_duplicates([1, 1, 1])", "output": "[1]"},
                {"input": "remove_duplicates([1, 2, 3])", "output": "[1, 2, 3]"},
                {"input": "remove_duplicates([])", "output": "[]"}
            ],
            starter_code="def remove_duplicates(lst):\n    # Your code here\n    pass",
            category="Lists",
            order_index=12
        ),
        Problem(
            title="Bubble Sort",
            description="Implement the bubble sort algorithm.",
            full_description="Write a function `bubble_sort` that takes a list of numbers and sorts them using the bubble sort algorithm.\n\nExample:\n- bubble_sort([64, 34, 25, 12, 22, 11, 90]) should return [11, 12, 22, 25, 34, 64, 90]",
            difficulty="intermediate",
            tags=["Algorithms", "Sorting"],
            points=40,
            estimated_time=30,
            examples=[{"input": "bubble_sort([64, 34, 25, 12, 22, 11, 90])", "output": "[11, 12, 22, 25, 34, 64, 90]"}],
            constraints=["Sort in-place or return new list", "Use bubble sort algorithm"],
            test_cases=[
                {"input": "bubble_sort([64, 34, 25, 12, 22, 11, 90])", "output": "[11, 12, 22, 25, 34, 64, 90]"},
                {"input": "bubble_sort([5, 2, 8, 1, 9])", "output": "[1, 2, 5, 8, 9]"},
                {"input": "bubble_sort([1])", "output": "[1]"},
                {"input": "bubble_sort([3, 1, 2])", "output": "[1, 2, 3]"},
                {"input": "bubble_sort([5, 4, 3, 2, 1])", "output": "[1, 2, 3, 4, 5]"}
            ],
            starter_code="def bubble_sort(arr):\n    # Your code here\n    pass",
            category="Algorithms",
            order_index=13
        ),
        Problem(
            title="Prime Number Checker",
            description="Check if a number is prime.",
            full_description="Write a function `is_prime` that takes a number and returns True if it is prime, False otherwise.\n\nExample:\n- is_prime(7) should return True\n- is_prime(10) should return False\n- is_prime(1) should return False",
            difficulty="beginner",
            tags=["Math", "Algorithms"],
            points=25,
            estimated_time=20,
            examples=[{"input": "is_prime(7)", "output": "True"}, {"input": "is_prime(10)", "output": "False"}, {"input": "is_prime(1)", "output": "False"}],
            constraints=["Handle edge cases (1, 2, negative numbers)", "Optimize for large numbers"],
            test_cases=[
                {"input": "is_prime(7)", "output": "True"},
                {"input": "is_prime(10)", "output": "False"},
                {"input": "is_prime(1)", "output": "False"},
                {"input": "is_prime(2)", "output": "True"},
                {"input": "is_prime(13)", "output": "True"},
                {"input": "is_prime(4)", "output": "False"}
            ],
            starter_code="def is_prime(n):\n    # Your code here\n    pass",
            category="Math",
            order_index=14
        ),
        Problem(
            title="Matrix Transpose",
            description="Transpose a matrix (2D list).",
            full_description="Write a function `transpose_matrix` that takes a 2D list (matrix) and returns its transpose.\n\nExample:\n- transpose_matrix([[1, 2, 3], [4, 5, 6]]) should return [[1, 4], [2, 5], [3, 6]]",
            difficulty="intermediate",
            tags=["Lists", "Algorithms"],
            points=35,
            estimated_time=25,
            examples=[{"input": "transpose_matrix([[1, 2, 3], [4, 5, 6]])", "output": "[[1, 4], [2, 5], [3, 6]]"}],
            constraints=["Handle rectangular matrices", "Return a new matrix"],
            test_cases=[
                {"input": "transpose_matrix([[1, 2, 3], [4, 5, 6]])", "output": "[[1, 4], [2, 5], [3, 6]]"},
                {"input": "transpose_matrix([[1, 2], [3, 4]])", "output": "[[1, 3], [2, 4]]"},
                {"input": "transpose_matrix([[1]])", "output": "[[1]]"},
                {"input": "transpose_matrix([[1, 2], [3, 4], [5, 6]])", "output": "[[1, 3, 5], [2, 4, 6]]"}
            ],
            starter_code="def transpose_matrix(matrix):\n    # Your code here\n    pass",
            category="Lists",
            order_index=15
        ),
    ]
    
    # Check existing problems
    existing_problem_count = db.query(Problem).count()
    existing_problem_titles = {p.title for p in db.query(Problem.title).all()}
    
    # Only add problems if database is empty, or add new ones that don't exist
    if existing_problem_count == 0:
        for problem in problems:
            db.add(problem)
        print(f"Created {len(problems)} coding problems")
    else:
        # Add only new problems that don't already exist
        new_problems = [p for p in problems if p.title not in existing_problem_titles]
        if new_problems:
            for problem in new_problems:
                db.add(problem)
            print(f"Added {len(new_problems)} new problems (skipped {len(problems) - len(new_problems)} duplicates)")
        else:
            print(f"All {len(problems)} problems already exist in database")
    
    db.commit()
    print("Problems initialized successfully!")
    
except Exception as e:
    db.rollback()
    print(f"Error initializing database: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()


