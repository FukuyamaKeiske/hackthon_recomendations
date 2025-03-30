from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Channel
from models.search import TelegramSearch

API_ID = '8339103'
API_HASH = 'debb01521a14f83592fc5ab9ea220953'
PHONE_NUMBER = '+79604767911'

class Telegram:
    def __init__(self):
        self.client = TelegramClient('tg_parser', API_ID, API_HASH)

    async def start(self):
        await self.client.start(PHONE_NUMBER)
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(PHONE_NUMBER)
            try:
                await self.client.sign_in(PHONE_NUMBER, input('Введите код: '))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input('Введите пароль: '))

    async def search_brand_channels(self, brand_name, keywords=None, limit=10) -> list[TelegramSearch]:
        async with self.client:
            channels = []
            # Формируем запрос с всеми обязательными параметрами
            if "t.me" not in brand_name:
                result = await self.client(SearchRequest(
                    q=brand_name,
                    limit=limit,
                ))

                for chat in result.chats:
                    if isinstance(chat, Channel) and chat.username:
                        ch_full = await self.client(GetFullChannelRequest(channel=chat))
                        desc = ch_full.full_chat.about
                        if keywords:
                            for keyword in keywords:
                                if keyword.lower() in desc.lower() or keyword.lower() in chat.title.lower():
                                    if chat.broadcast:
                                        channels.append(TelegramSearch(
                                            title=chat.title,
                                            username=chat.username,
                                            url=f'https://t.me/{chat.username}',
                                            image="https://pic.rutubelist.ru/user/2025-01-09/4e/5e/4e5e0faff8ad97cf55804c2155bb5d00.jpg",
                                            description=desc,
                                            subscribers=chat.participants_count
                                        ))
                                        break
                        else:
                            if chat.broadcast:
                                channels.append(TelegramSearch(
                                    title=chat.title,
                                    username=chat.username,
                                    url=f'https://t.me/{chat.username}',
                                    image="https://pic.rutubelist.ru/user/2025-01-09/4e/5e/4e5e0faff8ad97cf55804c2155bb5d00.jpg",
                                    description=desc,
                                    subscribers=chat.participants_count
                                ))
                                break
                if len(channels) == 0:
                    if keywords:
                        for keyword in keywords:
                            result = await self.client(SearchRequest(
                                q=brand_name + " " + keyword,
                                limit=limit,
                            ))
                            for chat in result.chats:
                                if isinstance(chat, Channel) and chat.username:
                                    ch_full = await self.client(GetFullChannelRequest(channel=chat))
                                    desc = ch_full.full_chat.about
                                    if chat.broadcast:
                                        channels.append(TelegramSearch(
                                            title=chat.title,
                                            username=chat.username,
                                            url=f'https://t.me/{chat.username}',
                                            image="https://pic.rutubelist.ru/user/2025-01-09/4e/5e/4e5e0faff8ad97cf55804c2155bb5d00.jpg",
                                            description=desc,
                                            subscribers=chat.participants_count
                                        ))
            else:
                channel = await self.client.get_entity(brand_name)
                ch_full = await self.client(GetFullChannelRequest(channel=channel))
                chat = ch_full.full_chat
                channels.append(TelegramSearch(
                    title=channel.title,
                    username=channel.username,
                    url=f'https://t.me/{channel.username}',
                    image="https://pic.rutubelist.ru/user/2025-01-09/4e/5e/4e5e0faff8ad97cf55804c2155bb5d00.jpg",
                    description=chat.about,
                    subscribers=chat.participants_count
                ))
            return channels 
