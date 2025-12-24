# Veria SDK for Python

[![PyPI version](https://img.shields.io/pypi/v/veria.svg)](https://pypi.org/project/veria/)
[![PyPI downloads](https://img.shields.io/pypi/dm/veria.svg)](https://pypi.org/project/veria/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python versions](https://img.shields.io/pypi/pyversions/veria.svg)](https://pypi.org/project/veria/)

Official SDK for the [Veria Compliance API](https://veria.cc) - screen wallet addresses for sanctions, PEP, and AML compliance.

## Installation

```bash
pip install veria
```

## Quick Start

```python
from veria import VeriaClient

client = VeriaClient(api_key="veria_live_xxxxxxxxxxxx")  # Get yours at https://veria.cc/choose-plan

# Screen an address
result = client.screen("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")

print(f"Risk: {result.risk}, Score: {result.score}")

# Check if should block
if result.should_block():
    print("Transaction blocked for compliance")
```

## Features

- Full type hints for IDE support
- Supports Ethereum addresses, ENS names, Solana addresses, and IBANs
- Configurable timeout and base URL
- Proper error handling with typed exceptions
- Context manager support for automatic cleanup

## API

### `VeriaClient(api_key, base_url=None, timeout=30)`

Create a new Veria client.

```python
client = VeriaClient(
    api_key="veria_live_xxx",           # Required: Your API key
    base_url="https://api.veria.cc",    # Optional: API base URL
    timeout=30,                          # Optional: Request timeout in seconds
)
```

### `client.screen(input)`

Screen an address for compliance risks.

```python
result = client.screen("vitalik.eth")
```

**Returns `ScreenResult`:**

```python
ScreenResult(
    score=15,                    # Risk score 0-100
    risk="low",                  # "low" | "medium" | "high" | "critical"
    chain="ethereum",            # Detected blockchain
    resolved="0x742d35...",      # Resolved address
    latency_ms=45,               # Processing time
    details=ScreenDetails(
        sanctions_hit=False,     # On sanctions list?
        pep_hit=False,           # Politically exposed person?
        watchlist_hit=False,     # On any watchlist?
        checked_lists=["OFAC SDN", "UN Consolidated", ...],
        address_type="wallet",   # wallet | contract | exchange | mixer
    ),
)
```

### `result.should_block()`

Helper to determine if an address should be blocked.

```python
result = client.screen(address)
if result.should_block():
    # Block the transaction
    pass
```

Returns `True` if:
- `sanctions_hit` is `True`, OR
- `risk` is `"high"` or `"critical"`

## Risk Levels

| Level | Score | Recommended Action |
|-------|-------|-------------------|
| low | 0-29 | Proceed |
| medium | 30-59 | Review |
| high | 60-79 | Block recommended |
| critical | 80-100 | Block required |

## Error Handling

```python
from veria import VeriaClient, VeriaError

try:
    result = client.screen(address)
except VeriaError as e:
    print(f"Error: {e.code} - {e}")

    # Handle specific error codes
    if e.code == "INVALID_API_KEY":
        # Re-authenticate
        pass
    elif e.code == "RATE_LIMIT_EXCEEDED":
        # Back off and retry
        pass
    elif e.code == "TIMEOUT":
        # Retry with longer timeout
        pass
```

## Context Manager

The client supports context manager protocol for automatic cleanup:

```python
with VeriaClient(api_key="veria_live_xxx") as client:
    result = client.screen(address)
# Session automatically closed
```

## Usage Examples

### Pre-transaction screening

```python
from veria import VeriaClient, VeriaError

client = VeriaClient(api_key="veria_live_xxx")

def safe_transfer(to_address: str, amount: float) -> bool:
    """Screen recipient before transfer."""
    result = client.screen(to_address)

    if result.should_block():
        raise ValueError(
            f"Recipient blocked: {result.risk} risk, "
            f"sanctions: {result.details.sanctions_hit}"
        )

    # Proceed with transfer
    return True
```

### Batch screening

```python
addresses = [
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "0x8576acc5c05d6ce88f4e49bf65bdf0c62f91353c",
    "vitalik.eth",
]

for address in addresses:
    try:
        result = client.screen(address)
        status = "BLOCKED" if result.should_block() else "OK"
        print(f"{address[:12]}... {status} (score: {result.score})")
    except VeriaError as e:
        print(f"{address[:12]}... ERROR: {e.code}")
```

### Django middleware example

```python
from veria import VeriaClient
from django.conf import settings

client = VeriaClient(api_key=settings.VERIA_API_KEY)

class ComplianceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        wallet = request.headers.get("X-Wallet-Address")
        if wallet:
            result = client.screen(wallet)
            if result.should_block():
                return JsonResponse(
                    {"error": "Wallet blocked for compliance"},
                    status=403
                )
        return self.get_response(request)
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Resources

- [Documentation](https://veria.cc/protocol/docs)
- [API Reference](https://veria.cc/protocol/docs/reference)
- [Get API Key](https://veria.cc/choose-plan)
- [GitHub](https://github.com/Veria-Protocol/veria-python)

## License

MIT
