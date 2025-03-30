from pydantic import BaseModel
from typing import Optional
from models.search import BrandInfo

class SearchResponse(BaseModel):
    match: Optional[list[BrandInfo]]
    rivals: Optional[list[BrandInfo]]
    message: Optional[str]
