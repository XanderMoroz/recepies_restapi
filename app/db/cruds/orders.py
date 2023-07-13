from datetime import datetime

from app.core.database import database
from app.db.models.deserts import desert_table
from app.db.models.orders import order_table, order_lines_table
from app.db.models.users import users_table
from app.api.schemas import orders as order_schema
from sqlalchemy import desc, func, select


async def create_order(user):
    query = (
        order_table.insert()
        .values(
            created_at=datetime.now(),
            user_id=user["user_id"],
        )
        .returning(
            order_table.c.id,
            order_table.c.created_at,
        )
    )
    order = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    order = dict(zip(order, order.values()))
    order["user_name"] = user["name"]
    return order

async def get_my_orders(user):
    query = (
        select(
            [
                order_table.c.id,
                order_table.c.created_at,
                order_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(order_table.join(users_table))
        .where(order_table.c.user_id == user["user_id"])
    )
    orders = await database.fetch_all(query)
    return orders

async def get_order(order_id: int):
    query = (
        select(
            [
                order_table.c.id,
                order_table.c.user_id,
                order_table.c.created_at,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(order_table.join(users_table))
        .where(order_table.c.id == order_id)
    )
    order = await database.fetch_one(query)
    return order


async def create_order_line(order_line, user):
    query = (
        order_lines_table.insert()
        .values(
            order_id=order_line.order_id,
            desert_id=order_line.desert_id,
            quantity=order_line.quantity,
            created_at=datetime.now(),
            # user_id=user["user_id"],
        )
        .returning(
            order_lines_table.c.id,
            order_lines_table.c.order_id,
            order_lines_table.c.desert_id,
            order_lines_table.c.quantity,
            order_lines_table.c.created_at,
        )
    )
    order_line = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    order_line = dict(zip(order_line, order_line.values()))
    order_line["ordered_by"] = user["name"]
    return order_line

async def get_order_lines(order_id: int):
    query = (
        select(
            [
                order_lines_table.c.id,
                order_lines_table.c.order_id,
                desert_table.c.title.label("desert_title"),
                desert_table.c.price.label("desert_price"),
                order_lines_table.c.quantity,
            ]
        )
        .select_from(order_lines_table.join(desert_table))
        .where(order_lines_table.c.order_id == order_id)
    )
    order_lines = await database.fetch_all(query)

    total_price = 0
    for line in order_lines:
        total_price += line["desert_price"] * line["quantity"]

    return {"ordered_desert_list" : order_lines,
            "total_price" : total_price
            }


# async def get_order(order_id: int):
#     query = (
#         select(
#             [
#                 order_table.c.id,
#                 order_table.c.created_at,
#                 order_table.c.user_id,
#                 users_table.c.name.label("user_name"),
#             ]
#         )
#         .select_from(order_table.join(users_table))
#         .where(order_table.c.id == order_id)
#     )
#     return await database.fetch_one(query)

#
# async def get_deserts(page: int):
#     max_per_page = 10
#     offset1 = (page - 1) * max_per_page
#     query = (
#         select(
#             [
#                 desert_table.c.id,
#                 desert_table.c.created_at,
#                 desert_table.c.title,
#                 desert_table.c.content,
#                 desert_table.c.user_id,
#                 users_table.c.name.label("user_name"),
#             ]
#         )
#         .select_from(desert_table.join(users_table))
#         .order_by(desc(desert_table.c.created_at))
#         .limit(max_per_page)
#         .offset(offset1)
#     )
#     return await database.fetch_all(query)
#
#
# async def get_deserts_count():
#     query = select([func.count()]).select_from(desert_table)
#     return await database.fetch_val(query)
#
#
# async def update_desert(desert_id: int, desert: desert_schema.DesertModel):
#     query = (
#         desert_table.update()
#         .where(desert_table.c.id == desert_id)
#         .values(title=desert.title, price=desert.price)
#     )
#     return await database.execute(query)
