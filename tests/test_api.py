import asyncio
import pytest
from typing import Optional

from aiobittrexapi import Bittrex
from aiobittrexapi.errors import (
    BittrexApiError,
    BittrexResponseError,
    BittrexInvalidAuthentication,
)

API_KEY = ""
API_SECRET = ""


@pytest.mark.asyncio
async def test_get_markets(
    api_key: Optional[str] = None, api_secret: Optional[str] = None
):
    """
    Test gathering the markets
    """

    if api_key and api_secret:
        api = Bittrex(api_key, api_secret)
    else:
        api = Bittrex()

    try:
        # Get the active markets from Bittrex - works without secret & key
        testEntries = []
        markets = await api.get_markets()
        for market in markets:
            if market["symbol"] == "BTC-USDT":
                testEntries.append(market)

        assert testEntries[0]["symbol"] == "BTC-USDT"
        assert testEntries[0]["baseCurrencySymbol"] == "BTC"
        assert testEntries[0]["quoteCurrencySymbol"] == "USDT"
        assert testEntries[0]["status"] == "ONLINE"
        assert testEntries[0]["createdAt"] == "2015-12-11T06:31:40.633Z"
    except BittrexApiError as e:
        print(e)
    except BittrexResponseError as e:
        print("Invalid response:", e)
    finally:
        await api.close()


@pytest.mark.asyncio
async def test_get_tickers(
    api_key: Optional[str] = None, api_secret: Optional[str] = None
):
    """
    Test gathering the market tickers
    """

    if api_key and api_secret:
        api = Bittrex(api_key, api_secret)
    else:
        api = Bittrex()

    try:
        # Get the active markets from Bittrex - works without secret & key
        testEntries = []
        tickers = await api.get_tickers()
        for ticker in tickers:
            if ticker["symbol"] == "BTC-USDT":
                testEntries.append(ticker)

        assert testEntries[0]["symbol"] == "BTC-USDT"
        assert testEntries[0]["lastTradeRate"]
        assert testEntries[0]["bidRate"]
        assert testEntries[0]["askRate"]
    except BittrexApiError as e:
        print(e)
    except BittrexResponseError as e:
        print("Invalid response:", e)
    finally:
        await api.close()


@pytest.mark.asyncio
async def test_get_account(
    api_key: Optional[str] = None, api_secret: Optional[str] = None
):
    """
    Test gathering account info
    """

    if api_key and api_secret:
        api = Bittrex(api_key, api_secret)
    else:
        api = Bittrex()

    try:
        await api.get_account()
        assert False
    except BittrexInvalidAuthentication:
        assert True
    finally:
        await api.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    if API_KEY and API_SECRET:
        loop.run_until_complete(test_get_markets(API_KEY, API_SECRET))
        loop.run_until_complete(test_get_account(API_KEY, API_SECRET))
        loop.run_until_complete(test_get_tickers(API_KEY, API_SECRET))
    else:
        loop.run_until_complete(test_get_markets())
        loop.run_until_complete(test_get_account())
        loop.run_until_complete(test_get_tickers())
