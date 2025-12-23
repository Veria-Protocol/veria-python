"""
Veria SDK - Official Python client for Veria Compliance API

Screen wallet addresses for sanctions, PEP, and AML compliance.

Example:
    >>> from veria import VeriaClient
    >>> client = VeriaClient(api_key="veria_live_xxx")
    >>> result = client.screen("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
    >>> print(f"Risk: {result.risk}, Score: {result.score}")
"""

from .client import VeriaClient, VeriaError, ScreenResult

__version__ = "0.1.0"
__all__ = ["VeriaClient", "VeriaError", "ScreenResult", "__version__"]
