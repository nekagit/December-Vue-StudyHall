# Contributing to StudyHall Platform

Thank you for your interest in contributing to StudyHall! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/December-Vue-StudyHall.git
   cd December-Vue-StudyHall
   ```
3. **Set up development environment** (see [DEVELOPMENT.md](./DEVELOPMENT.md))
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### 1. Make Your Changes

- Write clean, readable code
- Follow the existing code style
- Add comments for complex logic
- Update documentation as needed

### 2. Test Your Changes

- Run backend tests: `pytest`
- Test frontend manually in dev mode
- Ensure no linter errors
- Test edge cases

### 3. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of what you added"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Be specific and concise
- Reference issue numbers if applicable: "Fix #123: description"

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots (if UI changes)
- Testing notes

## Code Style

### Python (Backend)

- Follow **PEP 8** style guide
- Use **type hints** for all functions
- Maximum line length: **88 characters** (Black formatter default)
- Use **4 spaces** for indentation (no tabs)
- Use **docstrings** for public functions/classes

**Example:**
```python
from typing import Optional
from sqlalchemy.orm import Session

def authenticate_student(
    db: Session, 
    email: str, 
    password: str
) -> Optional[Student]:
    """Authenticate a student by email and password.
    
    Args:
        db: Database session
        email: Student email address
        password: Plain text password
        
    Returns:
        Student object if authenticated, None otherwise
    """
    student = db.query(Student).filter(Student.email == email).first()
    if student and verify_password(password, student.password_hash):
        return student
    return None
```

**Tools:**
- Use `black` for formatting (if configured)
- Use `flake8` or `pylint` for linting
- Use `mypy` for type checking (if configured)

### TypeScript/Vue (Frontend)

- Use **Composition API** (`<script setup>`) for all components
- Use **TypeScript strict mode**
- Use **TailwindCSS** for all styling (no custom CSS)
- Use **camelCase** for variables and functions
- Use **PascalCase** for components

**Example:**
```vue
<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold">{{ title }}</h1>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  title: string
}

const props = defineProps<Props>()
const count = ref<number>(0)
</script>
```

**Tools:**
- Use ESLint (if configured)
- Use Prettier (if configured)
- Use Vue's built-in type checking

## Project Structure Guidelines

### Backend

- **Models** (`backend/models/`): Database models only, no business logic
- **Services** (`backend/services/`): Business logic, reusable functions
- **Routes** (`backend/main.py`): API endpoints, minimal logic (delegate to services)
- **Database** (`backend/database.py`): SQLAlchemy setup only

### Frontend

- **Views** (`frontend/src/views/`): Page-level components (routes)
- **Components** (`frontend/src/components/`): Reusable UI components
- **Utils** (`frontend/src/utils/`): Utility functions
- **Styles**: Use TailwindCSS classes, minimal custom CSS

## Testing Guidelines

### Backend Tests

- Write tests for all service functions
- Test API endpoints with pytest
- Use fixtures from `tests/conftest.py`
- Aim for good coverage of critical paths

**Example:**
```python
def test_authenticate_student_success(db_session):
    student = create_student(
        db_session, 
        "test@example.com", 
        "Test User", 
        "password123"
    )
    authenticated = authenticate_student(
        db_session, 
        "test@example.com", 
        "password123"
    )
    assert authenticated is not None
    assert authenticated.email == "test@example.com"
```

### Frontend Tests

- Test component rendering (if test framework is set up)
- Test user interactions
- Test API integration (mock API calls)

## Pull Request Process

### Before Submitting

1. **Update documentation** if you changed:
   - API endpoints → Update `API.md`
   - Architecture → Update `ARCHITECTURE.md`
   - Setup instructions → Update `README.md` or `DEVELOPMENT.md`

2. **Run tests**:
   ```bash
   pytest  # Backend tests
   npm run build  # Frontend build (catches TypeScript errors)
   ```

3. **Check for linting errors**:
   ```bash
   # Python (if configured)
   flake8 backend/
   
   # TypeScript (if configured)
   npm run lint
   ```

4. **Test manually**:
   - Start dev servers: `./manage.py dev`
   - Test your changes in the browser
   - Test edge cases

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Backend tests pass
- [ ] Frontend builds successfully
- [ ] Manual testing completed
- [ ] Edge cases tested

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings/errors
```

### Review Process

1. **Automated Checks**: CI/CD (if configured) runs tests
2. **Code Review**: Maintainers review code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, PR will be merged

## Feature Requests

If you have an idea for a new feature:

1. **Check existing issues** to avoid duplicates
2. **Create an issue** describing:
   - Use case
   - Proposed solution
   - Benefits
3. **Wait for discussion** before implementing
4. **Get approval** before starting work on large features

## Bug Reports

When reporting bugs, include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**:
   - OS and version
   - Python version
   - Node.js version
   - Browser (if frontend issue)
6. **Screenshots**: If applicable
7. **Logs**: Error messages or console output

## Documentation Contributions

Documentation improvements are always welcome:

- Fix typos or clarify wording
- Add missing information
- Improve examples
- Translate documentation (if applicable)

## Questions?

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion (if enabled)
- **Email**: Contact maintainers directly (if provided)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Recognition

Contributors will be recognized in:
- README.md (if applicable)
- Release notes
- GitHub contributors page

Thank you for contributing to StudyHall! 🎉
