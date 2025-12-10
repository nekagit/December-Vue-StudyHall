# Testing Guide

This project includes comprehensive testing infrastructure for both backend and frontend.

## Backend Tests

Backend tests use **pytest** with coverage reporting.

### Running Backend Tests

```bash
cd backend
pytest
```

### Running with Coverage

```bash
cd backend
pytest --cov=backend --cov-report=html --cov-report=json
```

Coverage reports will be generated in:
- HTML: `backend/htmlcov/index.html`
- JSON: `backend/coverage.json`

### Test Structure

- `backend/tests/` - All test files
- `backend/tests/test_models.py` - Model tests
- `backend/tests/test_auth_service.py` - Authentication service tests
- `backend/tests/test_session_service.py` - Session service tests
- `backend/tests/test_api.py` - API endpoint tests

## Frontend Tests

Frontend tests use **Vitest** with Vue Test Utils.

### Running Frontend Tests

```bash
cd frontend
npm run test
```

### Running with Coverage

```bash
cd frontend
npm run test:coverage
```

Coverage reports will be generated in `frontend/coverage/`.

### Test Structure

- `frontend/tests/` - All test files
- `frontend/tests/components/` - Component tests
- `frontend/tests/views/` - View/page tests

## Test Dashboard

Access the test dashboard at `/tests` route (requires authentication).

The dashboard provides:
- **Coverage Summary**: Overall coverage percentages for backend and frontend
- **File-level Coverage**: Detailed coverage for each file
- **Test Results**: Pass/fail status for all tests
- **Run Tests**: Buttons to run tests directly from the UI
- **Refresh Coverage**: Update coverage data without running tests

### API Endpoints

- `POST /api/tests/backend/run` - Run backend tests
- `GET /api/tests/backend/coverage` - Get backend coverage data
- `POST /api/tests/frontend/run` - Run frontend tests
- `GET /api/tests/frontend/coverage` - Get frontend coverage data
- `GET /api/tests/summary` - Get summary of all tests and coverage

## Writing Tests

### Backend Test Example

```python
def test_example(db_session):
    """Test example."""
    # Your test code here
    assert True
```

### Frontend Test Example

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from '@/components/MyComponent.vue'

describe('MyComponent', () => {
  it('renders correctly', () => {
    const wrapper = mount(MyComponent)
    expect(wrapper.text()).toContain('Expected Text')
  })
})
```

## Coverage Goals

- **Backend**: Aim for >80% coverage
- **Frontend**: Aim for >70% coverage

## Continuous Integration

Tests should be run automatically in CI/CD pipelines. The test dashboard can be used to monitor test health and coverage trends.
