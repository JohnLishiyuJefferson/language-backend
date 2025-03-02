import re
import os


def process_subtitle(input_text):
    # 用来匹配字幕时间戳的正则表达式
    time_pattern = r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$'
    # 用来匹配纯数字的正则表达式
    number_pattern = r'^\d+$'

    # 分割文本为每行
    lines = input_text.split('\n')
    result_lines = []

    for line in lines:
        # 去除空行
        if not line.strip():
            continue
        # 如果是时间戳行，或者是纯数字行，或者是空行，则跳过
        if re.match(time_pattern, line) or re.match(number_pattern, line):
            continue
        result_lines.append(line.strip())

    # 将处理后的行合并回一个文本
    return '\n'.join(result_lines)


def save_processed_text(file_path, processed_text):
    # 获取文件名和后缀
    base_name, ext = os.path.splitext(os.path.basename(file_path))
    # 生成新的文件名，添加 "_processed" 后缀
    new_file_name = "/Users/C5389057/PycharmProjects/PythonProject/subtitle/处理后的文本/" + f"{base_name}_processed{ext}"

    # 保存处理后的文本到新文件
    with open(new_file_name, 'w', encoding='utf-8') as file:
        file.write(processed_text)

    print(f"处理后的文本已保存到: {new_file_name}")


# 主函数
def process_subtitle_file(input_file):
    # 读取原始字幕文件
    with open(input_file, 'r', encoding='utf-8') as file:
        input_text = file.read()

    # 处理字幕文本
    processed_text = process_subtitle(input_text)

    # 保存处理后的文本到本地
    save_processed_text(input_file, processed_text)


# 运行示例
input_file = '/Users/C5389057/Downloads/TOP GUN.WEBRip.ja.srt'  # 请替换为你的实际文件路径
process_subtitle_file(input_file)
