from app.api.schemas.recipes import RecipeDetailsModel, RecipeModel
from app.api.schemas.users import User
from app.db.cruds import recepies as recipe_utils
from app.api.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

recipe_router = APIRouter()


@recipe_router.post("/", response_model=RecipeDetailsModel, status_code=201)
async def create_post(recipe: RecipeModel, current_user: User = Depends(get_current_user)):
    recipe = await recipe_utils.create_recipe(recipe, current_user)
    return recipe


@recipe_router.get("/")
async def get_recepies(page: int = 1):
    total_cout = await recipe_utils.get_recipes_count()
    recipes = await recipe_utils.get_recipes(page)
    return {"total_count": total_cout, "results": recipes}


@recipe_router.get("/my_recipes")
async def read_my_recipes(current_user: User = Depends(get_current_user)):
    my_recipes = await recipe_utils.get_my_recipes(current_user)
    return {"my_recipes": my_recipes}

@recipe_router.get("/{recipe_id}", response_model=RecipeDetailsModel)
async def get_recipe(recipe_id: int):
    return await recipe_utils.get_recipe(recipe_id)


@recipe_router.put("/{recipe_id}", response_model=RecipeDetailsModel)
async def update_recipe(
    recipe_id: int, recipe_data: RecipeModel, current_user=Depends(get_current_user)
):
    recipe = await recipe_utils.get_recipe(recipe_id)
    if recipe["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this recipe",
        )

    await recipe_utils.update_recipe(recipe_id=recipe_id, recipe=recipe_data)
    return await recipe_utils.get_recipe(recipe_id)
