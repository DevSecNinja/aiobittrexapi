"""Interacts with the Bittrex API."""
import asyncio
from asyncio import AbstractEventLoop
from typing import Dict, Optional

import aiohttp
from asyncio_throttle import Throttler

from .const import API_URL
from .errors import (
    BittrexApiError,
    BittrexInvalidAuthentication,
    BittrexResponseError,
    BittrexRestError,
)

from .utils import compose_url, get_digest, get_nonce, get_signature


class Bittrex:
    """Bittrex API Class."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        throttler: Throttler = None,
        loop: AbstractEventLoop = None,
        session: aiohttp.ClientSession = None,
        timeout: int = 20,
    ):
        self._api_url = API_URL
        self.api_key = api_key or ""
        self.api_secret = api_secret or ""

        self._loop = loop or asyncio.get_event_loop()
        self._throttler = throttler or self._init_throttler()
        self._session = session or self._init_session(timeout)

    @staticmethod
    def _init_throttler() -> Throttler:
        """Initialize throttler."""
        return Throttler(rate_limit=60, period=60.0)

    def _init_session(self, timeout: int) -> aiohttp.ClientSession:
        """Initialize session."""
        return aiohttp.ClientSession(
            loop=self._loop,
            headers={"Content-Type": "application/json"},
            timeout=aiohttp.ClientTimeout(total=timeout),
        )

    async def close(self, delay: float = 0.250):
        """Graceful shutdown."""
        await asyncio.sleep(delay)
        await self._session.close()

    async def _request(self, path, options=None):
        """Create the Bittrex request."""
        url = compose_url(self._api_url, path)
        content = ""  # Currently no function requires a body
        content_hash = get_digest(content)
        nonce = str(get_nonce())
        signature = get_signature(
            "".join([nonce, url, "GET", content_hash]),
            self.api_secret,
        )
        headers = {
            "Api-Timestamp": str(nonce),
            "Api-Key": self.api_key,
            "Content-Type": "application/json",
            "Api-Content-Hash": content_hash,
            "Api-Signature": signature,
        }

        async with self._throttler:
            async with self._session.get(url=url, headers=headers) as response:
                return await self._handle_response(response)

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict:
        """Handle the response."""
        try:
            response_json = await response.json()
        except aiohttp.ContentTypeError:
            raise BittrexResponseError(response.status, await response.text())
        except Exception as e:
            raise BittrexRestError("Unknown exception: %s", e)
        else:
            self._raise_if_error(response_json)
            return response_json

    @staticmethod
    def _raise_if_error(response_json: Dict) -> None:
        """Raise if response is not expected."""
        if not response_json:
            return None
        if "code" in response_json:
            if response_json["code"] == "APIKEY_INVALID":
                raise BittrexInvalidAuthentication
            else:
                raise BittrexApiError(response_json.get("message"))

    async def get_markets(self):
        """Get the open and available trading markets at Bittrex."""
        return await self._request(path="markets")

    async def get_tickers(self, symbol: Optional[list] = None):
        """Get the market tickers from Bittrex."""
        tickers = await self._request(path="markets/tickers")
        results = {}

        if not symbol:
            symbol = []
            for ticker in tickers:
                symbol.append(ticker["symbol"])

        for sym in symbol:
            if sym not in results:
                results[sym] = {}
                details = next(item for item in tickers if item["symbol"] == sym)
                results[sym].update(details)

        return results

    async def get_balances(self, symbol: Optional[list] = None):
        """Get account balances from Bittrex."""
        balances = await self._request(path="balances")
        results = {}

        if not symbol:
            symbol = []
            for balance in balances:
                symbol.append(balance["currencySymbol"])

        for sym in symbol:
            if sym not in results:
                results[sym] = {}
                details = next(
                    item for item in balances if item["currencySymbol"] == sym
                )
                results[sym].update(details)

        return results

    async def get_account(self):
        """Get account info."""
        return await self._request(path="account")

    async def get_open_orders(self):
        """Get open orders."""
        return await self._request(path="orders/open")

    async def get_closed_orders(self):
        """Get closed orders."""
        return await self._request(path="orders/closed")
