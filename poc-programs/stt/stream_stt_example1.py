import os
import time
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.api_core.client_options import ClientOptions

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "asia-southeast1"

SAMPLE_RATE = 16000
CHUNK_SIZE = 4096  # 每次发送的字节数

def read_pcm_chunks(file_path: str, chunk_size: int):
    """逐块读取 PCM 文件，模拟音频流"""
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def build_requests(file_path: str):
    """构建流式请求生成器，第一个请求发配置，后续发音频数据"""

    # 第一个请求：发送识别配置
    recognition_config = cloud_speech.RecognitionConfig(
        explicit_decoding_config=cloud_speech.ExplicitDecodingConfig(
            encoding=cloud_speech.ExplicitDecodingConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=SAMPLE_RATE,
            audio_channel_count=1,
        ),
        language_codes=["ms-MY"],
        model="chirp_2",
        features=cloud_speech.RecognitionFeatures(
            enable_automatic_punctuation=True,
        ),
    )

    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config,
        streaming_features=cloud_speech.StreamingRecognitionFeatures(
            interim_results=True,  # 返回中间结果（未最终确认的识别结果）
        ),
    )

    config_request = cloud_speech.StreamingRecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/{LOCATION}/recognizers/_",
        streaming_config=streaming_config,
    )

    yield config_request

    # 后续请求：逐块发送音频数据
    for chunk in read_pcm_chunks(file_path, CHUNK_SIZE):
        yield cloud_speech.StreamingRecognizeRequest(audio=chunk)


def streaming_transcribe(file_path: str):
    """流式识别 PCM 文件"""
    client = SpeechClient(
        client_options=ClientOptions(
            api_endpoint=f"{LOCATION}-speech.googleapis.com"
        )
    )

    print("开始流式识别...")

    responses = client.streaming_recognize(requests=build_requests(file_path))

    for response in responses:
        for result in response.results:
            transcript = result.alternatives[0].transcript

            if result.is_final:
                # 最终结果
                print(f"[最终] {transcript}")
            else:
                # 中间结果（实时显示，会被覆盖更新）
                print(f"[中间] {transcript}", end="\r")

    print("\n识别完成！")


if __name__ == "__main__":
    PCM_FILE = "/home/hemanbin/google-cloud/poc-programs/stt/778148516480.pcm"
    streaming_transcribe(PCM_FILE)