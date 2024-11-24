from telethon.sync import TelegramClient
import asyncio
import re
from typing import List


class TelegramChannelParser:
    def __init__(self, api_id: int, api_hash: str, session_name: str, channels: List[str], interval: int,
                 limit: int = 1):
        self.api_id = api_id
        self.api_hash = api_hash
        self.channels = channels
        self.interval = interval
        self.limit = limit
        self.session_name = session_name
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

    async def authenticate(self):
        if not self.client.is_connected():
            await self.client.start()

    async def parse_channel(self, channel: str):
        try:
            channel_entity = await self.client.get_entity(channel)
            parsed_data = []
            async for message in self.client.iter_messages(channel_entity, limit=self.limit):
                if message.message:
                    keywords = self.extract_keywords(message.text)
                    if keywords:
                        parsed_data.append({
                            'channel': channel,
                            'keywords': keywords,
                            'post_url': f"{channel}/{message.id}",
                            'date': message.date
                        })
            return parsed_data
        except Exception as e:
            print(f"Error parsing channel {channel}: {e}")
            return []

    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        return re.findall(r'\$[A-Z]+', text)

    async def parse_channels(self):
        await self.authenticate()
        tasks = [self.parse_channel(channel) for channel in self.channels]
        result = await asyncio.gather(*tasks)
        return result

    def run(self):
        asyncio.run(self.parse_channels())
