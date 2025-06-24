import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

# Create logs directory if missing
import os
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='logs/trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        try:
            self.client.futures_account()
            logging.info("Connected to Binance Futures Testnet.")
        except BinanceAPIException as e:
            logging.error(f"Connection failed: {str(e)}")
            print(f"Error: {str(e)}")
            exit(1)

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == 'MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                if not price:
                    raise ValueError("Limit order requires a price.")
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            else:
                raise ValueError("Unsupported order type.")

            logging.info(f"Order Placed: {order}")
            print("Order executed successfully.")
            print(order)

        except BinanceAPIException as e:
            logging.error(f"Binance API Error: {str(e)}")
            print(f"API Error: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected Error: {str(e)}")
            print(f"Error: {str(e)}")
