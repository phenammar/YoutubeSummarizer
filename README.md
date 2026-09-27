# 🎥 YouTube Summarizer

A simple YouTube video summarizer built with **FastAPI, Streamlit, Hugging Face BART, Google Colab GPU, and ngrok**.

## 🏗️ Architecture

```text
Streamlit
    ↓
Local FastAPI
    ↓
YouTube Transcript
    ↓
Token Chunking
    ↓
ngrok
    ↓
Colab FastAPI + BART
    ↓
Chunk Summaries
    ↓
Streamlit
```

## 🚀 Features

* Extract YouTube transcripts
* Clean and chunk long transcripts
* Token-based chunking using BART tokenizer
* Summarize chunks using `facebook/bart-large-cnn`
* GPU inference through Google Colab
* Simple Streamlit interface

## 🛠️ Tech Stack

* Python
* FastAPI
* Streamlit
* Hugging Face Transformers
* BART Large CNN
* YouTube Transcript API
* Google Colab GPU
* ngrok

## 📁 Structure

```text
youtube-summarizer/
├── backend/
│   └── main.py
├── streamlit_app.py
└── README.md
```

## ▶️ Run

### 1. Start the Colab server

Load:

```text
facebook/bart-large-cnn
```

and expose the FastAPI `/summarize` endpoint through ngrok.

Then update the ngrok URL in the local backend:

```python
COLAB_URL = "https://YOUR-NGROK-URL.ngrok-free.dev"
```

### 2. Start FastAPI

```bash
cd backend
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

### 3. Start Streamlit

From the project root:

```bash
python -m streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501
```

## ⚙️ Current Configuration

```text
Chunk size: 900 tokens
Overlap:    100 tokens
Model:      facebook/bart-large-cnn
Inference:  Google Colab GPU
```

Each transcript chunk is summarized independently, then the summaries are combined.

## ⚠️ Notes

* The ngrok URL may change after restarting Colab.
* YouTube automatic transcripts can contain transcription errors.
* Long videos produce more chunks and take longer to process.
* The project currently does not use a final summarization pass.

## 🔮 Future Improvements

* Better transcript cleaning
* Progress tracking
* Arabic summarization
* Timestamped summaries
* Better handling of repeated information
* Permanent model deployment
