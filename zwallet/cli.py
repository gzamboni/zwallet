"""Console script for zwallet."""
from datetime import datetime
from locale import LC_ALL
import sys
from typing import List
import click
import locale

from zwallet import get_btc_quote
from zwallet.exchanges import bitcointrade
from time import sleep


UP_ARROW = '\u2B08'
DOWN_ARROW = '\u2B0A'
EQUAL = '\u2B0C'

locale.setlocale(LC_ALL, 'pt_BR.UTF-8')


def get_arrow(current: float, last: float) -> str:
    """Get current arrow indicator

    Args:
        current (float): Current value
        last (float): last value

    Returns:
        str: UP_ARROW if current > last,
             DOWM_ARROW if current < last.
             EQUAL if current == last
    """
    return_value = EQUAL

    if current > last:
        return_value = UP_ARROW
    elif current < last:
        return_value = DOWN_ARROW

    return return_value


def get_and_print_ticker(quote: dict) -> List[float]:
    """Get BTC quotes and print the ticker

    Args:
        quote (dict): Dict object with quotes from the Exchange

    Returns:
        List[float]: A list with [buy, sell, last_trade] prices
    """
    click.echo(f'BitCoinTrade Quotes - {quote.get("date", datetime.now()).strftime("%b %d %Y %H:%M:%S")}')
    click.echo('')
    if quote.get('error', False):
        click.echo(click.style(quote.get('message', ''), fg='red'), err=True)
        sys.exit(1)
    buy = quote.get("buy", 0)
    sell = quote.get("sell", 0)
    last_trade = quote.get("last", 0)
    last_buy = quote.get("last_buy", 0)
    last_sell = quote.get("last_sell", 0)
    last_last_trade = quote.get("last_last_trade", 0)

    click.secho(f'Venda:  {locale.currency(sell, grouping=True)} {get_arrow(sell, last_sell)}', fg='green')
    click.echo(f'Último: {locale.currency(last_trade, grouping=True)} {get_arrow(last_trade, last_last_trade)}')
    click.secho(f'Compra: {locale.currency(buy, grouping=True)} {get_arrow(buy, last_buy)}', fg='red')
    return [buy, sell, last_trade]


@click.group()
def main():
    pass


@click.command()
@click.option(
    '--follow',
    '-f',
    is_flag=True,
    help='BTC quote gonna be countinously checked'
)
@click.option(
    '--sleep-interval',
    '-s',
    type=click.IntRange(1, 60, clamp=True),
    default=60,
    help='with -f, sleep for approximately N seconds (default 60s) between iterations'
)
def ticker(follow: bool, sleep_interval: int):
    """Track current BTC prices."""
    if follow:
        click.clear()
    repeat_check_quote = True
    last_buy = 0
    last_sell = 0
    last_last_trade = 0

    while repeat_check_quote:
        quote = get_btc_quote()
        quote.update({
            'last_buy': last_buy,
            'last_sell': last_sell,
            'last_last_trade': last_last_trade
        })
        buy, sell, last_trade = get_and_print_ticker(quote)
        last_buy = buy
        last_sell = sell
        last_last_trade = last_trade
        if not follow:
            repeat_check_quote = follow
        else:
            sleep(sleep_interval)
            click.clear()
    return 0


@click.command()
@click.option(
    '--follow',
    '-f',
    is_flag=True,
    help='BTC quote gonna be countinously checked'
)
@click.option(
    '--sleep-interval',
    '-s',
    type=click.IntRange(1, 60, clamp=True),
    default=60,
    help='with -f, sleep for approximately N seconds (default 60s) between iterations'
)
@click.option('--usdbrl', prompt='USD BRL quote', help='USD BRL quote', type=float)
@click.option('--usdbtc', prompt='USD BTC quote', help='USD BTC quote', type=float)
@click.option('--btc', prompt='BTC quantity', help='BTC quantity to monitor', type=float)
def monitor(follow: bool, sleep_interval: int, usdbrl: float, usdbtc: float, btc: float):
    """Track current BTC prices and calculate if you are making or losing money."""
    locale.setlocale(LC_ALL, 'pt_BR.UTF-8')
    if follow:
        click.clear()
    repeat_check_quote = True
    last_buy = 0
    last_sell = 0
    last_last_trade = 0

    target_usd_value = btc * usdbtc
    target_brl_value = target_usd_value * usdbrl
    transfer_fee = bitcointrade.get_transfer_fee(target_brl_value)
    target_brl_value_with_fee = target_brl_value + transfer_fee

    while repeat_check_quote:
        quote = get_btc_quote()
        quote.update({
            'last_buy': last_buy,
            'last_sell': last_sell,
            'last_last_trade': last_last_trade
        })
        buy, sell, last_trade = get_and_print_ticker(quote)

        current_brl_value = btc * last_trade
        delta = current_brl_value - target_brl_value

        click.echo()
        click.echo(f"BTC Payment:  BTC {btc} ")
        click.echo(f"USD Payment:  US$ {locale.currency(target_usd_value, grouping=True, symbol=False)} ")
        click.echo(f"BRL Target Payment:  {locale.currency(target_brl_value_with_fee, grouping=True)} ", nl=False)
        click.echo(f"({locale.currency(target_brl_value, grouping=True)} + ", nl=False)
        click.echo(f"{locale.currency(transfer_fee, grouping=True)})")
        click.echo(f"BRL Current Payment: {locale.currency(current_brl_value, grouping=True)}")
        click.secho(f"BRL Delta:           {locale.currency(delta)} {get_arrow(current_brl_value, target_brl_value)}",
                    fg='red' if delta < 0 else 'green')

        last_buy = buy
        last_sell = sell
        last_last_trade = last_trade
        if not follow:
            repeat_check_quote = follow
        else:
            sleep(sleep_interval)
            click.clear()
    return 0


main.add_command(ticker)
main.add_command(monitor)

if __name__ == "__main__":
    sys.exit(main(auto_envvar_prefix='ZWALLET'))  # pragma: no cover
