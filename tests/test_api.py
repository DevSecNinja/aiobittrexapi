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
    api_key: Optional[str] = API_KEY, api_secret: Optional[str] = API_SECRET
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
    api_key: Optional[str] = API_KEY, api_secret: Optional[str] = API_SECRET
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
        tickers = await api.get_tickers()

        assert tickers["BTC-USDT"]["symbol"] == "BTC-USDT"
        assert tickers["BTC-USDT"]["lastTradeRate"]
        assert tickers["BTC-USDT"]["bidRate"]
        assert tickers["BTC-USDT"]["askRate"]
    except BittrexApiError as e:
        print(e)
    except BittrexResponseError as e:
        print("Invalid response:", e)
    finally:
        await api.close()


@pytest.mark.asyncio
async def test_get_two_tickers(
    api_key: Optional[str] = API_KEY, api_secret: Optional[str] = API_SECRET
):
    """
    Test gathering two of the market tickers
    """

    if api_key and api_secret:
        api = Bittrex(api_key, api_secret)
    else:
        api = Bittrex()

    try:
        # Get the active markets from Bittrex - works without secret & key
        symbols = ["BTC-USDT", "DGB-USDT"]
        testEntries = await api.get_tickers(symbol=symbols)

        assert testEntries["BTC-USDT"]["symbol"] == "BTC-USDT"
        assert testEntries["BTC-USDT"]["lastTradeRate"]
        assert testEntries["BTC-USDT"]["bidRate"]
        assert testEntries["BTC-USDT"]["askRate"]

        assert testEntries["DGB-USDT"]["symbol"] == "DGB-USDT"
        assert testEntries["DGB-USDT"]["lastTradeRate"]
        assert testEntries["DGB-USDT"]["bidRate"]
        assert testEntries["DGB-USDT"]["askRate"]
    except BittrexApiError as e:
        print(e)
    except BittrexResponseError as e:
        print("Invalid response:", e)
    finally:
        await api.close()


@pytest.mark.asyncio
async def test_get_account(
    api_key: Optional[str] = API_KEY, api_secret: Optional[str] = API_SECRET
):
    """
    Test gathering account info. Exception must be thrown without API details
    """

    if api_key and api_secret:
        api = Bittrex(api_key, api_secret)

        try:
            testEntries = await api.get_account()
            assert testEntries["accountId"]
        except BittrexInvalidAuthentication:
            print("Invalid authentication while API_KEY and API_SECRET were provided!")
            assert False
        finally:
            await api.close()
    else:
        api = Bittrex()

        try:
            await api.get_account()
            assert False
        except BittrexInvalidAuthentication:
            assert True
        finally:
            await api.close()


@pytest.mark.asyncio
async def test_get_open_orders(
    api_key: Optional[str] = API_KEY, api_secret: Optional[str] = API_SECRET
):
    """
    Test gathering open orders. Exception must be thrown without API details
    """

    if api_key and api_secret:
        api = Bittrex(api_key, api_secret)

        try:
            testEntries = await api.get_open_orders()
            assert testEntries[0]["id"]
            assert testEntries[0]["marketSymbol"]
            assert testEntries[0]["direction"]
            assert testEntries[0]["type"]
            assert testEntries[0]["quantity"]
        except BittrexInvalidAuthentication:
            print("Invalid authentication while API_KEY and API_SECRET were provided!")
            assert False
        finally:
            await api.close()
    else:
        api = Bittrex()

        try:
            await api.get_open_orders()
            assert False
        except BittrexInvalidAuthentication:
            assert True
        finally:
            await api.close()


@pytest.mark.asyncio
async def test_get_closed_orders(
    api_key: Optional[str] = API_KEY, api_secret: Optional[str] = API_SECRET
):
    """
    Test gathering closed orders. Exception must be thrown without API details
    """

    if api_key and api_secret:
        api = Bittrex(api_key, api_secret)

        try:
            testEntries = await api.get_closed_orders()
            assert testEntries[0]["id"]
            assert testEntries[0]["marketSymbol"]
            assert testEntries[0]["direction"]
            assert testEntries[0]["type"]
            assert testEntries[0]["quantity"]
        except BittrexInvalidAuthentication:
            print("Invalid authentication while API_KEY and API_SECRET were provided!")
            assert False
        finally:
            await api.close()
    else:
        api = Bittrex()

        try:
            await api.get_closed_orders()
            assert False
        except BittrexInvalidAuthentication:
            assert True
        finally:
            await api.close()
