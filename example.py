# From local file - import 'aiobittrexapi' pypi package if not running locally
from aiobittrexapi.api import BittrexAPI
from aiobittrexapi.errors import (
    BittrexApiError,
    BittrexResponseError,
    BittrexInvalidAuthentication,
)

import asyncio
from typing import Optional

API_KEY = ""
API_SECRET = ""


async def main(api_key: Optional[str] = None, api_secret: Optional[str] = None):
    if api_key and api_secret:
        api = BittrexAPI(api_key, api_secret)
    else:
        api = BittrexAPI()

    try:
        # Get the active markets from Bittrex - works without secret & key
        markets = await api.get_markets()
        print(markets)

        # Get your account data - requires secret & key
        account = await api.get_account()
    except BittrexApiError as e:
        print(e)
    except BittrexResponseError as e:
        print("Invalid response:", e)
    except BittrexInvalidAuthentication:
        print("Invalid authentication. Please provide a correct API Key and Secret")
    else:
        print(account)
    finally:
        await api.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    if API_KEY and API_SECRET:
        loop.run_until_complete(main(API_KEY, API_SECRET))
    else:
        loop.run_until_complete(main())
