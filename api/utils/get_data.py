import json
from aiohttp import ClientSession
from models.search import BrandInfo

async def get_recomendations(data1: BrandInfo, data2: BrandInfo):
    
    url = "https://gpt.jasper.finance/api/openai/v1/chat/completions"
    
    text = f"""
Проанализируй два бизнеса на основе их данных и предложи рекомендации для первого бизнеса, чтобы он превзошел конкурента. Учти следующие параметры: 

    Адрес :   
        Сравни локации бизнесов. Если адрес конкурента более выгодный (например, в проходимом месте), предложи варианты улучшения видимости или логистики для первого бизнеса.
         

    Название :   
        Оцени, насколько название первого бизнеса отражает его сферу и выделяется на фоне конкурента. Если название слабо запоминается, слишком общее или схоже с конкурентом, рекомендуй рассмотреть ребрендинг (без конкретных вариантов).
         

    Сфера :   
        Сравни ниши бизнесов. Если конкурент охватывает более узкий или востребованный сегмент, предложи идеи для диверсификации услуг/продуктов или уточнения специализации.
         

    Ключевые слова :   
        Проанализируй SEO-ключевые слова конкурента (например, их частоту, релевантность). Найди пробелы в текущей стратегии первого бизнеса и предложи ключевые слова/фразы, которые помогут привлечь больше клиентов.
         
     

Формат ответа :   

    Кратко опиши выводы по каждому пункту.  
    Дай конкретные рекомендации (не общие фразы), как усилить позиции бизнеса.  
    Избегай предложений по изменению названия — только анализ необходимости.
     

Данные для анализа :   

    Бизнес 1: {data1.model_dump()}.  
    Конкурент: {data2.model_dump()}.    
"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
        "Accept": "application/json, text/event-stream",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://gpt.jasper.finance/",
        "Content-Type": "application/json",
        "Authorization": "Bearer nk-jasper",
        "Origin": "https://gpt.jasper.finance",
        "Connection": "keep-alive",
    }

    payload = {
        "messages": [
            {
                "content": "\nYou are ChatGPT, a large language model trained by OpenAI.\nKnowledge cutoff: 2023-10\nCurrent model: chatgpt-4o-latest\nCurrent time: Sat Mar 29 2025 18:19:39 GMT+0300 (Москва, стандартное время)\nLatex inline: \\(x^2\\) \nLatex block: $$e=mc^2$$\n\n\nYou are an AI assistant with access to system tools. Your role is to help users by combining natural language understanding with tool operations when needed.\n\n1. AVAILABLE TOOLS:\n\n[clientId]\ngithub.com/modelcontextprotocol/servers/tree/main/src/filesy… \n ```{\n \"method\": \"search_repositories\",\n \"params\": {\n \"query\": \"2oeee\"\n }\n}\n ```\n\n This is wrong because the method is not tools/call.!!!!!!!!!!!\n\n the right format is:\n ```json:mcp:filesystem\n {\n \"method\": \"tools/call\",\n \"params\": {\n \"name\": \"search_repositories\",\n \"arguments\": {\n \"query\": \"2oeee\"\n }\n }\n }\n ```\n \n please follow the format strictly ONLY use tools/call method!!!!!!!!!!!\n \n",
                "role": "system"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "stream": True,
        "model": "chatgpt-4o-latest",
        "temperature": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "top_p": 1
    }

    async with ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                result = ""
                async for line in response.content:
                    if line.decode("utf-8").replace("[DONE]", "").replace("data: ", "") != "":
                        if line:
                            try:
                                result += json.loads(line.decode('utf-8').replace("data: ", ""))[
                                    "choices"][0]["delta"]["content"]
                            except:
                                continue
                return result.replace("```", "").replace("json", "")
            else:
                print(f"Request failed with status code {response.status}")
                return "Ошибка обнаружения"

async def get_revamped_text(text: str):
    url = "https://gpt.jasper.finance/api/openai/v1/chat/completions"

    text = """
Определи категории, по которым можно подобрать конкурентов по данным:
Найденные каналы для бренда 'Rostics':
""" + text + """
---
Группы категорий (писать только возможные, максимум 2 слова для категории): название бизнеса, описание, ссылка, ссылка на картинку аккаунта, количество подписчиков,  адрес (город, улица, дом), род занятий, размер бизнеса (малый, средний, большой), список ключевые слов/словосочетаний, которые могут помочь


В ответ пришли ТОЛЬКО json словарь с ключами name, description, url, image (картинка аккаунта), subscribers, adress (Россия, если не удалось найти адрес), type, size, keywords (список внутри, кейворды должны полностью относится именно к типу бизнеса, без обобщений по типу франшиза, бизнес и т.д.).


---


Все возможные роды занятий для бизнесов:
[
    "Сельское хозяйство",
    "Животноводство",
    "Рыболовство",
    "Лесное хозяйство",
    "Гидропоника",
    "Генетика растений",
    "Горнодобывающая промышленность",
    "Добыча нефти и газа",
    "Добыча полезных ископаемых",
    "Переработка сырья",
    "Промышленное производство",
    "Металлургия",
    "Машиностроение",
    "Текстильная промышленность",
    "Обувная промышленность",
    "Производство электроники",
    "Производство бытовой техники",
    "Производство мебели",
    "Производство игрушек",
    "Производство упаковки",
    "Производство строительных материалов",
    "Производство пластмасс",
    "Производство бумаги",
    "Пищевая промышленность",
    "Молочная промышленность",
    "Мясопереработка",
    "Пекарное производство",
    "Алкогольная промышленность",
    "Табачная промышленность",
    "Энергетика",
    "Атомная энергетика",
    "Гидроэнергетика",
    "Ветроэнергетика",
    "Солнечная энергетика",
    "Геотермальная энергетика",
    "Водородная энергетика",
    "Утилизация отходов",
    "Углеродная нейтрализация",
    "Строительство",
    "Гражданское строительство",
    "Дорожное строительство",
    "Инфраструктурные проекты",
    "Архитектура",
    "Градостроительство",
    "Инжиниринг",
    "Транспорт",
    "Автомобильные перевозки",
    "Железнодорожный транспорт",
    "Авиационный транспорт",
    "Морской транспорт",
    "Космический транспорт",
    "Логистика",
    "Складская логистика",
    "Таможенные услуги",
    "Цепочки поставок",
    "Оптовая торговля",
    "Розничная торговля",
    "Электронная коммерция",
    "Маркетплейсы",
    "Финансовые услуги",
    "Банковская деятельность",
    "Страхование",
    "Инвестиции",
    "Венчурный капитал",
    "Криптовалюты",
    "Финтех",
    "Бухгалтерия",
    "Аудит",
    "Информационные технологии",
    "Разработка ПО",
    "Разработка мобильных приложений",
    "Веб-разработка",
    "Кибербезопасность",
    "Облачные технологии",
    "Искусственный интеллект",
    "Машинное обучение",
    "Блокчейн",
    "AR/VR технологии",
    "IoT (Интернет вещей)",
    "Big Data",
    "Телекоммуникации",
    "Мобильная связь",
    "Интернет-провайдеры",
    "Спутниковая связь",
    "Здравоохранение",
    "Медицинские технологии",
    "Больницы и клиники",
    "Телемедицина",
    "Медицинская диагностика",
    "Психология и психотерапия",
    "Образование",
    "Онлайн-образование",
    "Школы и университеты",
    "Дополнительное образование",
    "Корпоративное обучение",
    "Языковые школы",
    "Туризм",
    "Экологический туризм",
    "Медицинский туризм",
    "Культурный туризм",
    "Гостиничный бизнес",
    "Хостелы",
    "Отели",
    "Санатории",
    "Ресторанный бизнес",
    "Фастфуд",
    "Кейтеринг",
    "Кофейни",
    "Барная индустрия",
    "Медиа",
    "Телевидение",
    "Радио",
    "Печать",
    "Интернет-СМИ",
    "Блогинг",
    "Подкасты",
    "Реклама",
    "Digital-маркетинг",
    "SEO/SEM",
    "SMM",
    "PR-агентства",
    "Брендинг",
    "Недвижимость",
    "Жилая недвижимость",
    "Коммерческая недвижимость",
    "Управление недвижимостью",
    "Юридические услуги",
    "Адвокатская практика",
    "Нотариальные услуги",
    "Международное право",
    "Консалтинг",
    "Бизнес-консалтинг",
    "IT-консалтинг",
    "HR-консалтинг",
    "Наука и исследования",
    "Фундаментальная наука",
    "Прикладные исследования",
    "Астрономия",
    "Биология",
    "Химия",
    "Физика",
    "Искусство",
    "Изобразительное искусство",
    "Музыка",
    "Киноиндустрия",
    "Фотография",
    "Театр",
    "Культура",
    "Наследие и музеи",
    "Религиозные организации",
    "Социальные инициативы",
    "Спорт",
    "Профессиональный спорт",
    "Фитнес-индустрия",
    "Йога и велнес",
    "Киберспорт",
    "Развлечения",
    "Игровая индустрия",
    "Кинотеатры",
    "Парки развлечений",
    "Сфера услуг",
    "Уборка",
    "Ремонт",
    "Салон красоты",
    "Парикмахерские",
    "Тату-салоны",
    "Химчистка",
    "Химическая промышленность",
    "Фармацевтика",
    "Биотехнологии",
    "Косметическая промышленность",
    "Автомобильная промышленность",
    "Авиастроение",
    "Судостроение",
    "Железнодорожное машиностроение",
    "Легкая промышленность",
    "Дизайн",
    "Мода",
    "Ювелирное производство",
    "Промышленный дизайн",
    "UX/UI дизайн",
    "Издательское дело",
    "Переводческие услуги",
    "HR и рекрутинг",
    "Некоммерческие организации",
    "Политическая деятельность",
    "Военная промышленность",
    "Охрана и безопасность",
    "Частные детективы",
    "Экологические технологии",
    "Робототехника",
    "Космическая индустрия",
    "Общественный транспорт",
    "Управление отходами",
    "Водоочистка",
    "Государственные услуги",
    "Агентства недвижимости",
    "Фриланс",
    "Коучинг",
    "Менторство",
    "Платформы онлайн-услуг",
    "Маркетинговые исследования",
    "Социальные сети",
    "Платёжные системы",
    "Маркетинг влияния",
    "Дропшиппинг",
    "Печать на заказ",
    "Краудфандинг",
    "Краудсорсинг",
    "Биржи труда",
    "Платформы аренды",
    "Коворкинги",
    "Инкубаторы и акселераторы",
    "Франчайзинг"
]
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
        "Accept": "application/json, text/event-stream",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://gpt.jasper.finance/",
        "Content-Type": "application/json",
        "Authorization": "Bearer nk-jasper",
        "Origin": "https://gpt.jasper.finance",
        "Connection": "keep-alive",
    }

    payload = {
        "messages": [
            {
                "content": "\nYou are ChatGPT, a large language model trained by OpenAI.\nKnowledge cutoff: 2023-10\nCurrent model: chatgpt-4o-latest\nCurrent time: Sat Mar 29 2025 18:19:39 GMT+0300 (Москва, стандартное время)\nLatex inline: \\(x^2\\) \nLatex block: $$e=mc^2$$\n\n\nYou are an AI assistant with access to system tools. Your role is to help users by combining natural language understanding with tool operations when needed.\n\n1. AVAILABLE TOOLS:\n\n[clientId]\ngithub.com/modelcontextprotocol/servers/tree/main/src/filesy… \n ```{\n \"method\": \"search_repositories\",\n \"params\": {\n \"query\": \"2oeee\"\n }\n}\n ```\n\n This is wrong because the method is not tools/call.!!!!!!!!!!!\n\n the right format is:\n ```json:mcp:filesystem\n {\n \"method\": \"tools/call\",\n \"params\": {\n \"name\": \"search_repositories\",\n \"arguments\": {\n \"query\": \"2oeee\"\n }\n }\n }\n ```\n \n please follow the format strictly ONLY use tools/call method!!!!!!!!!!!\n \n",
                "role": "system"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "stream": True,
        "model": "chatgpt-4o-latest",
        "temperature": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "top_p": 1
    }

    async with ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                result = ""
                async for line in response.content:
                    if line.decode("utf-8").replace("\n", "").replace("\r", "").replace("[DONE]", "").replace("data: ", "") != "":
                        if line:
                            try:
                                result += json.loads(line.decode('utf-8').replace("data: ", ""))[
                                    "choices"][0]["delta"]["content"]
                            except:
                                continue
                return result.replace("```", "").replace("json", "")
            else:
                print(f"Request failed with status code {response.status}")
                return "Ошибка обнаружения"


async def get_data(text):
    return json.loads(await get_revamped_text(text))
