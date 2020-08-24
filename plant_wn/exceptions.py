# SPDX-License-Identifier: GPL-3.0-or-later


class AppError(Exception):
    """A generic exception that all other exceptions are based on."""


class ConfigError(Exception):
    """An exception for invalid configuration."""


class ValidationError(AppError):
    """An exception for invalid input."""


class WeatherAPIError(AppError):
    """An exception when there is an error in the weather API."""
