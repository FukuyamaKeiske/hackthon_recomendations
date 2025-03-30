import aiohttp
import asyncio
from models.search import RutubeSearch

class Rutube:
    def __init__(self):
        self.base_url = 'https://rutube.ru/api/search/authors/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

    async def search_channels(self, query, keywords) -> list[RutubeSearch]:
        async with aiohttp.ClientSession() as session:
            params = {
                'query': query,
                'client': 'wdp',
                'fields': 'video_count,is_official',
                'page': 1
            }
            
            async with session.get(self.base_url, headers=self.headers, params=params) as response:
                if response.status != 200:
                    return []
                    
                data = await response.json()
                channels = []
                if 'results' not in data:
                    return channels
                for item in data.get('results', []):
                    try:
                        if keywords:
                            for keyword in keywords:
                                if keyword.lower() in item.get('description', '').lower() or keyword.lower() in item.get('name', '').lower():
                                    channels.append(RutubeSearch(
                                        title=item.get('name', ''),
                                        description=item.get('description', ''),
                                        url=item.get('absolute_url', ''),
                                        image=item.get('icon', ''),
                                        subscribers=item.get('subscribers_count', 0)
                                    ))
                                    break
                        else:
                            channels.append(RutubeSearch(
                                title=item.get('name', ''),
                                description=item.get('description', ''),
                                url=item.get('absolute_url', ''),
                                image=item.get('icon', ''),
                                subscribers=item.get('subscribers_count', 0)
                            ))
                    except Exception as e:
                        print(f"Ошибка обработки элемента: {e}")
                        continue
                        
                return channels

async def main():
    brand_name = input("Введите название бренда: ")
    searcher = Rutube()
    channels = await searcher.search_channels(brand_name)
    
    print(f"\nНайденные каналы на RuTube для '{brand_name}':")
    for ch in channels:
        print(f"Название: {ch['title']}")
        print(f"Ссылка: {ch['url']}")
        print(f"Описание: {ch['description']}")
        print(f"Подписчиков: {ch['subscribers']}")
        print('-' * 40)

if __name__ == '__main__':
    asyncio.run(main())