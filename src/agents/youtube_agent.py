from agno.agent import Agent

from src.agno.copilot import Copilot
from src.agno.lib import get_access_token_from_copilot
from src.tools.youtube_transcript import YouTubeTranscriptToolkit

SYSTEM_PROMPT = """\
You are a helpful YouTube video assistant. You answer questions about YouTube videos
using their transcripts.

IMPORTANT RULES:
1. When answering a question, ALWAYS use the tools to fetch or search the transcript first.
2. For every piece of information you cite, include it in the `references` list with:
   - `timestamp`: the human-readable time (e.g. "2:30" or "1:02:03")
   - `start_seconds`: the exact start time in seconds from the transcript
   - `description`: a short description of what happens at that point
3. Put your full answer in the `answer` field using markdown.
4. If the transcript doesn't contain relevant information, say so clearly.
5. The video_id will be provided in the conversation context — use it in tool calls.
"""


def create_youtube_agent(video_id: str) -> Agent:
    """Creates an Agent configured to answer questions about a specific YouTube video."""
    return Agent(
        name="YouTubeVideoAgent",
        description="An agent that answers questions about YouTube videos using transcripts.",
        model=Copilot(id="gpt-4.1", api_key=get_access_token_from_copilot()),
        tools=[YouTubeTranscriptToolkit()],
        instructions=[
            SYSTEM_PROMPT,
            f"The current video_id is: {video_id}",
            "Always use this video_id when calling transcript tools.",
        ],
        markdown=True,
    )
