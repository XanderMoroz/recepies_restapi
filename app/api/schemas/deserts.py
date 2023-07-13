from datetime import datetime

from pydantic import BaseModel


class DesertModel(BaseModel):
    """ Validate request data """
    title: str
    price: int


class DesertDetailsModel(DesertModel):
    """ Return response data """
    id: int
    created_at: datetime
    user_name: str
