import pytest
from typing import Optional

from aiobittrexapi import Bittrex
from aiobittrexapi.errors import (
    BittrexApiError,
    BittrexResponseError,
    BittrexInvalidAuthentication,
)

import logging

API_KEY = ""
API_SECRET = ""

if not API_KEY or not API_SECRET:
    logging.warning("As no API key and secret is provided, we cannot execute all tests")


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
        logging.error(e)
    except BittrexResponseError as e:
        logging.error("Invalid response:", e)
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
        logging.error(e)
    except BittrexResponseError as e:
        logging.error("Invalid response:", e)
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
        logging.error(e)
    except BittrexResponseError as e:
        logging.error("Invalid response:", e)
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
            logging.error(
                "Invalid authentication while API_KEY and API_SECRET were provided!"
            )
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
async def test_get_balances(
    api_key: Optional[str] = API_KEY, api_secret: Optional[str] = API_SECRET
):
    """
    Test gathering balances. Exception must be thrown without API details
    """

    if api_key and api_secret:
        api = Bittrex(api_key, api_secret)

        # Get the active markets from Bittrex - works without secret & key
        balances = ["DGB", "USDT"]
        testEntries = await api.get_balances(symbol=balances)

        assert testEntries["USDT"]["currencySymbol"] == "USDT"
        assert float(testEntries["USDT"]["total"]) > 0
        assert float(testEntries["USDT"]["available"]) > 0
        assert testEntries["USDT"]["updatedAt"]

        assert testEntries["DGB"]["currencySymbol"] == "DGB"
        assert float(testEntries["DGB"]["total"]) > 0
        assert float(testEntries["DGB"]["available"]) > 0
        assert testEntries["DGB"]["updatedAt"]

        await api.close()
    else:
        api = Bittrex()

        try:
            await api.get_balances()
            assert False
        except BittrexInvalidAuthentication:
            assert True
        finally:
            await api.close()


@pytest.mark.asyncio
async def test_get_two_balances(
    api_key: Optional[str] = API_KEY, api_secret: Optional[str] = API_SECRET
):
    """
    Test gathering balances. Exception must be thrown without API details
    """

    if api_key and api_secret:
        api = Bittrex(api_key, api_secret)

        # Get the active markets from Bittrex - works without secret & key
        testEntries = await api.get_balances()

        assert testEntries["USDT"]["currencySymbol"] == "USDT"
        assert float(testEntries["USDT"]["total"]) > 0
        assert float(testEntries["USDT"]["available"]) > 0
        assert testEntries["USDT"]["updatedAt"]

        assert testEntries["DGB"]["currencySymbol"] == "DGB"
        assert float(testEntries["DGB"]["total"]) > 0
        assert float(testEntries["DGB"]["available"]) > 0
        assert testEntries["DGB"]["updatedAt"]

        await api.close()
    else:
        api = Bittrex()

        try:
            await api.get_balances()
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
            if testEntries:
                assert testEntries[0]["id"]
                assert testEntries[0]["marketSymbol"]
                assert testEntries[0]["direction"]
                assert testEntries[0]["type"]
                assert testEntries[0]["quantity"]
            else:
                logging.warning("No open orders found so function cannot be tested")
        except BittrexInvalidAuthentication:
            logging.error(
                "Invalid authentication while API_KEY and API_SECRET were provided!"
            )
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
            if testEntries:
                assert testEntries[0]["id"]
                assert testEntries[0]["marketSymbol"]
                assert testEntries[0]["direction"]
                assert testEntries[0]["type"]
                assert testEntries[0]["quantity"]
            else:
                logging.warning("No open orders found so function cannot be tested")
        except BittrexInvalidAuthentication:
            logging.error(
                "Invalid authentication while API_KEY and API_SECRET were provided!"
            )
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
