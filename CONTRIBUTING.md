# Contributing to iTrip

Thank you for your interest in contributing to iTrip! We welcome contributions from the community. Please read this guide to understand how to contribute effectively.

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to kemperdesignservices@gmail.com.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/iTrip.git
   cd iTrip
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/kemperdesign/iTrip.git
   ```

## Development Setup

Follow the [DEVELOPMENT.md](./DEVELOPMENT.md) guide to set up your local development environment.

## Making Changes

### Branch Naming
Use descriptive branch names:
- Feature: `feature/description-of-feature`
- Bug fix: `fix/description-of-bug`
- Documentation: `docs/description`
- Refactor: `refactor/description`

```bash
git checkout -b feature/quote-export
```

### Commit Messages
Write clear, descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Be specific about what changed
- Keep the first line under 50 characters
- Add body with details if needed

```
Add quote export to PDF functionality

- Implement PDF generation using reportlab
- Add export button to quote detail view
- Include company branding in exported PDF
```

### Code Style

**Backend (Python):**
```bash
# Format code
black .

# Check types
mypy app/

# Lint
flake8 .

# Run tests
pytest tests/ -v
```

**Frontend (TypeScript/React):**
```bash
# Format and lint
npm run lint
npm run format

# Type check
npm run type-check

# Run tests
npm test
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage for critical paths

```bash
# Backend
cd backend
pytest tests/ --cov=app

# Frontend
cd frontend
npm test -- --coverage
```

## Submitting Changes

### Pull Request Process

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your changes**:
   ```bash
   git push origin feature/your-feature
   ```

3. **Create a Pull Request**:
   - Use a clear, descriptive title
   - Reference any related issues (#123)
   - Describe what the PR does and why
   - Include screenshots for UI changes

4. **PR Template**:
   ```
   ## Description
   Brief description of changes
   
   ## Related Issues
   Closes #123
   
   ## Changes Made
   - Change 1
   - Change 2
   
   ## Testing
   How to test the changes
   
   ## Screenshots
   If applicable
   ```

### Review Process

- Maintainers will review your PR
- Address feedback and make requested changes
- All tests must pass
- At least one maintainer approval required

## Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows project style guidelines
- [ ] Tests pass locally: `npm test`, `pytest tests/`
- [ ] Code is formatted: `black .`, `npm run format`
- [ ] Types check: `mypy app/`, `npm run type-check`
- [ ] No console errors or warnings
- [ ] Commit messages are clear and descriptive
- [ ] PR description clearly explains changes
- [ ] Related issues are referenced
- [ ] Documentation is updated if needed
- [ ] CHANGELOG.md is updated (if applicable)

## Types of Contributions Welcome

### Bug Reports
- Use the bug report template
- Include steps to reproduce
- Provide expected vs actual behavior
- Include screenshots/logs if possible

### Feature Requests
- Use the feature request template
- Explain the problem and solution
- Include use cases
- Provide mockups/examples if helpful

### Documentation
- Fix typos and improve clarity
- Add examples and guides
- Improve code comments
- Translate documentation

### Code Improvements
- Refactoring for clarity and performance
- Adding tests
- Fixing linting issues
- Optimizing database queries

## Review Guidelines

When reviewing PRs:
- Be respectful and constructive
- Focus on the code, not the person
- Suggest improvements, don't demand
- Approve when changes are good
- Request changes for issues

## Questions or Need Help?

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: kemperdesignservices@gmail.com
- **Documentation**: Check [docs/](./docs/) folder

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes for major contributions
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to iTrip! 🎉
