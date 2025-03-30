import os
import re
import json
import time
from bs4 import BeautifulSoup
import requests

class VkCommunitySearcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'
        }
        self.auth_file = 'vk_session.json'

    def auth(self, login: str, password: str) -> bool:
        """ Авторизация в ВК """
        try:
            # Получаем страницу авторизации
            auth_url = 'https://m.vk.com'
            response = self.session.get(auth_url)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Извлекаем auth_hash
            auth_hash = soup.find('input', {'name': '_auth_hash'})['value']
            
            # Отправляем данные авторизации
            data = {
                'email': login,
                'pass': password,
                '_auth_hash': auth_hash
            }
            response = self.session.post(auth_url, data=data)
            
            # Проверяем успешность авторизации
            if 'vk.com/feed' in response.url:
                # Сохраняем куки
                with open(self.auth_file, 'w') as f:
                    json.dump(
                        {c.name: c.value for c in self.session.cookies},
                        f
                    )
                return True
            return False
        except Exception as e:
            print(f"Ошибка авторизации: {e}")
            return False

    def load_session(self) -> bool:
        """ Загрузка сохраненной сессии """
        try:
            if os.path.exists(self.auth_file):
                with open(self.auth_file) as f:
                    cookies = json.load(f)
                    self.session.cookies.update(cookies)
                    return True
            return False
        except:
            return False

    def search_communities(self, query: str, max_results=10):
        """ Поиск пабликов """
        search_url = 'https://m.vk.com/search'
        params = {
            'c[q]': query,
            'c[section]': 'communities',
            'c[sort]': 2  # Сортировка по релевантности
        }
        
        response = self.session.get(search_url, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        
        communities = []
        for item in soup.select('.groups_row'):
            try:
                # Парсим данные
                title = item.select_one('.groups_name').text.strip()
                url = 'https://m.vk.com' + item.select_one('a')['href']
                description = item.select_one('.groups_desc').text.strip()
                members = item.select_one('.groups_count').text.strip()
                
                # Приводим количество подписчиков к числу
                members_count = int(
                    re.sub(r'\D', '', members.split(',')[0])
                ) if members else 0
                
                communities.append({
                    'title': title,
                    'url': url,
                    'description': description,
                    'members_count': members_count
                })
                
                if len(communities) >= max_results:
                    break
            except:
                continue
        
        return communities

def main():
    searcher = VkCommunitySearcher()
    
    # Пытаемся загрузить сохраненную сессию
    if not searcher.load_session():
        print("Авторизация требуется")
        login = input("Введите номер телефона ВК: ")
        password = input("Введите пароль: ")
        if not searcher.auth(login, password):
            print("Ошибка авторизации")
            return
    
    brand_name = input("Введите название бренда: ")
    communities = searcher.search_communities(brand_name)
    
    print(f"\nНайденные паблики для '{brand_name}':")
    for comm in communities:
        print(f"Название: {comm['title']}")
        print(f"Ссылка: {comm['url']}")
        print(f"Участников: {comm['members_count']}")
        print(f"Описание: {comm['description']}")
        print('-' * 40)

if __name__ == '__main__':
    main()