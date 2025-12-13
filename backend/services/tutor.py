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
            
            response = self.client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                abstract = data.get("AbstractText", "")
                answer = data.get("Answer", "")
                definition = data.get("Definition", "")
                
                # Combine results
                results = []
                if abstract:
                    results.append(abstract)
                if answer:
                    results.append(answer)
                if definition:
                    results.append(definition)
                
                if results:
                    return " ".join(results)
            
            # Fallback: Use HTML scraping from DuckDuckGo search results
            search_url = f"https://html.duckduckgo.com/html/?q={search_query.replace(' ', '+')}"
            html_response = self.client.get(search_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            if html_response.status_code == 200:
                # Extract text from HTML (simple extraction)
                text = html_response.text
                # Remove HTML tags
                text = re.sub(r'<[^>]+>', '', text)
                # Get first 500 characters as summary
                return text[:500] if text else ""
            
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
            response_parts.append(f"{search_results}\n")
        else:
            # Fallback explanation based on common patterns
            if "how" in question.lower():
                response_parts.append(f"Here's how to approach this in {language}:\n\n")
            elif "what" in question.lower():
                response_parts.append(f"In {language}, this refers to:\n\n")
            elif "why" in question.lower():
                response_parts.append(f"The reason for this in {language} is:\n\n")
            else:
                response_parts.append(f"Let me explain this {language} concept:\n\n")
            
            response_parts.append(f"**{question}** is an important concept in {language} programming. ")
            response_parts.append("To fully understand this, I recommend:\n")
            response_parts.append("1. Reviewing the official documentation\n")
            response_parts.append("2. Practicing with simple examples\n")
            response_parts.append("3. Building a small project to apply the concept\n")
        
        # Code examples section
        response_parts.append(f"\n## Example in {language}\n")
        response_parts.append("Here's a simple example to illustrate the concept:\n\n")
        response_parts.append("```" + language.lower() + "\n")
        
        # Generate example based on language
        example_code = self._generate_example_code(language)
        response_parts.append(example_code)
        response_parts.append("\n```\n")
        
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
    
    def _generate_example_code(self, language: str) -> str:
        """Generate example code based on language."""
        lang_lower = language.lower()
        
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






