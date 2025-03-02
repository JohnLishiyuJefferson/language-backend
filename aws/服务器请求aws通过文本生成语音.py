from flask import Flask, request, send_file, jsonify
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from tempfile import gettempdir
import os
import uuid
import subprocess
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

def local_synthesize(text: str):
    # 生成临时文件路径（AIFF 和 MP3）
    aiff_file = os.path.join(AUDIO_DIR, f"{uuid.uuid4().hex}.aiff")
    mp3_file = os.path.join(AUDIO_DIR, f"{uuid.uuid4().hex}.mp3")

    # 使用 macOS say 命令生成 AIFF 音频文件，使用日语语音 Kyoko
    try:
        # 注意：命令格式： say -v Kyoko "文本" -o 输出文件
        subprocess.run(['say', '-v', 'Kyoko', text, '-o', aiff_file], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to generate audio with say", "details": str(e)}), 500

    # 使用 ffmpeg 将 AIFF 文件转换为 MP3 文件
    try:
        # -y 表示覆盖已存在的输出文件
        subprocess.run(['ffmpeg', '-y', '-i', aiff_file, '-acodec', 'libmp3lame', mp3_file], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to convert AIFF to MP3", "details": str(e)}), 500

    # 删除 AIFF 文件（可选）
    try:
        os.remove(aiff_file)
    except Exception as e:
        print("Warning: Failed to remove temporary AIFF file", e)

    # 返回 MP3 文件，设置 as_attachment=True 使浏览器提示下载
    return send_file(
        mp3_file,
        mimetype="audio/mpeg",
        as_attachment=True,
        download_name="speech.mp3"
    )