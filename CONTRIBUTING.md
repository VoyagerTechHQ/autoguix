# Contributing to AutoGUI-X

Thank you for your interest in contributing to AutoGUI-X! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- macOS 10.14+
- uv (recommended) or pip
- Git

### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/autoguix.git
cd autoguix

# Create virtual environment
uv venv
source .venv/bin/activate

# Install in development mode with all dependencies
uv pip install -e ".[locate,dev]"

# Run tests to verify setup
pytest
```

## 📝 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Follow the existing code style
- Add tests for new features
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest --cov=autoguix
```

### 4. Format Code

```bash
# Format with black
black autoguix tests

# Lint with ruff
ruff check autoguix tests
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add awesome feature"
# or
git commit -m "fix: resolve issue with mouse clicks"
```

Use conventional commit messages:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📚 Code Guidelines

### Python Style

- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 100 characters
- Use docstrings (Google style) for all public functions and classes

### Example

```python
async def move_mouse(self, x: int, y: int, duration: float = 0.0) -> None:
    """Move mouse to specified coordinates.
    
    Args:
        x: X coordinate
        y: Y coordinate
        duration: Time to complete the movement in seconds
        
    Raises:
        ValueError: If coordinates are out of screen bounds
    """
    # Implementation here
    pass
```

### Testing

- Write tests for all new features
- Maintain or improve code coverage
- Use pytest fixtures for common setup
- Test both sync and async versions of functions

## 🏗️ Project Structure

```
autoguix/
├── autoguix/           # Main package
│   ├── __init__.py     # User API
│   ├── core/           # Core logic
│   │   ├── automation_core.py
│   │   ├── backend_base.py
│   │   └── types.py
│   └── backends/       # Platform backends
│       └── macos_backend.py
├── examples/           # Example scripts
├── tests/              # Test suite
└── docs/               # Documentation
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Minimal code to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**:
   - macOS version
   - Python version
   - AutoGUI-X version

## 💡 Suggesting Features

Feature requests are welcome! Please include:

1. **Use Case**: Why you need this feature
2. **Proposed Solution**: How you think it should work
3. **Alternatives**: Any alternative solutions you've considered

## 📄 License

By contributing, you agree that your contributions will be licensed under the BSD 3-Clause License.

## 🙏 Thank You!

Your contributions make AutoGUI-X better for everyone. Thank you for taking the time to contribute!
