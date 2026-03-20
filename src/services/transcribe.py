from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig, WebshareProxyConfig

from src.core.config import settings


class TranscribeService:
    def __init__(self):
        self.ytt = YouTubeTranscriptApi(
            proxy_config=GenericProxyConfig(
                http_url=f"http://{settings.WEBSHARE_PROXY_USERNAME}:{settings.WEBSHARE_PROXY_PASSWORD}@{settings.WEBSHARE_PROXY_HOST}:{settings.WEBSHARE_PROXY_PORT}",
                https_url=f"http://{settings.WEBSHARE_PROXY_USERNAME}:{settings.WEBSHARE_PROXY_PASSWORD}@{settings.WEBSHARE_PROXY_HOST}:{settings.WEBSHARE_PROXY_PORT}",
            )
        )

    def transcribe(self, video_id: str):
        transcript = self.ytt.fetch(video_id)
        return transcript
