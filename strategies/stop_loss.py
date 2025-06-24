from binance.client import Client
from binance.enums import SIDE_SELL, SIDE_BUY

def place_stop_loss(client: Client, symbol: str, side: str, quantity: float, stop_price: float, limit_price: float):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=SIDE_SELL if side == 'SELL' else SIDE_BUY,
            type="STOP_MARKET",  # <-- Fixed here
            stopPrice=stop_price,
            closePosition=False,
            quantity=quantity
        )
        return order
    except Exception as e:
        return {"error": str(e)}
