"""
Utility functions for XBlock
"""

from django.conf import settings


def bool_from_str(str_value):
    """
    Converts string to boolean
    """
    return str_value.strip().lower() in [
        'true'
    ]


def is_all_download_disabled():
    """
    Check if all download is disabled or not
    """
    return bool_from_str(
        getattr(settings, 'PDFXBLOCK_DISABLE_ALL_DOWNLOAD', 'False')
    )
