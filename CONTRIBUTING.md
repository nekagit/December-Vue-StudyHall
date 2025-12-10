# Contributing Guide

Thank you for your interest in contributing to the StudyHall Platform! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/December-Vue-StudyHall.git
   cd December-Vue-StudyHall
   ```

3. **Set up development environment:**
   ```bash
   # Backend
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

4. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### 1. Create an Issue

Before starting work on a major feature, create an issue to discuss:
- The problem you're solving
- Proposed solution
- Implementation approach

### 2. Make Changes

- Write clean, maintainable code
- Follow the coding standards
- Add tests for new features
- Update documentation

### 3. Test Your Changes

```bash
# Backend tests
pytest backend/tests/

# Frontend tests (if available)
cd frontend && npm test

# Manual testing
./manage.py dev
```

### 4. Commit Your Changes

Follow the commit message conventions (see below).

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Coding Standards

### Python

- **Style**: Follow PEP 8
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Add docstrings for public functions
- **Line Length**: Maximum 100 characters
- **Imports**: Use absolute imports, group by standard library, third-party, local

**Example:**
```python
from typing import Optional
from sqlalchemy.orm import Session

from backend.models.student import Student
from backend.services.auth import hash_password


def create_student(
    db: Session, 
    email: str, 
    name: str, 
    password: str
) -> Student:
    """
    Create a new student account.
    
    Args:
        db: Database session
        email: Student email address
        name: Student name
        password: Plain text password
        
    Returns:
        Created Student object
        
    Raises:
        ValueError: If email exists or student limit reached
    """
    # Implementation
```

### TypeScript/Vue

- **Style**: Use Composition API (`<script setup>`)
- **Types**: Use TypeScript strict mode
- **Naming**: camelCase for variables, PascalCase for components
- **Styling**: Use TailwindCSS utility classes

**Example:**
```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

interface Material {
  id: number
  title: string
}

const materials = ref<Material[]>([])
const isLoading = ref(false)

const hasMaterials = computed(() => materials.value.length > 0)
</script>

<template>
  <div class="container mx-auto p-4">
    <div v-if="isLoading" class="text-center">
      Loading...
    </div>
    <div v-else-if="hasMaterials">
      <!-- Content -->
    </div>
  </div>
</template>
```

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(auth): add password reset functionality

Add password reset endpoint and email service integration.
Users can now request password reset via email.

Closes #123
```

```
fix(materials): resolve search filter issue

Fix bug where search filter was case-sensitive.
Now uses case-insensitive matching.

Fixes #456
```

```
docs(api): update authentication endpoints documentation

Add examples and error response documentation for all
authentication endpoints.
```

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No linter errors
- [ ] Commit messages follow conventions

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
Describe how you tested your changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated
- [ ] All tests pass
```

### Review Process

1. **Automated Checks**: CI/CD will run tests and linting
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any feedback or requested changes
4. **Approval**: Once approved, your PR will be merged

## Testing

### Backend Testing

Create tests in `backend/tests/`:

```python
# backend/tests/test_auth.py
import pytest
from backend.services.auth import create_student, authenticate_student

def test_create_student(db_session):
    student = create_student(
        db_session, 
        "test@test.com", 
        "Test User", 
        "password123"
    )
    assert student.email == "test@test.com"
    assert student.name == "Test User"

def test_authenticate_student(db_session):
    create_student(
        db_session, 
        "test@test.com", 
        "Test User", 
        "password123"
    )
    authenticated = authenticate_student(
        db_session, 
        "test@test.com", 
        "password123"
    )
    assert authenticated is not None
```

### Frontend Testing

Add component tests using Vitest:

```typescript
// frontend/src/components/__tests__/Button.test.ts
import { mount } from '@vue/test-utils'
import Button from '../Button.vue'

describe('Button', () => {
  it('renders label correctly', () => {
    const wrapper = mount(Button, {
      props: { label: 'Click me' }
    })
    expect(wrapper.text()).toContain('Click me')
  })
})
```

## Documentation

### Code Documentation

- Add docstrings to Python functions
- Add JSDoc comments to TypeScript functions
- Comment complex logic
- Update README for major changes

### API Documentation

- Update `API.md` for new endpoints
- Include request/response examples
- Document error responses

### User Documentation

- Update `README.md` for new features
- Add examples and use cases
- Update setup instructions if needed

## Project-Specific Guidelines

### Adding New Features

1. **Backend:**
   - Add model in `backend/models/`
   - Add service logic in `backend/services/`
   - Add endpoint in `backend/main.py`
   - Add tests in `backend/tests/`

2. **Frontend:**
   - Create view in `frontend/src/views/`
   - Add route in `frontend/src/main.ts`
   - Update navigation if needed
   - Add component tests

### Database Changes

- Create migration scripts
- Update models in `backend/models/`
- Document schema changes
- Test migrations on sample data

### API Changes

- Follow RESTful conventions
- Use consistent error responses
- Update API documentation
- Consider backward compatibility

## Questions?

- Open an issue for questions
- Check existing issues and PRs
- Review documentation files

## Recognition

Contributors will be:
- Listed in project README (if desired)
- Credited in release notes
- Appreciated by the community!

Thank you for contributing! 🎉
