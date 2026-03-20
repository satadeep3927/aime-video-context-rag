from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig


class TranscribeService:
    def __init__(self):
        self.ytt = YouTubeTranscriptApi(
            proxy_config=GenericProxyConfig(http_url="http://47.243.181.85:41714")
        )

    def transcribe(self, video_id: str):
        transcript = self.ytt.fetch(video_id)
        return transcript
