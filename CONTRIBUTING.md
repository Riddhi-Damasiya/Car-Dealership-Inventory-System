# Contributing Guidelines

## Development Workflow

This project follows a Test-Driven Development (TDD) approach with a focus on clean code and SOLID principles.

### Git Workflow

1. **Create feature branches:** `git checkout -b feature/your-feature-name`
2. **Make small, focused commits:** Each commit should be logically independent
3. **Write descriptive commit messages:** Follow the format below
4. **Include AI co-authorship when applicable:** When AI assistance was used significantly

### Commit Message Format

```
<type>: <subject>

<body>

[Co-authored-by: Antigravity <antigravity@users.noreply.github.com>]
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `test:` - Test additions or modifications
- `chore:` - Build, configuration, or tooling changes
- `docs:` - Documentation
- `refactor:` - Code refactoring without feature changes

**Example:**
```
feat: implement vehicle purchase endpoint

Added POST /api/vehicles/{id}/purchase to decrement inventory quantity.
Validates stock availability and prevents negative quantity.
Returns updated vehicle with new quantity.

Co-authored-by: Antigravity <antigravity@users.noreply.github.com>
```

## Code Standards

### Python (Backend)

- **Formatter:** Black (line length: 100)
- **Linter:** Ruff
- **Type Checking:** MyPy
- **Test Runner:** Pytest with async support

```bash
# Format code
black backend/

# Lint
ruff check backend/

# Type check
mypy backend/

# Run tests
pytest tests/ -v --cov=app
```

### JavaScript (Frontend)

- **Formatter:** Prettier
- **Linter:** ESLint (react-app config)
- **Test Runner:** Vitest

```bash
# Format code
npm run format

# Lint
npm run lint

# Run tests
npm run test

# Coverage
npm run coverage
```

## Test-Driven Development

Follow the Red-Green-Refactor cycle:

1. **Red:** Write failing tests that describe the desired behavior
2. **Green:** Write minimal code to pass the tests
3. **Refactor:** Improve code quality without changing behavior

### Test Coverage Requirements

- **Backend:** Aim for >80% coverage
- **Frontend:** Aim for >80% coverage
- **E2E:** Cover critical user flows

## Pull Request Process

1. Ensure all tests pass locally
2. Ensure code formatting and linting pass
3. Write clear PR description explaining changes
4. Ensure commits are logically organized
5. Include any necessary documentation updates

## Reporting Issues

When reporting bugs, include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Node/Python version, etc.)

## AI Assistance Policy

When using AI tools (like GitHub Copilot):
1. Review all generated code carefully
2. Understand the code before committing
3. Test thoroughly
4. Include co-authorship in commit message
5. Document significant AI-assisted changes in PROMPTS.md

---

For more details, see the main README.md
