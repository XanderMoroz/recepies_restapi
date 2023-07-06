from datetime import datetime

from pydantic import BaseModel


class RecipeModel(BaseModel):
    """ Validate request data """
    title: str
    content: str


class RecipeDetailsModel(RecipeModel):
    """ Return response data """
    id: int
    created_at: datetime
    user_name: str
