from app.api.schemas.deserts import DesertDetailsModel, DesertModel
from app.api.schemas.users import User
from app.db.cruds import deserts as desert_utils
from app.api.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

desert_router = APIRouter()


@desert_router.post("/", response_model=DesertDetailsModel, status_code=201)
async def create_desert(desert: DesertModel, current_user: User = Depends(get_current_user)):
    desert = await desert_utils.create_desert(desert, current_user)
    return desert


@desert_router.get("/")
async def get_deserts(page: int = 1):
    total_cout = await desert_utils.get_deserts_count()
    deserts = await desert_utils.get_deserts(page)
    return {"total_count": total_cout, "results": deserts}


@desert_router.get("/{desert_id}", response_model=DesertDetailsModel)
async def get_desert(desert_id: int):
    return await desert_utils.get_desert(desert_id)


@desert_router.put("/{desert_id}", response_model=DesertDetailsModel)
async def update_desert(
    desert_id: int, desert_data: DesertModel, current_user=Depends(get_current_user)
):
    desert = await desert_utils.get_desert(desert_id)
    if desert["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this desert",
        )

    await desert_utils.update_desert(desert_id=desert_id, desert=desert_data)
    return await desert_utils.get_desert(desert_id)
