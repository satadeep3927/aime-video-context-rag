from urllib.parse import parse_qs, urlparse

import streamlit as st
import streamlit.components.v1 as components  # type: ignore[attr-defined]

from src.agents.schema import VideoResponse
from src.agents.youtube_agent import create_youtube_agent


def extract_video_id(url: str) -> str | None:
    """Extract the video ID from various YouTube URL formats."""
    parsed = urlparse(url)
    if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]
        if parsed.path.startswith("/v/"):
            return parsed.path.split("/")[2]
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")
    return None


def render_video_embed(video_id: str, start: int) -> None:
    """Render a single YouTube iframe embed at the given start time."""
    embed_url = f"https://www.youtube.com/embed/{video_id}?start={start}&autoplay=1"
    components.iframe(embed_url, height=400, width=700)


def render_timestamp_links(
    timestamps: list[dict], msg_index: int
) -> None:
    """Render timestamps as a simple clickable list."""
    if not timestamps:
        return
    for i, ts in enumerate(timestamps):
        key = f"ts_{msg_index}_{i}_{ts['start_seconds']}"
        cols = st.columns([0.95, 0.05])
        with cols[0]:
            st.markdown(
                f"- **{ts['timestamp']}** — {ts['description']}"
            )
        with cols[1]:
            if st.button("▶", key=key, help="Jump to this timestamp"):
                st.session_state.video_start = int(ts["start_seconds"])
                st.rerun()


st.set_page_config(page_title="YouTube Video Chat", page_icon="▶️", layout="wide")
st.title("▶️ YouTube Video Chat")
st.caption("Paste a YouTube link, then ask questions about the video content.")

# Session state defaults
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "current_video_id" not in st.session_state:
    st.session_state.current_video_id = None
if "video_start" not in st.session_state:
    st.session_state.video_start = 0

# Sidebar for video input
with st.sidebar:
    st.header("Video")
    video_url = st.text_input(
        "YouTube URL", placeholder="https://www.youtube.com/watch?v=..."
    )

    video_id = None
    if video_url:
        video_id = extract_video_id(video_url.strip())
        if video_id:
            st.success(f"Video ID: `{video_id}`")
        else:
            st.error("Could not extract a valid video ID from this URL.")

# Reset agent when video changes
if video_id and video_id != st.session_state.current_video_id:
    st.session_state.current_video_id = video_id
    st.session_state.agent = None
    st.session_state.messages = []
    st.session_state.video_start = 0

# Main layout: video player on top, chat below
if video_id:
    render_video_embed(video_id, st.session_state.video_start)
    st.divider()

# Display chat history
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("timestamps"):
            render_timestamp_links(msg["timestamps"], idx)

# Chat input
if prompt := st.chat_input("Ask a question about the video..."):
    if not video_id:
        st.error("Please paste a YouTube URL in the sidebar first.")
    else:
        # Create agent on first message (lazy init so token is fetched once)
        if st.session_state.agent is None:
            with st.spinner("Loading video transcript..."):
                st.session_state.agent = create_youtube_agent(video_id)

        # Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.agent.run(
                    prompt, output_schema=VideoResponse
                )
                parsed: VideoResponse = response.content  # type: ignore[assignment]

            st.markdown(parsed.answer)

            ts_list = [
                {
                    "timestamp": ref.timestamp,
                    "start_seconds": ref.start_seconds,
                    "description": ref.description,
                }
                for ref in parsed.references
            ]
            msg_idx = len(st.session_state.messages)
            render_timestamp_links(ts_list, msg_idx)

        st.session_state.messages.append(
            {"role": "assistant", "content": parsed.answer, "timestamps": ts_list}
        )
