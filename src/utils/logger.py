"""
Logging configuration module for AWS CloudWatch compatibility.
"""

import logging
import os
import sys


def setup_logging():
    """
    Configure logging for AWS CloudWatch compatibility with full stack traces.

    This function sets up structured logging that outputs to stdout,
    which is captured by AWS CloudWatch logs. It also configures
    uvicorn loggers to use the same format. Error-level logs and above
    will automatically include full stack traces when available.
    """
    # Get log level from environment variable, default to INFO
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Create formatter for structured logging with stack trace support
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Custom formatter class that always includes stack traces for errors
    class StackTraceFormatter(logging.Formatter):
        def format(self, record):
            # Always include exception info for ERROR level and above
            if record.levelno >= logging.ERROR and record.exc_info is None:
                # Get the current exception info if available
                record.exc_info = sys.exc_info()
                # If no exception is currently being handled, we'll still get
                # stack trace through the standard logging mechanism when
                # logging.exception() is used
            return super().format(record)

    # Use the custom formatter
    formatter = StackTraceFormatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler that outputs to stdout
    # CloudWatch captures stdout/stderr from containers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level, logging.INFO))
    console_handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(console_handler)

    # Configure uvicorn logging to use our formatter
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = []
    uvicorn_logger.addHandler(console_handler)
    uvicorn_logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Configure uvicorn access logger
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = []
    uvicorn_access_logger.addHandler(console_handler)
    uvicorn_access_logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Don't propagate to avoid duplicate logs
    uvicorn_logger.propagate = False
    uvicorn_access_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: The name of the logger (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
