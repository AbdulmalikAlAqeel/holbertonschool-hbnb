#!/usr/bin/python3
"""Persistence package initialization."""
from app.persistence.repository import InMemoryRepository

# Explicitly defining the public interface of the persistence package.
# This makes importing the repository cleaner across the application.
__all__ = [
    'InMemoryRepository'
]
