# Contributing to NarrativeNexus

First off, thank you for considering contributing to the AI Content Generation Pipeline! 🎉

This document provides guidelines for contributing to this project. Following these guidelines helps communicate that you respect the time of the developers managing and developing this open-source project.

## 🌟 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots)
- **Describe the behavior you observed** and what you expected
- **Include your environment details** (OS, Python version, etc.)

**Example Bug Report Template:**
```markdown
**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
What you expected to happen

**Actual Behavior:**
What actually happened

**Environment:**
- OS: Windows 11 / macOS 14 / Ubuntu 22.04
- Python Version: 3.12.1
- Browser: Chrome 120

**Screenshots:**
If applicable, add screenshots
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a step-by-step description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any similar features** in other projects (if applicable)

### Pull Requests

1. **Fork the repository** and create your branch from `main`:
   ```bash
   git checkout -b feature/AmazingFeature
   ```

2. **Make your changes** following our coding standards

3. **Test your changes thoroughly**

4. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add: New feature for XYZ"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/AmazingFeature
   ```

6. **Open a Pull Request** with a clear description

## 📝 Development Guidelines

### Code Style

We follow PEP 8 style guide for Python code:

- Use **4 spaces** for indentation (not tabs)
- Maximum line length: **127 characters**
- Use **descriptive variable names**
- Add **docstrings** to all functions and classes
- Format code with **Black**:
  ```bash
  black .
  ```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: Add support for GPT-4 model
fix: Resolve memory leak in agent orchestration
docs: Update installation instructions for Windows
```

### Testing

- Write tests for new features using `pytest`
- Ensure all tests pass before submitting PR:
  ```bash
  pytest
  ```
- Aim for at least 80% code coverage

### Documentation

- Update the README.md if you change functionality
- Add docstrings to new functions/classes
- Update DEPLOYMENT.md for deployment-related changes

## 🔧 Setting Up Development Environment

1. **Clone your fork:**
   ```bash
   git clone https://github.com/nadir-sheikh09/Content-Generation-Pipeline-Agent.git
   cd Content-Generation-Pipeline-Agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8 black  # Development tools
   ```

4. **Create a .env file:**
   ```bash
   cp .env.example .env
   # Add your DEEPSEEK_API_KEY
   ```

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest test_specific.py

# Run with verbose output
pytest -v
```

## 🎯 Project Structure

```
Content-Generation-Pipeline-Agent/
├── app.py                        # Streamlit UI
├── content_generation_crew.py    # Multi-agent orchestration
├── custom_tools.py               # Custom CrewAI tools
├── quality_scorer.py             # Content quality metrics
├── content_versioning.py         # Version control
├── logger.py                     # Logging utilities
├── requirements.txt              # Dependencies
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # CI/CD pipeline
├── tests/                        # Test files (add yours here)
└── docs/                         # Additional documentation
```

## 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested

## 📋 Pull Request Checklist

Before submitting your PR, make sure:

- [ ] Code follows the style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] No new warnings generated
- [ ] Tests added/updated and passing
- [ ] Branch is up to date with main

## 💬 Communication

- **GitHub Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions
- **Discussions**: For questions and general discussion

## 🙏 Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🚀**

If you have questions, feel free to open an issue or reach out to the maintainers.
