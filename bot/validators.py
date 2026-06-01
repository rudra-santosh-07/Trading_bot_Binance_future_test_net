def validate_inputs(symbol, side, order_type, quantity, price):
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be either BUY or SELL")
        
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be either MARKET or LIMIT")
        
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than 0")
    except ValueError:
        raise ValueError("Quantity must be a valid number")
        
    if order_type.upper() == "LIMIT":
        if not price:
            raise ValueError("Price is required for LIMIT orders")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError("Price must be greater than 0")
        except ValueError:
            raise ValueError("Price must be a valid number")
            
    return True