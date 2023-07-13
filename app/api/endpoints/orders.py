from app.api.schemas.orders import OrderDetailsModel, OrderModel, OrderLineDetailsModel, OrderLineModel
from app.api.schemas.users import User
from app.db.cruds import orders as order_utils
from app.db.cruds import deserts as desert_utils
from app.api.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

order_router = APIRouter()


@order_router.post("/", response_model=OrderDetailsModel, status_code=201)
async def create_order(current_user: User = Depends(get_current_user)):
    order = await order_utils.create_order(current_user)
    return order

@order_router.get("/my_orders")
async def read_my_orders(current_user: User = Depends(get_current_user)):
    my_orders = await order_utils.get_my_orders(current_user)
    return {"my_orders": my_orders}

@order_router.get("/{order_id}", response_model=OrderDetailsModel)
async def get_order(order_id: int, current_user: User = Depends(get_current_user)):
    order = await order_utils.get_order(order_id)
    order_lines = await order_utils.get_order_lines(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order #{order_id} not found. Try another one.")

    if order["user_name"] != current_user.name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This order is not yours. You don't have access to explore this order.",
        )
    order = dict(zip(order, order.values()))

    order["ordered_deserts"] = order_lines["ordered_desert_list"]
    order["total_price"] = order_lines["total_price"]
    return order

@order_router.post("/{order_id}/", response_model=OrderLineDetailsModel, status_code=201)
async def create_order_line(order_line: OrderLineModel,
                            current_user: User = Depends(get_current_user)):
    order = await order_utils.get_order(order_line.order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order #{order_line.order_id} not found. Try another one.",
        )
    desert = await desert_utils.get_desert(order_line.desert_id)
    if desert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Desert #{order_line.order_id} not found. Try another one.",
        )
    order_line = await order_utils.create_order_line(order_line, current_user)
    return order_line