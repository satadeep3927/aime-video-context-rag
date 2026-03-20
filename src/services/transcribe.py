from youtube_transcript_api import YouTubeTranscriptApi


class TranscribeService:
    def __init__(self):
        self.ytt = YouTubeTranscriptApi()

    def transcribe(self, video_id: str):
        transcript = self.ytt.fetch(video_id)
        return transcript
