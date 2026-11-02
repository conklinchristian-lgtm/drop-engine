from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="South Jersey Property Underwriter")

class PropertyData(BaseModel):
    zpid: Optional[str] = None
    address: str
    zip_code: str
    price: float
    estimated_arv: Optional[float] = None
    monthly_rent: Optional[float] = None
    home_type: Optional[str] = "SINGLE_FAMILY"

@app.post("/underwrite")
def underwrite(data: PropertyData):
    arv = data.estimated_arv or (data.price * 1.25)
    rent = data.monthly_rent or (data.price * 0.01)
    rehab_est = 35000.0
    
    # Strategy 1: BRRRR
    total_cost = data.price + rehab_est + (data.price * 0.03)
    max_refi = arv * 0.75
    trapped_capital = total_cost - max_refi
    monthly_debt = (max_refi * 0.07) / 12
    brrrr_cashflow = rent - (rent * 0.16) - monthly_debt
    
    # Strategy 2: Fix & Flip
    flip_profit = arv - data.price - rehab_est - (arv * 0.08)
    flip_roi = (flip_profit / (data.price + rehab_est)) * 100 if (data.price + rehab_est) > 0 else 0
    
    # Strategy Grading
    if trapped_capital <= 0 and brrrr_cashflow >= 200:
        grade = "A+"
    elif flip_profit >= 40000 and flip_roi >= 15:
        grade = "A"
    elif brrrr_cashflow > 0 or flip_profit > 20000:
        grade = "B"
    else:
        grade = "C"
        
    return {
        "address": data.address,
        "price": data.price,
        "home_type": data.home_type,
        "grade": grade,
        "trapped_capital": round(trapped_capital, 2),
        "monthly_cashflow": round(brrrr_cashflow, 2),
        "flip_profit": round(flip_profit, 2),
        "flip_roi_pct": round(flip_roi, 2)
    }
