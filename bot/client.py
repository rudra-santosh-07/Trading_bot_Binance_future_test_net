import time
import hmac
import hashlib
import requests
import logging

class BinanceFuturesTestnetClient:
    def __init__(self, api_key, api_secret):
        self.base_url = "https://demo-fapi.binance.com"
        self.api_key = api_key
        self.api_secret = api_secret

    def _generate_signature(self, query_string):
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def place_order(self, symbol, side, order_type, quantity, price=None):
        endpoint = "/fapi/v1/order"
        
        # Current UNIX timestamp in milliseconds (required by Binance)
        timestamp = int(time.time() * 1000)
        
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
            "timestamp": timestamp
        }
        
        if order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good 'Till Cancelled

        # 1. Generate the base query parameters string
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        
        # 2. Cryptographically hash the string using your Secret Key
        signature = self._generate_signature(query_string)
        
        # 3. Append the signature to complete the parameter string
        query_string += f"&signature={signature}"

        # 4. Bind the complete query string securely to the final endpoint URL
        url = f"{self.base_url}{endpoint}?{query_string}"

        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        logging.info(f"Sending signed order request to endpoint...")
        
        try:
            # Replaced data=query_string with structured URL parameters for accurate parsing
            response = requests.post(url, headers=headers)
            response_data = response.json()
            
            if response.status_code == 200:
                logging.info(f"API Response Code 200: Order Placed Successfully!")
                return True, response_data
            else:
                logging.error(f"Binance API Error ({response.status_code}): {response_data.get('msg')}")
                return False, response_data
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network Connection Failure: {e}")
            return False, {"error": str(e)}