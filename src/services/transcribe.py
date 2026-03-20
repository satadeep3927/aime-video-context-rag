from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

from src.core.config import settings


class TranscribeService:
    def __init__(self):
        self.ytt = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=settings.WEBSHARE_PROXY_USERNAME,
                proxy_password=settings.WEBSHARE_PROXY_PASSWORD,
            )
        )

    def transcribe(self, video_id: str):
        transcript = self.ytt.fetch(video_id)
        return transcript
