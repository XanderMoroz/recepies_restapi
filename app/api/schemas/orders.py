from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel




class OrderLineModel(BaseModel):
    """ Validate request data """
    order_id: int
    desert_id: int
    quantity: int

class OrderLineDetailsModel(OrderLineModel):
    """ Return response data """
    id: int
    created_at: datetime
    ordered_by: str

class OrderModel(BaseModel):
    """ Validate request data """



class OrderDetailsModel(OrderModel):
    """ Return response data """
    id: int
    created_at: datetime
    user_name: str
    ordered_deserts: List
    total_price: int
