#!/usr/bin/python3
"""Application configuration module."""


class Config:
    """Base configuration class."""

    SECRET_KEY = "default_secret_key"
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration class."""

    DEBUG = True
