# Contributing to Veria Python SDK

Thank you for your interest in contributing to the Veria SDK! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/veria-python.git`
3. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
4. Install dev dependencies: `pip install -e ".[dev]"`
5. Create a branch: `git checkout -b feature/your-feature-name`

## Development

### Testing

```bash
pytest
```

### Code Style

- We follow PEP 8 guidelines
- Use type hints for all public APIs
- Use meaningful variable and function names
- Add docstrings for public functions and classes

### Linting

```bash
ruff check .
mypy src/
```

## Pull Request Process

1. Ensure your code passes all tests and linting
2. Update documentation if needed
3. Add a clear description of your changes
4. Reference any related issues

## Reporting Issues

When reporting issues, please include:

- SDK version (`pip show veria`)
- Python version
- Operating system
- Minimal reproduction steps
- Expected vs actual behavior

## Questions?

- Open a GitHub issue for bugs or feature requests
- Email support@veria.cc for general questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
