from typing import List, Dict, Tuple, Optional
TAX_RATE = 0.21
SAVE10_RATE = 0.10
SAVE20_HIGH_RATE = 0.20
SAVE20_LOW_RATE = 0.05
SAVE20_THRESHOLD = 200
VIP_DEFAULT_DISCOUNT = 50
VIP_LOW_SUBTOTAL_DISCOUNT = 10
VIP_THRESHOLD = 100

def validate_items(items: List[Dict]) -> None:
    if not isinstance(items, list) or len(items) == 0:
        raise ValueError("items must be a non-empty list")
    for item in items:
        if "price" not in item or "qty" not in item:
            raise ValueError("item must have price and qty")
        if item["price"] <= 0 or item["qty"] <= 0:
            raise ValueError("price and qty must be positive")

def calculate_subtotal(items: List[Dict]) -> float:
    return sum(item["price"] * item["qty"] for item in items)

def get_coupon_discount(coupon: Optional[str], subtotal: float) -> float:
    if not coupon:
        return 0
    
    if coupon == "SAVE10":
        return subtotal * SAVE10_RATE
    elif coupon == "SAVE20":
        rate = SAVE20_HIGH_RATE if subtotal >= SAVE20_THRESHOLD else SAVE20_LOW_RATE
        return subtotal * rate
    elif coupon == "VIP":
        return VIP_DEFAULT_DISCOUNT if subtotal >= VIP_THRESHOLD else VIP_LOW_SUBTOTAL_DISCOUNT
    
    raise ValueError("unknown coupon")

def process_checkout(request: Dict) -> Dict:
    user_id = request.get("user_id")
    if user_id is None:
        raise ValueError("user_id is required")
        
    items = request.get("items")
    validate_items(items)
    
    subtotal = calculate_subtotal(items)
    discount = int(get_coupon_discount(request.get("coupon"), subtotal))
    
    total_after_discount = max(0, subtotal - discount)
    tax = int(total_after_discount * TAX_RATE)
    total = total_after_discount + tax
    
    return {
        "order_id": f"{user_id}-{len(items)}-{int(total)}",
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "currency": request.get("currency", "USD")
    }