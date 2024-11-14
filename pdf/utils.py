"""
Utility functions for PDF XBlock
"""
from typing import Optional
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

GOTENBERG_HOST = getattr(settings, "GOTENBERG_HOST", None)
GOTENBERG_CONVERSION_URL = f"{GOTENBERG_HOST}/forms/libreoffice/convert"


def convert_to_pdf(doc_url: str, pdf_path: str) -> Optional[str]:
    """
    Uses the Gotenberg service to convert the document at `doc_url` to a PDF file.

    Parameters:
        doc_url (str): The path or URL to the document to be converted.
        pdf_path (str): The path where the converted PDF file will be stored.

    Returns:
        str | None: Return None if conversation fails, or returns the PDF url.
    """
    source_url = urlparse(doc_url)
    filename = source_url.path.split('/')[-1]
    source_doc_response = requests.get(doc_url, timeout=(10, 120))

    pdf_response = requests.post(GOTENBERG_CONVERSION_URL, files={
        'file': (filename, source_doc_response.content)
    }, timeout=(2, 120))
    if pdf_response.status_code != 200:
        return None
    file_path = default_storage.save(pdf_path, ContentFile(pdf_response.content))
    return default_storage.url(file_path)


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
    return getattr(settings, 'PDFXBLOCK_DISABLE_ALL_DOWNLOAD', False)


def _(text):
    """
    Dummy `gettext` replacement to make string extraction tools scrape strings marked for translation
    """
    return text


def ngettext_fallback(text_singular, text_plural, number):
    """
    Dummy `ngettext` replacement to make string extraction tools scrape strings marked for translation
    """
    if number == 1:
        return text_singular
    return text_plural


class DummyTranslationService:
    """
    Dummy drop-in replacement for i18n XBlock service
    """
    gettext = _
    ngettext = ngettext_fallback
