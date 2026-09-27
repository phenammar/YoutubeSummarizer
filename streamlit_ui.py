import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="🎥",
    layout="centered"
)

st.title("🎥 YouTube Summarizer")
st.write("Enter a YouTube video URL and get a summary.")

url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

if st.button("Summarize", type="primary"):

    if not url.strip():
        st.warning("Please enter a YouTube URL.")
    else:
        with st.spinner("Processing video..."):

            try:
                response = requests.post(
                    f"{BACKEND_URL}/process-video",
                    json={"url": url},
                    timeout=600
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success("Summary generated successfully!")

                    st.subheader("Summary")

                    st.write(data["summary"])

                    st.divider()

                    st.caption(
                        f"Video ID: {data['video_id']} | "
                        f"Transcript length: {data['transcript_length']} characters | "
                        f"Chunks: {data['number_of_chunks']}"
                    )

                else:
                    st.error(
                        f"Backend error ({response.status_code}): "
                        f"{response.text}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the FastAPI backend. "
                    "Make sure FastAPI is running."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The request took too long. "
                    "The video may be too long."
                )

            except Exception as e:
                st.error(f"Unexpected error: {e}")