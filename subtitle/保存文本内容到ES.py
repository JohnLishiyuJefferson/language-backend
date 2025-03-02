import requests
import re

# 定义读取本地日语文件的函数
def read_japanese_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()


# 定义发送 POST 请求的函数
def send_text_to_java_backend(text_list):
    url = "http://localhost:85/es/add-text-list"  # 替换为你的实际 Java 接口地址
    payload = {"text_list": text_list}  # 将文本作为 JSON 请求体的一部分发送
    payload = text_list
    headers = {"Content-Type": "application/json"}  # 设置请求头，告诉服务器发送的是 JSON 数据

    # 发送 POST 请求
    response = requests.post(url, json=payload, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        print("文本成功发送并保存到 Elasticsearch")
    else:
        print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")


def split_sentences(text: str) -> list:
    # 使用正则表达式拆分字符串，匹配换行符、问号、句号和感叹号
    sentences = re.split(r'[\n?!。！]', text)

    # 清理每个句子前后空白字符
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    return sentences

# 主程序
if __name__ == "__main__":
    file_path = "/Users/C5389057/PycharmProjects/PythonProject/subtitle/处理后的文本/Titanic.srt"  # 替换为实际文件路径
    # text_list = read_japanese_file(file_path)  # 读取日语文件内容
    text = "CCTVによると、探査車のレーダーが探知したのは、中・低緯度地域の地表から10～35メートルの深さにある多層の堆積（たいせき）物。層の傾斜などが地球上で海岸線が形成される際の地質学的な特徴と似ているという。abcabc　「祝融」は2021年5月に火星に着陸。過去の研究成果が高緯度地域に集中していたのに対して、人間の活動に適した低・中緯度地域を探査した。今回の研究により、火星にかつて居住可能な環境があったことが裏付けられたと報じている。abcabc　中国は昨年発表した2050年までの宇宙計画で「人類が居住可能な星を探す」という目標を掲げる。CCTVは「大量の水が地下に氷として閉じ込められている可能性があり、将来の火星基地の建設費も大幅に削減されるだろう」としている。";
    text_list = split_sentences(text)
    send_text_to_java_backend(text_list)  # 发送内容到后端
