import openai
import pygame

# 🔹 设置 OpenAI API Key
openai.api_key = "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"

# 🔹 需要朗读的文本（日语）
text = "こんにちは、これは日本語のテストです。"

# 🔹 调用 OpenAI 的 TTS API
response = openai.audio.speech.create(
    model="tts-1",  # 或者 "tts-1-hd"（高清版）
    voice="alloy",  # 可选: "alloy", "nova", "shimmer"（不同音色）
    input=text
)

# 🔹 将语音文件保存
output_file = "output.mp3"
with open(output_file, "wb") as f:
    f.write(response.content)

# 🔹 使用 pygame 播放语音
pygame.mixer.init()
pygame.mixer.music.load(output_file)
pygame.mixer.music.play()

# 等待音频播放结束
while pygame.mixer.music.get_busy():
    pass
