import os

from flask import Flask, request, jsonify, send_file, abort
from flask_cors import CORS

from LLM.DeepSeek应用 import ai_reply
from aws.服务器请求aws通过文本生成语音 import local_synthesize, synthesize
from use.拆分句子并关联词典 import parse_sentence

app = Flask(__name__)
CORS(app)  # 允许所有域访问

@app.route('/')
def home():
    return "Hello, this is a Flask server!"

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json  # 获取 JSON 数据
    input_text = data.get("text", "")

    elements, original_text_list = parse_sentence(input_text)
    # 把列表转换成 JSON 格式
    result_list = [element.to_dict() for element in elements]
    return jsonify({"result_list": result_list, "original_text_list": original_text_list})  # 返回 JSON


@app.route('/ai', methods=['POST'])
def ai_reply_api():
    try:
        # 获取 JSON 请求数据
        data = request.json

        # 解析参数
        sentence = data.get("sentence", "")
        questions = data.get("questions", [])

        # 确保 questions 是列表
        if not isinstance(questions, list):
            return jsonify({"error": "questions must be a list"}), 400

        reply = ai_reply(sentence, questions[-1])
        return jsonify(reply)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 路由：提供音频文件
@app.route('/get-audio', methods=['GET'])
def get_audio():
    # 指定音频文件路径
    audio_path = '/Users/C5389057/Downloads/老鼠爱大米.mp3'

    # 检查音频文件是否存在
    if os.path.exists(audio_path):
        # 使用 send_file 返回音频文件
        return send_file(audio_path, mimetype='audio/mp3', as_attachment=True, download_name='my-audio.mp3')
    else:
        return "Audio file not found", 404

@app.route('/get-video', methods=['GET'])
def get_video():
    video_path = '/Users/C5389057/Downloads/鸡你太美.mp4'
    if os.path.exists(video_path):
        # 使用 send_file 返回视频文件，设置 MIME 类型为 video/mp4
        return send_file(video_path, mimetype='video/mp4', as_attachment=False)
    else:
        abort(404, description="Video file not found")

@app.route("/synthesize", methods=["GET", "POST"])
def get_synthesized_audio():
    # 支持 GET 或 POST 方式传入文本参数
    if request.method == "POST":
        data = request.get_json() or {}
        text = data.get("text", "")
        use_ai = str(data.get("useAI", "false")).lower() in "true"
    else:
        text = request.args.get("text", "")
        use_ai = str(request.args.get("useAI", "false")).lower() in "true"

    if not text:
        return jsonify({"error": "Missing 'text' parameter"}), 400

    if use_ai:
        return synthesize(text)
    else:
        return local_synthesize(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
