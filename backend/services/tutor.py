"""
Tutor service for AI-powered programming language tutoring.
Uses web search to gather online data and generates educational responses.
"""
import os
import tempfile
import uuid
from typing import Dict, Any
import httpx
import re
from datetime import datetime


class TutorService:
    """Service for AI tutoring with web search integration."""
    
    def __init__(self):
        self.client = httpx.Client(timeout=30.0)
        self.temp_files: Dict[str, str] = {}  # Store temp file paths by session_id
    
    def search_web(self, query: str, language: str = "") -> str:
        """Search the web for information about the query and language."""
        try:
            # Use DuckDuckGo Instant Answer API (free, no API key needed)
            search_query = f"{language} {query}" if language else query
            url = "https://api.duckduckgo.com/"
            params = {
                "q": search_query,
                "format": "json",
                "no_html": "1",
                "skip_disambig": "1"
            }
            
            response = self.client.get(url, params=params, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                abstract = data.get("AbstractText", "")
                answer = data.get("Answer", "")
                definition = data.get("Definition", "")
                related_topics = data.get("RelatedTopics", [])
                
                # Combine results
                results = []
                if abstract:
                    results.append(abstract)
                if answer:
                    results.append(answer)
                if definition:
                    results.append(definition)
                
                # Extract related topics
                if related_topics:
                    topic_texts = []
                    for topic in related_topics[:3]:  # Limit to first 3
                        if isinstance(topic, dict):
                            topic_text = topic.get("Text", "")
                            if topic_text:
                                topic_texts.append(topic_text)
                    if topic_texts:
                        results.append("Related: " + " ".join(topic_texts[:200]))
                
                if results:
                    return " ".join(results)
            
            # Fallback: Use HTML scraping from DuckDuckGo search results
            search_url = f"https://html.duckduckgo.com/html/?q={search_query.replace(' ', '+')}"
            html_response = self.client.get(search_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }, timeout=10.0)
            
            if html_response.status_code == 200:
                # Extract text from HTML (simple extraction)
                text = html_response.text
                # Remove HTML tags
                text = re.sub(r'<[^>]+>', '', text)
                # Remove extra whitespace
                text = re.sub(r'\s+', ' ', text)
                # Get first 800 characters as summary
                return text[:800] if text else ""
            
            return ""
        except httpx.TimeoutException:
            print(f"Web search timeout for query: {query}")
            return ""
        except (httpx.HTTPError, httpx.RequestError, Exception) as e:
            print(f"Web search error: {e}")
            return ""
    
    def generate_tutor_response(self, question: str, language: str) -> str:
        """Generate an educational tutor response based on question and language."""
        # Search for relevant information
        search_results = self.search_web(question, language)
        
        # Generate structured markdown response
        response_parts = []
        
        # Header
        response_parts.append(f"# {language} Tutoring: {question}\n")
        response_parts.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        # Introduction
        response_parts.append(f"\n## Understanding Your Question\n")
        response_parts.append(f"You asked about **{question}** in the context of **{language}**. ")
        response_parts.append("Let me help you understand this concept!\n")
        
        # Main explanation
        response_parts.append("\n## Explanation\n")
        
        if search_results:
            # Clean and format search results
            cleaned_results = search_results.strip()
            if len(cleaned_results) > 100:
                response_parts.append(f"{cleaned_results}\n\n")
            else:
                response_parts.append(f"{cleaned_results}\n")
                # Add additional context if results are short
                response_parts.append(f"\nThis concept is fundamental in {language} programming. ")
                response_parts.append("Understanding it will help you write better code.\n")
        else:
            # Fallback explanation based on common patterns
            question_lower = question.lower()
            if "how" in question_lower or "how to" in question_lower:
                response_parts.append(f"Here's how to approach this in {language}:\n\n")
                response_parts.append(f"**{question}** is a common task in {language}. ")
                response_parts.append("The approach typically involves:\n")
                response_parts.append("1. Understanding the problem requirements\n")
                response_parts.append("2. Breaking it down into smaller steps\n")
                response_parts.append("3. Using appropriate {language} features and libraries\n")
                response_parts.append("4. Testing and refining your solution\n\n")
            elif "what" in question_lower:
                response_parts.append(f"In {language}, **{question}** refers to:\n\n")
                response_parts.append("This is an important concept that you'll encounter frequently. ")
                response_parts.append("It's used to solve specific programming challenges and is part of the core {language} knowledge.\n\n")
            elif "why" in question_lower:
                response_parts.append(f"The reason for this in {language} is:\n\n")
                response_parts.append(f"Understanding why {question} works this way helps you:\n")
                response_parts.append("1. Make better design decisions\n")
                response_parts.append("2. Write more efficient code\n")
                response_parts.append("3. Debug issues more effectively\n\n")
            elif "when" in question_lower:
                response_parts.append(f"You should use this in {language} when:\n\n")
                response_parts.append("1. You need to solve a specific type of problem\n")
                response_parts.append("2. The situation calls for this particular approach\n")
                response_parts.append("3. It's the most appropriate solution for your use case\n\n")
            else:
                response_parts.append(f"Let me explain **{question}** in {language}:\n\n")
                response_parts.append(f"This is an important concept in {language} programming. ")
                response_parts.append("To fully understand this, I recommend:\n")
                response_parts.append("1. Reviewing the official documentation\n")
                response_parts.append("2. Practicing with simple examples\n")
                response_parts.append("3. Building a small project to apply the concept\n\n")
        
        # Code examples section
        response_parts.append(f"\n## Example in {language}\n")
        response_parts.append("Here's a simple example to illustrate the concept:\n\n")
        response_parts.append("```" + language.lower() + "\n")
        
        # Generate example based on language and question context
        example_code = self._generate_example_code(language, question)
        response_parts.append(example_code)
        response_parts.append("\n```\n")
        
        # Add explanation of the example
        response_parts.append("\n**What this example does:**\n")
        response_parts.append("- Demonstrates the core concept\n")
        response_parts.append("- Shows practical usage\n")
        response_parts.append("- Provides a starting point for your own code\n")
        
        # Best practices
        response_parts.append("\n## Best Practices\n")
        response_parts.append(f"When working with this concept in {language}:\n")
        response_parts.append("- Always refer to the official documentation\n")
        response_parts.append("- Test your code with different inputs\n")
        response_parts.append("- Consider edge cases and error handling\n")
        response_parts.append("- Write clean, readable code\n")
        
        # Additional resources
        response_parts.append("\n## Additional Resources\n")
        response_parts.append(f"- Official {language} Documentation\n")
        response_parts.append(f"- {language} Community Forums\n")
        response_parts.append("- Online tutorials and courses\n")
        response_parts.append("- Practice problems on coding platforms\n")
        
        # Encouragement
        response_parts.append("\n## Keep Learning!\n")
        response_parts.append("Remember, learning programming takes practice. ")
        response_parts.append("Don't hesitate to experiment and build projects to reinforce your understanding!\n")
        
        return "".join(response_parts)
    
    def _generate_example_code(self, language: str, question: str = "") -> str:
        """Generate example code based on language and question context."""
        lang_lower = language.lower()
        question_lower = question.lower() if question else ""
        
        # Try to generate context-aware examples based on question keywords
        if "function" in question_lower or "def" in question_lower:
            return self._get_function_example(lang_lower)
        elif "class" in question_lower or "object" in question_lower or "oop" in question_lower:
            return self._get_class_example(lang_lower)
        elif "loop" in question_lower or "iterate" in question_lower or "for" in question_lower:
            return self._get_loop_example(lang_lower)
        elif "list" in question_lower or "array" in question_lower:
            return self._get_list_example(lang_lower)
        elif "dictionary" in question_lower or "dict" in question_lower or "map" in question_lower:
            return self._get_dict_example(lang_lower)
        elif "async" in question_lower or "await" in question_lower or "asynchronous" in question_lower:
            return self._get_async_example(lang_lower)
        elif "error" in question_lower or "exception" in question_lower or "try" in question_lower:
            return self._get_error_handling_example(lang_lower)
        
        # Common examples for different languages
        examples = {
            "python": """# Example: Basic Python concept
def example_function():
    \"\"\"Demonstrates the concept.\"\"\"
    result = "Hello, World!"
    return result

# Usage
output = example_function()
print(output)""",
            "javascript": """// Example: Basic JavaScript concept
function exampleFunction() {
    // Demonstrates the concept
    const result = "Hello, World!";
    return result;
}

// Usage
const output = exampleFunction();
console.log(output);""",
            "java": """// Example: Basic Java concept
public class Example {
    public static void main(String[] args) {
        // Demonstrates the concept
        String result = "Hello, World!";
        System.out.println(result);
    }
}""",
            "cpp": """// Example: Basic C++ concept
#include <iostream>
using namespace std;

int main() {
    // Demonstrates the concept
    string result = "Hello, World!";
    cout << result << endl;
    return 0;
}""",
            "c": """// Example: Basic C concept
#include <stdio.h>

int main() {
    // Demonstrates the concept
    char* result = "Hello, World!";
    printf("%s\\n", result);
    return 0;
}""",
            "go": """// Example: Basic Go concept
package main

import "fmt"

func main() {
    // Demonstrates the concept
    result := "Hello, World!"
    fmt.Println(result)
}""",
            "rust": """// Example: Basic Rust concept
fn main() {
    // Demonstrates the concept
    let result = "Hello, World!";
    println!("{}", result);
}""",
            "typescript": """// Example: Basic TypeScript concept
function exampleFunction(): string {
    // Demonstrates the concept
    const result: string = "Hello, World!";
    return result;
}

// Usage
const output: string = exampleFunction();
console.log(output);""",
        }
        
        return examples.get(lang_lower, examples.get("python", "# Code example here"))
    
    def _get_function_example(self, lang: str) -> str:
        """Get function example for language."""
        examples = {
            "python": """def calculate_sum(a, b):
    \"\"\"Add two numbers and return the result.\"\"\"
    return a + b

result = calculate_sum(5, 3)
print(f"Sum: {result}")  # Output: Sum: 8""",
            "javascript": """function calculateSum(a, b) {
    return a + b;
}

const result = calculateSum(5, 3);
console.log(`Sum: ${result}`);  // Output: Sum: 8""",
        }
        return examples.get(lang, examples.get("python", ""))
    
    def _get_class_example(self, lang: str) -> str:
        """Get class example for language."""
        examples = {
            "python": """class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"I'm {self.name}, {self.age} years old"

person = Person("Alice", 30)
print(person.introduce())""",
            "javascript": """class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    introduce() {
        return `I'm ${this.name}, ${this.age} years old`;
    }
}

const person = new Person("Alice", 30);
console.log(person.introduce());""",
        }
        return examples.get(lang, examples.get("python", ""))
    
    def _get_loop_example(self, lang: str) -> str:
        """Get loop example for language."""
        examples = {
            "python": """# Iterate over a list
fruits = ['apple', 'banana', 'orange']
for fruit in fruits:
    print(fruit)

# With index
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")""",
            "javascript": """// Iterate over an array
const fruits = ['apple', 'banana', 'orange'];
for (const fruit of fruits) {
    console.log(fruit);
}

// With index
fruits.forEach((fruit, i) => {
    console.log(`${i}: ${fruit}`);
});""",
        }
        return examples.get(lang, examples.get("python", ""))
    
    def _get_list_example(self, lang: str) -> str:
        """Get list/array example for language."""
        examples = {
            "python": """# Create and manipulate a list
numbers = [1, 2, 3, 4, 5]
numbers.append(6)  # Add element
numbers.remove(2)  # Remove element
print(numbers)  # [1, 3, 4, 5, 6]

# List comprehension
squares = [x**2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]""",
            "javascript": """// Create and manipulate an array
const numbers = [1, 2, 3, 4, 5];
numbers.push(6);  // Add element
numbers.splice(1, 1);  // Remove element at index 1
console.log(numbers);  // [1, 3, 4, 5, 6]

// Map to create new array
const squares = numbers.map(x => x * x);
console.log(squares);""",
        }
        return examples.get(lang, examples.get("python", ""))
    
    def _get_dict_example(self, lang: str) -> str:
        """Get dictionary/map example for language."""
        examples = {
            "python": """# Create and use a dictionary
student = {
    'name': 'Alice',
    'age': 20,
    'grade': 'A'
}

# Access values
print(student['name'])  # Alice
print(student.get('age'))  # 20

# Add/update
student['email'] = 'alice@example.com'
student['age'] = 21

# Iterate
for key, value in student.items():
    print(f"{key}: {value}")""",
            "javascript": """// Create and use an object/map
const student = {
    name: 'Alice',
    age: 20,
    grade: 'A'
};

// Access values
console.log(student.name);  // Alice
console.log(student['age']);  // 20

// Add/update
student.email = 'alice@example.com';
student.age = 21;

// Iterate
Object.entries(student).forEach(([key, value]) => {
    console.log(`${key}: ${value}`);
});""",
        }
        return examples.get(lang, examples.get("python", ""))
    
    def _get_async_example(self, lang: str) -> str:
        """Get async/await example for language."""
        examples = {
            "python": """import asyncio

async def fetch_data():
    await asyncio.sleep(1)  # Simulate API call
    return "Data fetched"

async def main():
    result = await fetch_data()
    print(result)

# Run async function
asyncio.run(main())""",
            "javascript": """// Async function
async function fetchData() {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return "Data fetched";
}

// Use async function
async function main() {
    const result = await fetchData();
    console.log(result);
}

main();""",
        }
        return examples.get(lang, examples.get("python", ""))
    
    def _get_error_handling_example(self, lang: str) -> str:
        """Get error handling example for language."""
        examples = {
            "python": """try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"An error occurred: {e}")
else:
    print("No errors occurred")
finally:
    print("This always runs")""",
            "javascript": """try {
    const result = 10 / 0;
    if (!isFinite(result)) {
        throw new Error("Division resulted in infinity");
    }
} catch (error) {
    console.error(`An error occurred: ${error.message}`);
} finally {
    console.log("This always runs");
}""",
        }
        return examples.get(lang, examples.get("python", ""))
    
    def create_tutor_response(self, question: str, language: str) -> Dict[str, Any]:
        """Create a tutor response and save to temporary markdown file."""
        # Generate response
        markdown_content = self.generate_tutor_response(question, language)
        
        # Create temporary file
        session_id = str(uuid.uuid4())
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"tutor_{session_id}.md")
        
        try:
            with open(temp_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Store file path
            self.temp_files[session_id] = temp_file_path
            
            return {
                "success": True,
                "session_id": session_id,
                "markdown": markdown_content,
                "file_path": temp_file_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create response: {str(e)}"
            }
    
    def delete_tutor_file(self, session_id: str) -> bool:
        """Delete the temporary tutor markdown file."""
        if session_id not in self.temp_files:
            return False
        
        file_path = self.temp_files[session_id]
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            del self.temp_files[session_id]
            return True
        except (OSError, FileNotFoundError) as e:
            print(f"Error deleting tutor file: {e}")
            return False
    
    def close(self):
        """Close the HTTP client and clean up."""
        # Clean up all temp files
        for file_path in list(self.temp_files.values()):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except (OSError, FileNotFoundError):
                pass
        self.temp_files.clear()
        self.client.close()


# Global instance
tutor_service = TutorService()






