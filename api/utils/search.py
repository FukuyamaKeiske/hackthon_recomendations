from search_engine import Telegram, Rutube


async def search_brand(name: str, keywords: list[str]):
    complete_channels = []
    
    tg_searcher = Telegram()
    await tg_searcher.start()
    tg_channels = await tg_searcher.search_brand_channels(name, None if len(keywords) == 0 else keywords)
    complete_channels += tg_channels
    
    rt_searcher = Rutube()
    rt_channels = await rt_searcher.search_channels(name, None if len(keywords) == 0 else keywords)
    
    complete_channels += rt_channels
    return complete_channels
