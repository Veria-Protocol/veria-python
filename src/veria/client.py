"""
Veria SDK Client - Screen wallet addresses for compliance risks.
"""

from dataclasses import dataclass
from typing import Literal, Optional
import requests


class VeriaError(Exception):
    """Exception raised for Veria API errors."""

    def __init__(self, message: str, code: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.code = code
        self.status_code = status_code

    def __str__(self) -> str:
        return f"VeriaError({self.code}): {self.args[0]}"


@dataclass
class ScreenDetails:
    """Detailed screening results."""

    sanctions_hit: bool
    """True if address appears on a sanctions list."""

    pep_hit: bool
    """True if associated with a politically exposed person."""

    watchlist_hit: bool
    """True if on any watchlist."""

    checked_lists: list[str]
    """List of sanctions databases checked."""

    address_type: str
    """Type of address: wallet, contract, exchange, mixer, ens, iban."""


@dataclass
class ScreenResult:
    """Result from screening an address."""

    score: int
    """Risk score from 0-100."""

    risk: Literal["low", "medium", "high", "critical"]
    """Risk level based on score."""

    chain: str
    """Detected blockchain."""

    resolved: str
    """Resolved address (ENS names resolved to hex)."""

    latency_ms: int
    """Processing time in milliseconds."""

    details: ScreenDetails
    """Detailed screening results."""

    def should_block(self) -> bool:
        """
        Check if this address should be blocked.

        Returns True if:
        - sanctions_hit is True, OR
        - risk is 'high' or 'critical'
        """
        return self.details.sanctions_hit or self.risk in ("high", "critical")


class VeriaClient:
    """
    Official Python client for the Veria Compliance API.

    Args:
        api_key: Your Veria API key (get one at https://protocol.veria.cc)
        base_url: Base URL for the API (default: https://api.veria.cc)
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> client = VeriaClient(api_key="veria_live_xxx")
        >>> result = client.screen("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        >>> if result.should_block():
        ...     print("Address blocked for compliance")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.veria.cc",
        timeout: int = 30,
    ):
        if not api_key:
            raise VeriaError("API key is required", "MISSING_API_KEY")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )

    def screen(self, input: str) -> ScreenResult:
        """
        Screen a wallet address for compliance risks.

        Args:
            input: Ethereum address, ENS name, Solana address, or IBAN

        Returns:
            ScreenResult with risk score and details

        Raises:
            VeriaError: If the request fails or address is invalid

        Example:
            >>> result = client.screen("vitalik.eth")
            >>> print(f"Risk: {result.risk}, Score: {result.score}")
        """
        try:
            response = self._session.post(
                f"{self.base_url}/v1/screen",
                json={"input": input},
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise VeriaError("Request timed out", "TIMEOUT")
        except requests.exceptions.RequestException as e:
            raise VeriaError(str(e), "NETWORK_ERROR")

        if not response.ok:
            try:
                error_data = response.json()
                message = (
                    error_data.get("error", {}).get("message")
                    or error_data.get("message")
                    or f"Request failed with status {response.status_code}"
                )
                code = error_data.get("error", {}).get("code") or "REQUEST_FAILED"
            except Exception:
                message = f"Request failed with status {response.status_code}"
                code = "REQUEST_FAILED"

            raise VeriaError(message, code, response.status_code)

        data = response.json()

        details = ScreenDetails(
            sanctions_hit=data["details"]["sanctions_hit"],
            pep_hit=data["details"]["pep_hit"],
            watchlist_hit=data["details"]["watchlist_hit"],
            checked_lists=data["details"]["checked_lists"],
            address_type=data["details"]["address_type"],
        )

        return ScreenResult(
            score=data["score"],
            risk=data["risk"],
            chain=data["chain"],
            resolved=data["resolved"],
            latency_ms=data["latency_ms"],
            details=details,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
