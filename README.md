# Local AI Platform

A local AI platform for personal use.

The project provides the foundation for building and running a personal AI assistant with local language models, context and memory management, and tool execution. It is designed to be modular and extensible, allowing additional capabilities and services to be integrated over time.

## Documentation

- [Commit Message Convention](docs/commit-convention.md)
- [Branch Strategy](docs/branch-strategy.md)
- [Logging Documentation](docs/logging.md).

## Development

The project uses [uv](https://docs.astral.sh/uv/) for Python project and dependency management, [Code Style](docs/code-style.md) for coding conventions.

## Logging

The application uses Python's standard `logging` module
for user-facing messages, application diagnostics, and debugging.

Console output provides simplified messages, while detailed logs
are written to a rotating log file.

For configuration details and usage guidelines, see
[Logging Documentation](docs/logging.md).