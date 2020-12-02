"""Main module."""
from zwallet.exchanges import bitcointrade
import dateutil.parser as dt
import datetime
from tzlocal import get_localzone


def get_btc_quote() -> dict:
    """Get the current BTC quote from BT

    Returns:
        dict: Decoded BTC quotes
              {
                  buy: float,
                  sell: float,
                  last: float
              }
    """

    bt_public = bitcointrade.BitcoinTradePublic()
    btc_ticker = bt_public.get_ticker()
    btc_data = btc_ticker.get('data')
    if btc_data is None:
        return {
            'date': datetime.datetime.now().astimezone(get_localzone()),
            'message': 'Sem dados da exchange BitcoinTrade',
            'error': True
        }

    return {
        'buy': btc_data.get('buy'),
        'high': btc_data.get('high'),
        'last': btc_data.get('last'),
        'low': btc_data.get('low'),
        'sell': btc_data.get('sell'),
        'trades_quantity': btc_data.get('trades_quantity'),
        'volume': btc_data.get('volume'),
        'date': dt.parse(btc_data.get('date')).astimezone(get_localzone()),
        'message': 'Ok'
    }
