from datetime import datetime

from app.core.database import database
from app.db.models.recipes import recipes_table
from app.db.models.users import users_table
from app.api.schemas import recipes as recipe_schema
from sqlalchemy import desc, func, select


async def create_recipe(recipe: recipe_schema.RecipeModel, user):
    query = (
        recipes_table.insert()
        .values(
            title=recipe.title,
            content=recipe.content,
            created_at=datetime.now(),
            user_id=user["user_id"],
        )
        .returning(
            recipes_table.c.id,
            recipes_table.c.title,
            recipes_table.c.content,
            recipes_table.c.created_at,
        )
    )
    new_recipe = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    recipe = dict(zip(new_recipe, new_recipe.values()))
    recipe["user_name"] = user["name"]
    return recipe




async def get_recipe(recipe_id: int):
    query = (
        select(
            [
                recipes_table.c.id,
                recipes_table.c.created_at,
                recipes_table.c.title,
                recipes_table.c.content,
                recipes_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(recipes_table.join(users_table))
        .where(recipes_table.c.id == recipe_id)
    )
    return await database.fetch_one(query)

async def get_my_recipes(user):
    query = (
        select(
            [
                recipes_table.c.id,
                recipes_table.c.created_at,
                recipes_table.c.title,
                recipes_table.c.content,
                recipes_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(recipes_table.join(users_table))
        .where(recipes_table.c.user_id == user["user_id"])
    )
    return await database.fetch_all(query)
async def get_recipes(page: int):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                recipes_table.c.id,
                recipes_table.c.created_at,
                recipes_table.c.title,
                recipes_table.c.content,
                recipes_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(recipes_table.join(users_table))
        .order_by(desc(recipes_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_recipes_count():
    query = select([func.count()]).select_from(recipes_table)
    return await database.fetch_val(query)



async def update_recipe(recipe_id: int, recipe: recipe_schema.RecipeModel):
    query = (
        recipes_table.update()
        .where(recipes_table.c.id == recipe_id)
        .values(title=recipe.title, content=recipe.content)
    )
    return await database.execute(query)
