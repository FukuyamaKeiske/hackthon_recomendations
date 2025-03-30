from fastapi import APIRouter, Query
from utils.search import search_brand
from utils.get_data import get_data
from models.response import SearchResponse
from models.search import BrandInfo

router = APIRouter(prefix="/api")

@router.get("/search/", response_model=SearchResponse)
async def search(brand: str, keywords: str = Query("", description="Теги через запятую")):
    keywords = keywords.split(",")
    results = await search_brand(brand, keywords)
    response = SearchResponse(match=[], rivals=[], message=None)
    if len(results) > 0:
        for result in results:
            text = f"""
- Название: {result.title}
- Описание: {result.description}
- Ссылка: {result.url}
- Картинка: {result.image}
- Подписчиков: {result.subscribers}
"""
            data = await get_data(text)
            response.match.append(BrandInfo(**data))
        return response
    return SearchResponse(match=None, rivals=None, message="Nothing found")
        
@router.get("/rivals/", response_model=SearchResponse)
async def rivals(brand: str, keywords: str = Query("", description="Теги через запятую")):
    keywords = keywords.split(",")
    results = await search_brand(brand, keywords)
    response = SearchResponse(match=[], rivals=[], message=None)
    if len(results) > 0:
        for result in results:
            text = f"""
- Название: {result.title}
- Описание: {result.description}
- Ссылка: {result.url}
- Картинка: {result.image}
- Подписчиков: {result.subscribers}
"""
            data = await get_data(text)
            response.match.append(BrandInfo(**data))
            break
    for keyword in response.match[0].keywords:
        results1 = await search_brand(keyword, [])
        processed_urls = []
        for name_part in brand.split(" "):
            results1 += await search_brand(keyword, name_part)
            results1 += await search_brand(name_part, keyword)
            results1 += await search_brand(name_part, [])
        for result1 in results1:
            if result1.url != response.match[0].url and result1.url not in processed_urls and response.match[0].name not in [result1.title, result1.description]:
                processed_urls.append(result1.url)
                t = f"""
- Название: {result1.title}
- Описание: {result1.description}
- Ссылка: {result1.url}
- Картинка: {result1.image}
- Подписчиков: {result1.subscribers}
"""
                d = await get_data(t)
                count = len(d["keywords"])
                g = 0
                for k in d["keywords"]:
                    if k in d["keywords"]:
                        g += 1
                if g / count > 0.3:
                    print(BrandInfo(**d))
                    response.rivals.append(BrandInfo(**d))
        return response
