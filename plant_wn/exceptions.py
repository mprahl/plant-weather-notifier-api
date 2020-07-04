# SPDX-License-Identifier: GPL-3.0-or-later


class AppError(Exception):
    """A generic exception that all other exceptions are based on."""


class ValidationError(AppError):
    """An exception for invalid input."""
