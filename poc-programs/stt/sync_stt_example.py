import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.api_core.client_options import ClientOptions


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us"

api_endpoint = f"{LOCATION}-speech.googleapis.com"

client = SpeechClient(client_options=ClientOptions(api_endpoint=api_endpoint))

config = cloud_speech.RecognitionConfig(
    auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
    language_codes=["en-US"],
    model="chirp_3",
    features=cloud_speech.RecognitionFeatures(
        # Enable automatic punctuation
        enable_automatic_punctuation=True,
    )
)
"""
# If you want to open local audio file, please uncomment this snip codes, 
# and notice to modify request section about uri and content.

with open("/home/hemanbin/english-radio.mp3", "rb") as f:
    audio_content = f.read()
"""

request = cloud_speech.RecognizeRequest(
    recognizer=f"projects/{PROJECT_ID}/locations/{LOCATION}/recognizers/_",
    config=config,
    uri="gs://hemanbin-common/example_files/stt_files/short_time_speech.mp3",
    #content=audio_content,
)

# Transcribes the audio into text
response = client.recognize(request=request)

for result in response.results:
    print(f"Transcript: {result.alternatives[0].transcript}")

