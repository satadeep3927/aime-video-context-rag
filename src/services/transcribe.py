from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound


class TranscribeService:
    def __init__(self):
        self.ytt = YouTubeTranscriptApi()

    def transcribe(self, video_id: str):
        try:
            return self.ytt.fetch(video_id, languages=("en",))
        except NoTranscriptFound:
            transcript_list = self.ytt.list(video_id)
            # If nothing is translatable, just return the first available transcript
            for transcript in transcript_list:
                return transcript.fetch()
            raise
