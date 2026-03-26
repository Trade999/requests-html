# requests_html/__init__.py

"""
Requests-HTML: HTML Parsing for Humans (Modified Version)
"""

# Import ny zavatra rehetra avy amin'ny core module
from .core import (
    HTMLSession,
    AsyncHTMLSession,
    HTML,
    HTMLResponse,
    Element,
    BaseParser,
    user_agent,
    MaxRetries,
    AsyncRequests,
    AsyncResponse,
)

arequests = AsyncRequests()

import requests as _requests

# Re-export ny requests module
requests = _requests

# Version (azonao ovaina)
__version__ = "0.1.0"

# Izay rehetra azo alaina amin'ny "from requests_html import *"
__all__ = [
    'HTMLSession',
    'AsyncHTMLSession',
    'HTML',
    'HTMLResponse',
    'Element',
    'BaseParser',
    'user_agent',
    'MaxRetries',
    'requests',
    "arequests",
    "AsyncRequests",
    "AsyncResponse"
]