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
    language_codes=["cmn-Hans-CN"],
    model="chirp_3",
    features=cloud_speech.RecognitionFeatures(
        # Enable automatic punctuation
        enable_automatic_punctuation=True,
    )
)
audio_uri = "gs://hemanbin-common/example_files/stt_files/short_time_speech.mp3"
# 长音频用 batch_recognize（异步），传 GCS URI
request = cloud_speech.BatchRecognizeRequest(
    recognizer=f"projects/{PROJECT_ID}/locations/{LOCATION}/recognizers/_",
    config=config,
    files=[
        cloud_speech.BatchRecognizeFileMetadata(
            uri=audio_uri
        )
    ],
    recognition_output_config=cloud_speech.RecognitionOutputConfig(
        inline_response_config=cloud_speech.InlineOutputConfig(),
    ),
)

operation = client.batch_recognize(request=request)
print(f"Operation: {operation.operation.name}")

# 阻塞等待结果
response = operation.result(timeout=600)

for result in response.results[audio_uri].transcript.results:
    print(f"Transcript: {result.alternatives[0].transcript}")