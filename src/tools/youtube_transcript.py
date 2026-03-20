from agno.tools.toolkit import Toolkit

from src.services.transcribe import TranscribeService


class YouTubeTranscriptToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="youtube_transcript")
        self.service = TranscribeService()
        self._transcript_cache: dict[str, list[dict]] = {}
        self.register(self.get_transcript)
        self.register(self.search_transcript)

    def _fetch_and_cache(self, video_id: str) -> list[dict]:
        if video_id in self._transcript_cache:
            return self._transcript_cache[video_id]

        transcript = self.service.transcribe(video_id)
        segments = []
        for snippet in transcript.snippets:
            total_seconds = int(snippet.start)
            minutes, seconds = divmod(total_seconds, 60)
            hours, minutes = divmod(minutes, 60)
            if hours > 0:
                timestamp = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                timestamp = f"{minutes}:{seconds:02d}"
            segments.append(
                {
                    "text": snippet.text,
                    "start": snippet.start,
                    "duration": snippet.duration,
                    "timestamp": timestamp,
                }
            )
        self._transcript_cache[video_id] = segments
        return segments

    def get_transcript(self, video_id: str) -> str:
        """Fetches the full transcript of a YouTube video. Returns all transcript segments
        with their timestamps and text. Use this to load the video content before answering questions.

        Args:
            video_id: The YouTube video ID (e.g. 'dQw4w9WgXcQ').

        Returns:
            A formatted string of all transcript segments with timestamps.
        """
        segments = self._fetch_and_cache(video_id)
        lines = []
        for seg in segments:
            lines.append(f"[{seg['timestamp']}] {seg['text']}")
        return "\n".join(lines)

    def search_transcript(self, video_id: str, query: str) -> str:
        """Searches the transcript of a YouTube video for segments matching a query.
        Returns matching segments with their timestamps. Use this to find specific
        parts of the video related to a user's question.

        Args:
            video_id: The YouTube video ID.
            query: The search term or phrase to look for in the transcript.

        Returns:
            Matching transcript segments with timestamps, or a message if nothing was found.
        """
        segments = self._fetch_and_cache(video_id)
        query_lower = query.lower()
        matches = [
            seg for seg in segments if query_lower in seg["text"].lower()
        ]
        if not matches:
            return f"No segments found matching '{query}'. Try using get_transcript to read the full transcript."
        lines = []
        for seg in matches:
            lines.append(
                f"[{seg['timestamp']} | start={seg['start']}s] {seg['text']}"
            )
        return "\n".join(lines)
