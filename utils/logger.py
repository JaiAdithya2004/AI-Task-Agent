"""
Logger Utility Module

This module provides logging functionality for the AI Agent project.
It sets up a comprehensive logging system with different levels and
formatters for better debugging and monitoring.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logger(
    name: str = "ai_agent",
    level: str = None,
    log_file: str = None
) -> logging.Logger:
    """
    Set up and configure the logger for the AI Agent.
    
    Args:
        name: Logger name (default: "ai_agent")
        level: Logging level (default: from environment or INFO)
        log_file: Path to log file (default: logs/ai_agent.log)
    
    Returns:
        Configured logger instance
    """
    # Get log level from environment or use default
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level, logging.INFO)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file is specified or default)
    if log_file is None:
        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        log_file = logs_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # File gets all levels
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"Logging to file: {log_file}")
    except Exception as e:
        logger.warning(f"Could not create log file {log_file}: {e}")
    
    # Log initial setup
    logger.info(f"Logger '{name}' initialized with level: {level}")
    
    return logger

def get_logger(name: str = "ai_agent") -> logging.Logger:
    """
    Get an existing logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

def log_function_call(func):
    """
    Decorator to log function calls with parameters and return values.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        logger = get_logger()
        logger.debug(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised exception: {e}")
            raise
    
    return wrapper

def log_execution_time(func):
    """
    Decorator to log function execution time.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    import time
    
    def wrapper(*args, **kwargs):
        logger = get_logger()
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.3f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.3f} seconds: {e}")
            raise
    
    return wrapper

# Example usage and testing
if __name__ == "__main__":
    # Test the logger setup
    test_logger = setup_logger("test_logger", "DEBUG")
    
    test_logger.debug("This is a debug message")
    test_logger.info("This is an info message")
    test_logger.warning("This is a warning message")
    test_logger.error("This is an error message")
    
    print("Logger test completed. Check the logs directory for the log file.")
