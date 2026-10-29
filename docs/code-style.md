# Code Style Guide

## Overview

This document defines the coding conventions used in Local AI Platform.

The project follows the Google Python Style Guide for docstrings and uses
PEP 8 conventions for Python code, with project-specific tooling and
configuration defined in `pyproject.toml`.

**References:**
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)

## Python Code

- Use four spaces for indentation.
- Use `snake_case` for functions, methods, variables, and modules.
- Use `PascalCase` for classes.
- Use `UPPER_SNAKE_CASE` for constants.
- Add type annotations to public APIs and other code where they improve
  correctness and readability.
- Follow the line length and formatting configuration in `pyproject.toml`.
- Use Ruff for linting and formatting.
- Use mypy for static type checking.

## Docstrings

- Write docstrings in English.
- Follow the Google Python Style Guide docstring conventions.
- Use triple double quotes (`"""`).
- Start with a concise summary ending with a period.
- Document public modules, classes, and functions.
- Add `Args`, `Returns`, and `Raises` sections when they clarify the API.
- Do not repeat type information already expressed by type annotations
  unless it improves clarity.
- Document behavior and side effects rather than implementation details.
- Avoid docstrings that merely repeat an obvious function or method name.

## Comments

- Explain why a non-obvious decision was made, not merely what the code does.
- Keep comments concise and relevant.
- Update comments when the associated behavior changes.

## Consistency

- Do not mix Google-style and NumPy-style docstrings.
- Prefer the project's existing conventions when modifying existing code.
- Update this document when project-wide conventions change.
