import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBEAPI_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.view_count = channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f"{self.title}({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return  self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return  self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return  self.subscriber_count <= other.subscriber_count

    # def __eq__(self, other):
    #     if isinstance(other, Channel):
    #         return self.title == other.title
    #     return False


    def print1(self, to_print: dict) -> None:
        print(json.dumps(to_print, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        # api_key: str = os.getenv('YOUTUBEAPI_KEY')
        # youtube = build('youtube', 'v3', developerKey=api_key)
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.print1(channel)

    @classmethod
    def get_service(cls):
        # return build("youtube", "v3", developerKey=api_key)
        # api_key: str = os.getenv('YouTubeAPI_KEY')
        # youtube = build('youtube', 'v3', developerKey=api_key)
        return cls.youtube

    def to_json(self, filename):
        result = {
            "id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False)
