#!/usr/bin/python3
"""Services package initialization."""
from app.services.facade import facade

# Expose the single instantiated facade to the rest of the application.
# This ensures a clean, unified point of access for all business logic operations.
__all__ = [
    'facade'
]
