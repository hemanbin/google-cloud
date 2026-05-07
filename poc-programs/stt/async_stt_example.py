import os
import sys
import time
from concurrent.futures import TimeoutError

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

curl_command=f"""
    curl -X GET -H "Authorization: Bearer $(gcloud auth print-access-token)" \\
        -H "x-goog-user-project: {PROJECT_ID}" \\
        "https://{LOCATION}-speech.googleapis.com/v2/{operation.operation.name}"
    """

print(f"\nYou can use curl command to query the operation: \n {curl_command}")

#"""
# 获取结果方式 1: 手动轮询是否完成
MAX_WAIT = 600  # 最多等待 300 秒
elapsed = 0
try:
    while not operation.done():
        if elapsed >= MAX_WAIT:
            raise TimeoutError(f"超过 {MAX_WAIT} 秒仍未完成")
        print(f"识别中... 已等待 {elapsed} 秒")
        time.sleep(5)
        elapsed += 5

    response = operation.result()
    print("已完成！")
except TimeoutError as e:
    print(f"超时: {e}")
    sys.exit(1)
except Exception as e:
    print(f"识别失败: {e}")
    sys.exit(2)
#"""


"""
# 获取结果方式 2: 阻塞等待结果
try:
    response = operation.result(timeout=1800)
    print("识别完成")
except TimeoutError:
    print("超时，任务仍在后台运行")
    sys.exit(1)
except Exception as e:
    print(f"识别失败: {e}")
    sys.exit(2)
"""

for result in response.results[audio_uri].transcript.results:
    print(f"Transcript: {result.alternatives[0].transcript}")
    print(f"Detected Language: {result.language_code}")
    print(f"Speakers per word: {result.alternatives[0].words}")