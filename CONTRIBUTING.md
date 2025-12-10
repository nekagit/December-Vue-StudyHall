# Contributing Guide

Thank you for your interest in contributing to the StudyHall Platform! This guide will help you get started.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/December-Vue-StudyHall.git
   cd December-Vue-StudyHall
   ```
3. **Set up development environment** (see `DEVELOPMENT.md`)
4. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Process

### 1. Choose an Issue

- Check existing issues or create a new one
- Comment on the issue to claim it
- Discuss approach before starting major changes

### 2. Make Changes

- Follow code style guidelines (see below)
- Write clear, descriptive commit messages
- Keep changes focused and atomic
- Test your changes thoroughly

### 3. Commit Your Changes

Use descriptive commit messages:

```
feat: Add bookmark export functionality
fix: Resolve session expiration bug
docs: Update API documentation
refactor: Improve database query performance
test: Add tests for auth service
style: Format code with black
chore: Update dependencies
```

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to related issue
- Screenshots (if UI changes)
- Testing notes

## Code Style

### Python

- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 100 characters
- Use 4 spaces (no tabs)
- Use descriptive names

Example:
```python
from typing import Optional
from sqlalchemy.orm import Session

def get_student_by_email(
    db: Session, 
    email: str
) -> Optional[Student]:
    """Get a student by email address.
    
    Args:
        db: Database session
        email: Student email address
        
    Returns:
        Student object if found, None otherwise
    """
    return db.query(Student).filter(Student.email == email).first()
```

### TypeScript/Vue

- Use Composition API (`<script setup>`)
- TypeScript strict mode
- TailwindCSS for styling
- Prefer `const` over `let`
- Use async/await

Example:
```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Material {
  id: number
  title: string
  category: string
}

const materials = ref<Material[]>([])

onMounted(async () => {
  try {
    const response = await fetch('/api/materials', {
      credentials: 'include'
    })
    materials.value = await response.json()
  } catch (error) {
    console.error('Failed to load materials:', error)
  }
})
</script>
```

## Project Structure

### Backend

- `backend/models/`: Database models
- `backend/services/`: Business logic
- `backend/main.py`: API routes
- Keep routes thin, move logic to services

### Frontend

- `frontend/src/views/`: Page components
- `frontend/src/components/`: Reusable components
- `frontend/src/utils/`: Utility functions
- Keep components focused and reusable

## Testing

### Writing Tests

- Test critical paths
- Test edge cases
- Test error handling
- Keep tests simple and readable

### Running Tests

```bash
# Backend tests
pytest backend/tests/

# Frontend tests
cd frontend
npm run test
```

## Documentation

### Code Documentation

- Add docstrings to functions
- Comment complex logic
- Update README if needed
- Update API.md for API changes

### Pull Request Documentation

- Describe what changed
- Explain why it changed
- Include screenshots for UI changes
- Update relevant docs

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No console errors/warnings
- [ ] Commits are atomic and well-described

### PR Checklist

- [ ] Clear title and description
- [ ] References related issue
- [ ] Screenshots (if UI changes)
- [ ] Breaking changes documented
- [ ] Migration guide (if database changes)

### Review Process

1. Maintainers will review your PR
2. Address feedback promptly
3. Keep discussion constructive
4. Be patient - reviews take time

## Feature Guidelines

### Adding New Features

1. **Discuss first**: Open an issue to discuss
2. **Keep it focused**: One feature per PR
3. **Follow patterns**: Match existing code style
4. **Test thoroughly**: Manual and automated tests
5. **Document**: Update relevant docs

### Feature Ideas

Great areas for contribution:
- UI/UX improvements
- Performance optimizations
- Additional integrations
- Testing coverage
- Documentation improvements
- Accessibility enhancements

## Bug Reports

### Before Reporting

1. Check existing issues
2. Reproduce the bug
3. Check recent changes

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Screenshots**
If applicable

**Environment**
- OS: [e.g., macOS 12.0]
- Browser: [e.g., Chrome 120]
- Version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information
```

## Questions?

- Check existing documentation
- Search closed issues
- Ask in discussions
- Open a question issue

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (if created)
- Credited in release notes
- Appreciated by the community!

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

Thank you for contributing to StudyHall Platform! 🎉
