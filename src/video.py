import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YOUTUBEAPI_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        self.video_id = video_id
        try:
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id
                                                             ).execute()
            self.url = f"https://www.youtube.com/channel/{self.video_id}"
            self.title = self.video_response["items"][0]["snippet"]["title"]
            self.view_count = self.video_response["items"][0]["statistics"]["viewCount"]
            self.like_count = self.video_response["items"][0]["statistics"]["likeCount"]
        except IndexError:
            self.video_response = None
            self.url = None
            self.title = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
