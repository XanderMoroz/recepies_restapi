from app.api.schemas.posts import PostDetailsModel, PostModel
from app.api.schemas.users import User
from app.db.utils import posts as post_utils
from app.api.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

post_router = APIRouter()


@post_router.post("/", response_model=PostDetailsModel, status_code=201)
async def create_post(post: PostModel, current_user: User = Depends(get_current_user)):
    post = await post_utils.create_post(post, current_user)
    return post


@post_router.get("/")
async def get_posts(page: int = 1):
    total_cout = await post_utils.get_posts_count()
    posts = await post_utils.get_posts(page)
    return {"total_count": total_cout, "results": posts}


@post_router.get("/{post_id}", response_model=PostDetailsModel)
async def get_post(post_id: int):
    return await post_utils.get_post(post_id)


@post_router.put("/{post_id}", response_model=PostDetailsModel)
async def update_post(
    post_id: int, post_data: PostModel, current_user=Depends(get_current_user)
):
    post = await post_utils.get_post(post_id)
    if post["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to modify this post",
        )

    await post_utils.update_post(post_id=post_id, post=post_data)
    return await post_utils.get_post(post_id)
