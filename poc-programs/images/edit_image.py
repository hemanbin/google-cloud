from google import genai
from google.genai import types
from PIL import Image

client = genai.Client(
    vertexai=True,
    project="gcp-support-test-347006",
    location="global",
)

# client = genai.Client()

system_prompt = "你是一位专业的图像生成引擎。收到用户描述后立即生成图片，不要提问、不要给出选项、不要等待用户确认。"
user_prompt = "你把这个文件里的logo抠出来变成透明底"


image = Image.open("/home/hemanbin/google-cloud/poc-programs/images/79b9839f5758.jpg")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[user_prompt, image],
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_modalities=["IMAGE", "TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_CIVIC_INTEGRITY", threshold="OFF"),
        ],
        temperature=0.0,
    ),
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")