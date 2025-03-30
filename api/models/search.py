from pydantic import BaseModel

class TelegramSearch(BaseModel):
    title: str
    username: str
    url: str
    image: str
    description: str
    subscribers: int

class RutubeSearch(BaseModel):
    title: str
    url: str
    image: str
    description: str
    subscribers: int

class BrandInfo(BaseModel):
    name: str
    description: str
    url: str
    image: str
    subscribers: int
    adress: str
    type: str
    size: str
    keywords: list[str]

class RecomendationsRequest(BaseModel):
    data1: BrandInfo
    data2: BrandInfo
