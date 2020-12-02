"""Top-level package for ZWallet."""
from . import exchanges
from .zwallet import get_btc_quote

__author__ = """Giovani Zamboni"""
__email__ = 'g@zamboni.dev'
__version__ = '0.1.0'

exchanges = exchanges
get_btc_quote = get_btc_quote
