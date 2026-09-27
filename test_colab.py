import requests

COLAB_URL = "https://scalding-creme-broiling.ngrok-free.dev"

response = requests.post(
    f"{COLAB_URL}/summarize",
    json={
        "text": """
        Artificial intelligence is transforming many industries.
        Machine learning allows computers to learn patterns from data.
        Deep learning uses neural networks with multiple layers
        to solve complex problems such as image recognition,
        natural language processing, and speech recognition.
        """
    },
    timeout=120
)

print("Status:", response.status_code)
print("Status:", response.status_code)
print("Response:", response.text)