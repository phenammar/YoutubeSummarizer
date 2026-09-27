from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from transformers import BartTokenizer

tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

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


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 100) -> list[str]:
    tokens = tokenizer.encode(text, add_special_tokens=False)

    chunks = []

    start = 0

    while start < len(tokens):
        end = start + chunk_size

        chunk_tokens = tokens[start:end]

        chunk = tokenizer.decode(
            chunk_tokens,
            skip_special_tokens=True
        )

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


#--------------- this step depends on the colab notebook -----------

import requests
COLAB_URL = "https://scalding-creme-broiling.ngrok-free.dev"

def summarize_chunk(text: str) -> str:
    response = requests.post(
        f"{COLAB_URL}/summarize",
        json={"text": text},
        timeout=120
    )

    response.raise_for_status()

    return response.json()["summary"]

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

        summaries = []

        for chunk in chunks:
            summary = summarize_chunk(chunk)
            summaries.append(summary)

        combined_summaries = " ".join(summaries)

        final_summary = "\n\n".join(summaries)

        return {
            "video_id": video_id,
            "transcript_length": len(transcript),
            "number_of_chunks": len(chunks),
            "summary": final_summary
}



    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process video: {str(e)}"
        )


@app.post("/test-summary")
def test_summary():
    text = """
    Artificial intelligence is transforming many industries.
    Machine learning allows computers to learn patterns from data.
    Deep learning uses neural networks with multiple layers
    to solve complex problems such as image recognition,
    natural language processing, and speech recognition.
    """

    summary = summarize_chunk(text)

    return {
        "summary": summary
    }