from datetime import datetime

from app.core.database import database
from app.db.models.deserts import desert_table
from app.db.models.users import users_table
from app.api.schemas import deserts as desert_schema
from sqlalchemy import desc, func, select


async def create_desert(desert: desert_schema.DesertModel, user):
    query = (
        desert_table.insert()
        .values(
            title=desert.title,
            price=desert.price,
            created_at=datetime.now(),
            user_id=user["user_id"],
        )
        .returning(
            desert_table.c.id,
            desert_table.c.title,
            desert_table.c.price,
            desert_table.c.created_at,
        )
    )
    desert = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    desert = dict(zip(desert, desert.values()))
    desert["user_name"] = user["name"]
    return desert


async def get_desert(desert_id: int):
    query = (
        select(
            [
                desert_table.c.id,
                desert_table.c.created_at,
                desert_table.c.title,
                desert_table.c.price,
                desert_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(desert_table.join(users_table))
        .where(desert_table.c.id == desert_id)
    )
    return await database.fetch_one(query)


async def get_deserts(page: int):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                desert_table.c.id,
                desert_table.c.created_at,
                desert_table.c.title,
                desert_table.c.price,
                desert_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(desert_table.join(users_table))
        .order_by(desc(desert_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_deserts_count():
    query = select([func.count()]).select_from(desert_table)
    return await database.fetch_val(query)


async def update_desert(desert_id: int, desert: desert_schema.DesertModel):
    query = (
        desert_table.update()
        .where(desert_table.c.id == desert_id)
        .values(title=desert.title, price=desert.price)
    )
    return await database.execute(query)
