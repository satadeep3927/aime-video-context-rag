from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound



class TranscribeService:
    def __init__(self):
        self.ytt = YouTubeTranscriptApi()

    def transcribe(self, video_id: str):
        try:
            return self.ytt.fetch(video_id, languages=("en",))
        except NoTranscriptFound:
            # No English transcript — find any available and translate to English
            transcript_list = self.ytt.list(video_id)
            for transcript in transcript_list:
                if any(
                    lang.language_code == "en"
                    for lang in transcript.translation_languages
                ):
                    return transcript.translate("en").fetch()
            # If nothing is translatable, just return the first available transcript
            for transcript in transcript_list:
                return transcript.fetch()
            raise
