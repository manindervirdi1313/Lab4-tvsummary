"""Exceptions raised by the tvsummary package."""


class TVSummaryError(Exception):
    """Base exception for expected application errors."""


class SettingsError(TVSummaryError):
    """Raised when application settings are missing or invalid."""


class DataSourceError(TVSummaryError):
    """Raised when retrieving or decoding show data fails."""


class DataValidationError(TVSummaryError):
    """Raised when retrieved data has an invalid structure."""


class ReportError(TVSummaryError):
    """Raised when writing a report fails."""
