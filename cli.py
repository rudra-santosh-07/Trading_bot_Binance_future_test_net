import argparse
import os
from bot.logging_config import setup_logging
from bot.validators import validate_inputs
from bot.client import BinanceFuturesTestnetClient

# You will paste your Testnet API keys here later
API_KEY = "Binomo_API_Key"
API_SECRET = "BIniomo_secret_key"

def main():
    # Initialize our dual terminal/file logging configuration
    setup_logging()
    
    # Configure the CLI argument parser to accept inputs smoothly
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot CLI")
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g., BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side: BUY or SELL")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="The amount of crypto asset to trade")
    parser.add_argument("--price", help="Required only if order type is LIMIT")

    args = parser.parse_args()

    try:
        # Step 1: Validate inputs locally before sending a request over the network
        validate_inputs(args.symbol, args.side, args.type, args.quantity, args.price)
        
        # Step 2: Initialize the API wrapper client
        client = BinanceFuturesTestnetClient(API_KEY, API_SECRET)
        
        # Step 3: Send the signed trade request to the Binance Futures Testnet
        success, result = client.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
        
        # Step 4: Display a clean, structured summary output directly in the CLI terminal
        print("\n" + "="*50)
        print("TRADE ORDER REQUEST SUMMARY")
        print("="*50)
        print(f"Target Asset : {args.symbol.upper()}")
        print(f"Action Side  : {args.side.upper()}")
        print(f"Order Type   : {args.type.upper()}")
        print(f"Quantity     : {args.quantity}")
        if args.price:
            print(f"Limit Price  : {args.price}")
        print("-"*50)
        
        if success:
            print(f"EXECUTION STATUS: SUCCESS")
            print(f"Binance Order ID: {result.get('orderId')}")
            print(f"Executed Qty    : {result.get('executedQty')}")
            print(f"Avg Fill Price  : {result.get('avgPrice', 'Market Filled')}")
        else:
            print(f"EXECUTION STATUS: FAILED")
            print(f"Error Message   : {result.get('msg', 'Unknown Endpoint Error')}")
        print("="*50 + "\n")

    except ValueError as err:
        print(f"\n[Configuration Error]: {err}\n")

if __name__ == "__main__":
    main()