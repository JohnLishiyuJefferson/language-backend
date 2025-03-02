from flask import Flask, request, send_file, jsonify
import os
import subprocess
import uuid
from tempfile import gettempdir

app = Flask(__name__)


@app.route('/synthesize', methods=['GET', 'POST'])
def synthesize():
    # 从查询参数或 JSON 数据中获取文本
    if request.method == 'POST':
        data = request.get_json() or {}
        text = data.get('text')
    else:
        text = request.args.get('text')

    if not text:
        return jsonify({"error": "Missing 'text' parameter"}), 400

    # 生成临时文件路径（AIFF 和 MP3）
    temp_dir = gettempdir()
    aiff_file = os.path.join(temp_dir, f"{uuid.uuid4().hex}.aiff")
    mp3_file = os.path.join(temp_dir, f"{uuid.uuid4().hex}.mp3")

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


if __name__ == '__main__':
    app.run(debug=True)
