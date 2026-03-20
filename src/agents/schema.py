from pydantic import BaseModel, Field


class TimestampReference(BaseModel):
    timestamp: str = Field(
        description="The timestamp in MM:SS or H:MM:SS format, e.g. '2:30' or '1:02:03'."
    )
    start_seconds: float = Field(
        description="The start time in seconds from the transcript, e.g. 150.0."
    )
    description: str = Field(
        description="A short description of what happens at this timestamp."
    )


class VideoResponse(BaseModel):
    answer: str = Field(
        description="The full answer to the user's question in markdown format."
    )
    references: list[TimestampReference] = Field(
        default_factory=list,
        description="List of timestamp references cited in the answer, each with a timestamp and description.",
    )
