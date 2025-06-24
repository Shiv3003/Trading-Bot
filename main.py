import os
from dotenv import load_dotenv
from bot.basic_bot import BasicBot
from strategies.oco_strategy import place_oco_order
from strategies.stop_loss import place_stop_loss
from strategies.grid_trading import execute_grid

load_dotenv()

def show_menu():
    print("\n=== Binance Trading Bot CLI Menu ===")
    print("1. Place MARKET or LIMIT Order")
    print("2. Place OCO Order (SPOT only)")
    print("3. Place Stop-Loss Order (FUTURES)")
    print("4. Run Grid Trading (FUTURES)")
    print("0. Exit")


def get_basic_input():
    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
    side = input("Order Side (BUY or SELL): ").strip().upper()
    quantity = float(input("Quantity: ").strip())
    return symbol, side, quantity


def run_cli():
    API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
    API_SECRET = os.getenv("BINANCE_TESTNET_API_SECRET")

    if not API_KEY or not API_SECRET:
        print("Missing API credentials in .env")
        return

    bot = BasicBot(API_KEY, API_SECRET)
    client = bot.client

    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        if choice == '1':
            symbol, side, quantity = get_basic_input()
            order_type = input("Order Type (MARKET or LIMIT): ").strip().upper()
            price = None
            if order_type == 'LIMIT':
                price = float(input("Limit Price: ").strip())
            bot.place_order(symbol, side, order_type, quantity, price)

        elif choice == '2':
            print("\n--- OCO Order ---")
            symbol, side, quantity = get_basic_input()
            price = float(input("Limit Price: ").strip())
            stop_price = float(input("Stop Price: ").strip())
            stop_limit_price = float(input("Stop-Limit Price: ").strip())
            result = place_oco_order(client, symbol, side, quantity, price, stop_price, stop_limit_price)
            print(result)

        elif choice == '3':
            print("\n--- Stop-Loss Order ---")
            symbol, side, quantity = get_basic_input()
            stop_price = float(input("Stop Price: ").strip())
            limit_price = float(input("Limit Price (optional): ").strip())
            result = place_stop_loss(client, symbol, side, quantity, stop_price, limit_price)
            print(result)

        elif choice == '4':
            print("\n--- Grid Trading ---")
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            base_price = float(input("Base price: ").strip())
            grid_size = int(input("Number of grid levels: ").strip())
            quantity = float(input("Quantity per order: ").strip())
            price_gap_pct = float(input("Gap between levels (percentage): ").strip())
            result = execute_grid(client, symbol, base_price, grid_size, quantity, price_gap_pct)
            print(result)

        elif choice == '0':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    run_cli()
