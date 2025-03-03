import os
from contextlib import closing

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from flask import send_file, jsonify

from util.工具 import sha256_hash

AUDIO_DIR = "/Users/C5389057/PycharmProjects/PythonProject/aws/generated_content"

def synthesize(text: str):
    # 计算文本对应的 SHA-256 哈希
    file_hash = sha256_hash(text)
    filename = os.path.join(AUDIO_DIR, f"{file_hash}.mp3")
    # 如果文件已存在，直接返回
    if os.path.exists(filename):
        return send_file(
            filename,
            mimetype="audio/mp3",
            as_attachment=True,
            download_name="speech.mp3",
        )
    # 使用默认 AWS 账户配置创建一个 boto3 Session
    session = Session(profile_name="default")
    polly = session.client("polly")

    try:
        # 调用 Amazon Polly 合成语音接口
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Mizuki",
            LanguageCode="ja-JP"
        )
    except (BotoCoreError, ClientError) as error:
        return jsonify({"error": str(error)}), 500

    if "AudioStream" not in response:
        return jsonify({"error": "Could not stream audio"}), 500

    try:
        # 通过 contextlib.closing 确保流正确关闭
        with closing(response["AudioStream"]) as stream:
            with open(filename, "wb") as file:
                file.write(stream.read())
    except IOError as error:
        return jsonify({"error": str(error)}), 500

    # 返回生成的 MP3 文件，设置 as_attachment=True 会让浏览器提示下载
    return send_file(
        filename,
        mimetype="audio/mp3",
        as_attachment=True,
        download_name="speech.mp3"
    )
