## Logging

The Local AI Platform uses Python's built-in `logging` module to provide a centralized and consistent logging system for application development, debugging, and maintenance.

The logging system is used for both user-facing application messages and developer diagnostics. Use logging instead of `print()` for application output.

### Configuration

All logging-related configuration is managed in:

`src/local_ai_platform/logging_config.py`

This module defines log formats, handlers, output destinations, log levels, and file rotation settings.

The application currently uses two handlers:

- **Console handler** — displays simplified messages at the `INFO` level and above.
- **File handler** — records detailed logs, including timestamps, logger names, source line numbers, function names, and exception tracebacks when available.

The file handler uses Python's `RotatingFileHandler`, with a maximum file size of 5 MB and up to three backup files.

Logging is initialized once during application startup by calling `configure_logging()`.

### Log Levels

The system uses Python's standard logging levels:

| Level | Purpose |
|---|---|
| `DEBUG` | Detailed diagnostic information for developers, including intermediate processing steps and internal state. |
| `INFO` | Normal application events, status updates, completed operations, and useful information for users. |
| `WARNING` | Unexpected situations or potential problems that do not prevent the application from continuing. |
| `ERROR` | An operation failed and could not complete as expected. |
| `CRITICAL` | A severe failure that may prevent the application from continuing. |

Use the lowest appropriate level that communicates the significance of an event. Avoid logging routine events as warnings or errors.

### Logger Naming

Use the centralized `get_logger()` function from `logging_config.py` to obtain a logger for a specific application component.

Logger names are built from the application's `APP_NAME` and the component path. This provides consistent, hierarchical logger names regardless of how an individual module is executed.

For example:

```python
from local_ai_platform.logging_config import get_logger

logger = get_logger("models.providers.ollama")
```

This produces the logger name:

`local_ai_platform.models.providers.ollama`

Always use `get_logger()` for application loggers instead of creating them directly with `logging.getLogger()`. Provide a meaningful component name that reflects the relevant area of responsibility. Nested component names can be separated with dots.

### Usage Guidelines

- **`logger.debug()`** — use for developer-oriented diagnostics, intermediate steps, detailed state, and troubleshooting information. Keep these messages out of normal console output.
- **`logger.info()`** — use for normal application events, progress updates, operation results, and useful status messages.
- **`logger.warning()`** — use when something unexpected or potentially problematic occurs, but the application can continue.
- **`logger.error()`** — use when an operation fails and requires attention or recovery.
- **`logger.critical()`** — use for severe failures that threaten the application's ability to continue.
- **`logger.exception()`** — use inside an exception handler when the exception traceback is useful for diagnosing a failure. It logs at `ERROR` level by default.

Prefer clear, concise messages that explain what happened. Include relevant context when it helps diagnose a problem, but avoid logging secrets, credentials, or sensitive data.

### Example

```python
from local_ai_platform.logging_config import get_logger

logger = get_logger("models.providers.ollama")

logger.info("Connecting to Ollama")
logger.warning("GPU acceleration is unavailable")
logger.debug("Loading model configuration")

try:
    # Perform an operation that may fail.
    ...
except Exception:
    logger.exception("Failed to load model")
```

Call `configure_logging()` once during application startup before emitting application logs.

### Implementation Notes

The logging system relies on Python's standard library and does not require an external logging package. Logging configuration is currently maintained separately from the rest of the application configuration and may be integrated into a shared configuration system in the future.