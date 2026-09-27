from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


app = FastAPI(title="YouTube Summarizer API")


# ---------- Request Schema ----------

class VideoRequest(BaseModel):
    url: str


# ---------- YouTube Utilities ----------

def extract_video_id(url: str) -> str | None:
    parsed_url = urlparse(url)

    # https://www.youtube.com/watch?v=VIDEO_ID
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]

    # https://youtu.be/VIDEO_ID
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path.strip("/")

    return None


def get_transcript(video_id: str) -> str:
    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id)

    text = " ".join(
        snippet.text
        for snippet in transcript
    )

    return text


# ---------- Text Processing ----------

def clean_text(text: str) -> str:
    text = " ".join(text.split())
    return text


def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100
) -> list[str]:

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ---------- API Endpoint ----------

@app.post("/process-video")
def process_video(request: VideoRequest):

    # 1. Extract video ID
    video_id = extract_video_id(request.url)

    if not video_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL"
        )

    try:

        # 2. Get transcript
        transcript = get_transcript(video_id)

        if not transcript:
            raise HTTPException(
                status_code=404,
                detail="Transcript is empty"
            )

        # 3. Clean transcript
        transcript = clean_text(transcript)

        # 4. Chunk transcript
        chunks = chunk_text(
            transcript,
            chunk_size=800,
            overlap=100
        )

        return {
            "video_id": video_id,
            "transcript_length": len(transcript),
            "number_of_chunks": len(chunks),
            "chunks": chunks
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process video: {str(e)}"
        )