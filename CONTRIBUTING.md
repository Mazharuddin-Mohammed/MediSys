# Contributing to MediSys

Thank you for your interest in contributing to MediSys! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
   - [Setting Up Your Development Environment](#setting-up-your-development-environment)
   - [Project Structure](#project-structure)
3. [Development Workflow](#development-workflow)
   - [Branching Strategy](#branching-strategy)
   - [Commit Guidelines](#commit-guidelines)
   - [Pull Request Process](#pull-request-process)
4. [Coding Standards](#coding-standards)
   - [C++ Style Guide](#c-style-guide)
   - [Python Style Guide](#python-style-guide)
   - [SQL Style Guide](#sql-style-guide)
5. [Testing](#testing)
   - [Writing Tests](#writing-tests)
   - [Running Tests](#running-tests)
6. [Documentation](#documentation)
7. [Issue Reporting](#issue-reporting)
8. [Feature Requests](#feature-requests)
9. [Community](#community)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. We expect all contributors to be respectful, inclusive, and considerate of others.

- Be respectful and inclusive: We welcome contributions from people of all backgrounds and identities.
- Be collaborative: Work together effectively, consider different perspectives, and be open to constructive criticism.
- Be mindful of your language: Use inclusive language and avoid offensive terms or comments.
- Focus on the issue, not the person: Discuss ideas and code, not individuals.

## Getting Started

### Setting Up Your Development Environment

1. **Fork the repository**:
   - Click the "Fork" button at the top right of the repository page.

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/medisys.git
   cd medisys
   ```

3. **Set up the upstream remote**:
   ```bash
   git remote add upstream https://github.com/Mazharuddin-Mohammed/MediSys.git
   ```

4. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

7. **Set up the database**:
   ```bash
   ./scripts/setup_db.sh
   ```

8. **Build the C++ backend**:
   ```bash
   ./scripts/build.sh
   ```

### Project Structure

The MediSys project is organized as follows:

```
MediSys/
├── build/                  # Build artifacts (generated)
├── cmake/                  # CMake modules and configuration
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── src/                    # Source code
│   ├── backend/            # C++ backend code
│   │   ├── bindings/       # Python bindings
│   │   ├── core/           # Core functionality
│   │   │   ├── database/   # Database management
│   │   │   ├── models/     # Data models
│   │   │   └── services/   # Business logic services
│   │   └── utils/          # Utility functions
│   └── frontend/           # Frontend code
│       └── python/         # Python GUI code
│           ├── gui/        # GUI components
│           └── resources/  # Resources (images, styles, etc.)
├── tests/                  # Test code
│   ├── backend_tests/      # C++ backend tests
│   └── frontend_tests/     # Python frontend tests
├── .gitignore              # Git ignore file
├── CMakeLists.txt          # Main CMake configuration
├── CONTRIBUTING.md         # Contributing guidelines (this file)
├── LICENSE.md              # License information
├── README.md               # Project overview
└── requirements.txt        # Python dependencies
```

## Development Workflow

### Branching Strategy

We follow a simplified Git workflow:

1. **Main Branch**: The `main` branch contains the stable version of the code.
2. **Feature Branches**: Create a new branch for each feature or bugfix.

When starting work on a new feature or bugfix:

```bash
# Ensure you're on the main branch and up-to-date
git checkout main
git pull upstream main

# Create a new branch for your feature
git checkout -b feature/your-feature-name
```

### Commit Guidelines

We follow these commit message guidelines:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable prefix:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `style:` for formatting changes
  - `refactor:` for code refactoring
  - `test:` for adding or modifying tests
  - `chore:` for maintenance tasks

Example:
```
feat: Add patient photo management functionality

- Add photo upload and display in patient form
- Implement placeholder images for patients without photos
- Store photos as base64 encoded strings in the database

Closes #123
```

### Pull Request Process

1. **Update your branch**: Before submitting a pull request, rebase your branch on the latest main:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Push your branch**:
   ```bash
   git push origin your-feature-branch
   ```

3. **Create a Pull Request**: Go to the repository on GitHub and create a new pull request.

4. **Pull Request Template**: Fill out the pull request template with:
   - A clear description of the changes
   - Any related issues
   - Screenshots if applicable
   - Testing steps

5. **Code Review**: Address any feedback from code reviews.

6. **Merge**: Once approved, your pull request will be merged.

## Coding Standards

### C++ Style Guide

We follow the Google C++ Style Guide with some modifications:

- Use 4 spaces for indentation (not tabs)
- Use camelCase for variable and function names
- Use PascalCase for class names
- Use snake_case for file names
- Include descriptive comments for complex logic
- Write meaningful variable and function names

### Python Style Guide

We follow PEP 8 with some modifications:

- Use 4 spaces for indentation (not tabs)
- Maximum line length of 100 characters
- Use snake_case for variable and function names
- Use PascalCase for class names
- Use docstrings for all functions, classes, and modules
- Include type hints where appropriate

### SQL Style Guide

For SQL code:

- Use uppercase for SQL keywords (SELECT, INSERT, etc.)
- Use snake_case for table and column names
- Include comments for complex queries
- Format queries for readability with appropriate line breaks and indentation

## Testing

### Writing Tests

- **Backend Tests**: Use Catch2 for C++ tests
- **Frontend Tests**: Use pytest for Python tests
- Write unit tests for all new functionality
- Aim for high test coverage, especially for critical components

### Running Tests

To run the backend tests:
```bash
cd build
ctest
```

To run the frontend tests:
```bash
pytest tests/frontend_tests
```

## Documentation

Good documentation is crucial for the project:

- Add docstrings to all Python functions, classes, and modules
- Document C++ functions and classes with clear comments
- Update the README.md when adding major features
- Create or update user guides in the docs/ directory
- Add comments explaining complex logic

## Issue Reporting

When reporting issues:

1. Check if the issue already exists
2. Use the issue template
3. Include detailed steps to reproduce
4. Include relevant information:
   - Operating system
   - Python version
   - C++ compiler version
   - PostgreSQL version
   - Error messages
   - Screenshots if applicable

## Feature Requests

For feature requests:

1. Check if the feature has already been requested
2. Use the feature request template
3. Clearly describe the feature and its benefits
4. Consider including mockups or examples

## Community

Join our community:

- Participate in discussions
- Help answer questions
- Review pull requests
- Suggest improvements

Thank you for contributing to MediSys!

---

## License

By contributing to MediSys, you agree that your contributions will be licensed under the project's MIT license.

## Contact

If you have any questions, feel free to reach out to the project maintainer:
- Mazharuddin Mohammed
