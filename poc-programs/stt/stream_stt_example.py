import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech as cloud_speech_types

from google.api_core.client_options import ClientOptions


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "asia-southeast1"

api_endpoint = f"{LOCATION}-speech.googleapis.com"

client = SpeechClient(client_options=ClientOptions(api_endpoint=api_endpoint))

# Reads a file as bytes
with open("/home/hemanbin/google-cloud/poc-programs/stt/778148516480.pcm", "rb") as f:
    audio_content = f.read()

# In practice, stream should be a generator yielding chunks of audio data
chunk_length = len(audio_content) // 40
stream = [
    audio_content[start : start + chunk_length]
    for start in range(0, len(audio_content), chunk_length)
]
audio_requests = (
    cloud_speech_types.StreamingRecognizeRequest(audio=audio) for audio in stream
)

recognition_config = cloud_speech_types.RecognitionConfig(
    explicit_decoding_config=cloud_speech_types.ExplicitDecodingConfig(
        encoding=cloud_speech_types.ExplicitDecodingConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,   # 按实际采样率填写：8000 / 16000 / 44100 等
        audio_channel_count=1,     # 单声道=1，立体声=2
    ),
    language_codes=["ms-MY"],
    model="chirp_2",
)
streaming_config = cloud_speech_types.StreamingRecognitionConfig(
    config=recognition_config
)
config_request = cloud_speech_types.StreamingRecognizeRequest(
    recognizer=f"projects/{PROJECT_ID}/locations/{LOCATION}/recognizers/_",
    streaming_config=streaming_config,
)

def requests(config: cloud_speech_types.RecognitionConfig, audio: list) -> list:
    yield config
    yield from audio

# Transcribes the audio into text
responses_iterator = client.streaming_recognize(
    requests=requests(config_request, audio_requests)
)
responses = []
for response in responses_iterator:
    responses.append(response)
    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
