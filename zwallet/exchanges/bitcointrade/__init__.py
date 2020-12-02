from .api import BitcoinTradeBitcoin, BitcoinTradeMarket, BitcoinTradePublic, BitcoinTradeWallets


BitcoinTradeBitcoin = BitcoinTradeBitcoin
BitcoinTradeMarket = BitcoinTradeMarket
BitcoinTradePublic = BitcoinTradePublic
BitcoinTradeWallets = BitcoinTradeWallets


def get_transfer_fee(value: float) -> float:
    """	0,99% + R$ 4,90"""
    return (value * (0.99 / 100)) + 4.9
