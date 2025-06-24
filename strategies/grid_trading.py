from binance.client import Client
from binance.enums import *
import logging

def execute_grid(client: Client, symbol: str, base_price: float, grid_size: int, quantity: float, price_gap_pct: float):
    orders = []
    try:
        for i in range(1, grid_size + 1):
            buy_price = round(base_price * (1 - price_gap_pct / 100 * i), 2)
            sell_price = round(base_price * (1 + price_gap_pct / 100 * i), 2)

            buy_order = client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=buy_price
            )

            sell_order = client.futures_create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=sell_price
            )

            orders.append({"buy": buy_order, "sell": sell_order})
    except Exception as e:
        logging.error(str(e))
        orders.append({"error": str(e)})

    return orders
