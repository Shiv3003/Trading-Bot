from binance.client import Client
from binance.enums import *

def place_oco_order(client: Client, symbol: str, side: str, quantity: float, price: float, stop_price: float, stop_limit_price: float):
    try:
        if side not in ['BUY', 'SELL']:
            raise ValueError("Side must be BUY or SELL")

        order = client.create_oco_order(
            symbol=symbol,
            side=SIDE_SELL if side == 'SELL' else SIDE_BUY,
            quantity=quantity,
            price=price,
            stopPrice=stop_price,
            stopLimitPrice=stop_limit_price,
            stopLimitTimeInForce=TIME_IN_FORCE_GTC
        )
        return order
    except Exception as e:
        return {"error": str(e)}
